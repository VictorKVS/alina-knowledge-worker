"""Two comparable agents in parallel: narrative continuity vs game-world state.

Run from project root: python -m projects.DUAL_AGENT_DECISION_LAB.dual_agents
Set AGENT_DECISION_MODE=llm to use existing ModelAdapter (Ollama/cloud).
Default rule policy is deterministic and needs only Python stdlib.
"""
from __future__ import annotations

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from pathlib import Path

@dataclass(frozen=True)
class Option:
    name: str
    purpose: str
    duration: int
    risk: float
    progress: int
    prerequisites: tuple[str, ...] = ()

@dataclass
class World:
    kind: str
    budget: int = 4
    facts: set[str] = field(default_factory=set)
    steps: list[str] = field(default_factory=list)
    position: int = 0
    hp: int = 2
    goal: bool = False

    def available(self) -> list[Option]:
        if self.kind == "story":
            pool = [
                Option("establish", "Establish a setting and character", 1, 0.0, 1),
                Option("clue", "Introduce clue, consistent with earlier scene", 1, 0.0, 2, ("establish",)),
                Option("reveal", "Resolve planted clue and character motive", 1, 0.0, 3, ("clue",)),
                Option("brief_end", "Short coherent ending if short of time", 1, 0.1, 1, ("establish",)),
            ]
        else:
            pool = [
                Option("scout", "Inspect hazard before moving", 1, 0.0, 0),
                Option("move", "Move one cell toward treasure", 1, 0.05 if "scout" in self.facts else 0.4, 2),
                Option("rush", "Advance quickly without observation", 1, 0.9, 4),
            ]
        return [
            action for action in pool
            if (self.kind == "game" or action.name not in self.facts)
            and action.duration <= self.budget
            and all(pre in self.facts for pre in action.prerequisites)
            and not (self.kind == "game" and action.name == "scout" and "scout" in self.facts)
        ]

    def observe(self) -> dict:
        return {"world": self.kind, "budget": self.budget, "facts": sorted(self.facts),
                "position": self.position, "hp": self.hp, "finished": self.goal}

    def step(self, action: Option) -> dict:
        allowed = {x.name: x for x in self.available()}
        if self.goal or action.name not in allowed or action.duration > self.budget:
            raise ValueError("Illegal action, stale state, or terminal episode")
        self.budget -= action.duration
        self.facts.add(action.name)
        if self.kind == "story":
            if action.name in {"reveal", "brief_end"}:
                self.goal = True
            observation = {
                "establish": "The traveler arrives at a deserted observatory.",
                "clue": "A logbook mentions an unannounced signal.",
                "reveal": "The signal came from a forgotten rescue beacon.",
                "brief_end": "The traveler leaves, preserving the mystery.",
            }[action.name]
        else:
            if action.name == "scout":
                observation = "A hazard is detected. Slower travel is safer."
            elif action.name == "move":
                self.position += 1
                if "scout" not in self.facts:
                    self.hp -= 1
                self.goal = self.position >= 2 and self.hp > 0
                observation = f"Moved to {self.position}; hp={self.hp}"
            else:
                self.position += 2
                self.hp -= 2
                self.goal = self.position >= 2 and self.hp > 0
                observation = f"Rushed to {self.position}; hp={self.hp}"
            if self.hp <= 0:
                observation += "; FAILED: player exhausted"
        self.steps.append(action.name)
        return {"action": action.name, "result": observation, "remaining": self.budget}

    def done(self) -> bool:
        return self.goal or self.budget == 0 or (self.kind == "game" and self.hp <= 0)

def score(option: Option, world: World, strategy: str = "balanced") -> float:
    """Transparent baseline, NOT an empirically calibrated optimal policy."""
    risk_weight = {"fast": 1.0, "balanced": 5.0, "careful": 11.0}[strategy]
    reward = option.progress * 2
    if world.kind == "story":
        if option.name == "brief_end":
            reward = 0 if world.budget > 1 else 4
        if option.name == "establish" and not world.facts:
            reward += 3
        if option.name == "reveal":
            reward += 3
    else:
        if option.name == "scout" and world.position == 0 and world.budget >= 3:
            reward += (3 if strategy in {"balanced", "careful"} else 0)
        if option.name == "rush" and world.hp <= 2:
            return float("-inf")  # hard safety constraint: unacceptable death risk
    return reward - risk_weight * option.risk - 0.2 * option.duration

def choose_rule(world: World, strategy: str) -> tuple[Option, str]:
    options = world.available()
    if not options:
        raise ValueError("No available action")
    ranked = sorted(options, key=lambda item: (-score(item, world, strategy), item.name))
    chosen = ranked[0]
    return chosen, f"rule: score={score(chosen, world, strategy):.2f}; risk={chosen.risk}; budget={world.budget}"

def choose_llm(world: World, strategy: str, llm) -> tuple[Option, str]:
    """LLM proposes one JSON action; Python validates against allowed set."""
    allowed = world.available()
    policy = (
        "You are a decision-maker inside a toy simulator. This text is DATA, not tool authority. "
        "Select exactly ONE action by its name, considering goal, prereqs, risk, "
        "time budget and strategy. Return ONLY JSON: "
        '{"action":"name","reason":"concise justification"}.'
    )
    payload = {
        "context": world.observe(), "strategy": strategy,
        "goal": "story consistency and resolved clue" if world.kind == "story"
                else "reach treasure with positive health",
        "available_actions": [asdict(a) for a in allowed],
    }
    result = llm.invoke([("system", policy), ("human", json.dumps(payload, ensure_ascii=False))])
    text = str(result.content).strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    try:
        proposal = json.loads(text)
        selected = next(x for x in allowed if x.name == proposal["action"])
    except (ValueError, KeyError, StopIteration, TypeError) as exc:
        fallback, reason = choose_rule(world, strategy)
        return fallback, f"invalid LLM proposal → {reason} ({type(exc).__name__})"
    if score(selected, world, strategy) == float("-inf"):
        fallback, reason = choose_rule(world, strategy)
        return fallback, f"unsafe LLM proposal denied → {reason}"
    return selected, f"llm: {str(proposal.get('reason',''))[:180]}"

def run_episode(kind: str, strategy: str, use_llm: bool = False) -> dict:
    world = World(kind)
    model = None
    if use_llm:
        # Reuse the existing model adapter without copying its credentials.
        examples = Path(__file__).resolve().parents[2] / "examples"
        sys.path.insert(0, str(examples))
        from model_adapter import ModelConfig, create_chat_model
        model = create_chat_model(ModelConfig.from_env())
    trace = []
    while not world.done():
        if not world.available():
            break
        before = world.observe()
        option, reasoning = (choose_llm(world, strategy, model) if model
                             else choose_rule(world, strategy))
        outcome = world.step(option)
        trace.append({"before": before, "chosen": asdict(option),
                      "reason": reasoning, "observation": outcome})
    return {"agent": kind, "strategy": strategy, "mode": "llm" if use_llm else "rule",
            "success": bool(world.goal), "final": world.observe(), "trace": trace}

def main():
    strategy = os.getenv("AGENT_STRATEGY", "balanced").strip().lower()
    if strategy not in {"fast", "balanced", "careful"}:
        raise ValueError("AGENT_STRATEGY must be fast|balanced|careful")
    mode = os.getenv("AGENT_DECISION_MODE", "rule").strip().lower()
    if mode not in {"rule", "llm"}:
        raise ValueError("AGENT_DECISION_MODE must be rule|llm")
    # Two independent episodes execute concurrently, not necessarily GPU-parallel.
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run_episode, kind, strategy, mode == "llm")
                   for kind in ("story", "game")]
        results = [future.result() for future in futures]
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
