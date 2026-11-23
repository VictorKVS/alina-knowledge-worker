"""Chapter 2 — Routing: one coordinator, provider-independent LLM.

Usage: set AGENT_LLM_PROVIDER and AGENT_LLM_MODEL; python ch02_router.py.
The three handlers are MOCKS. No real booking or external tool actions.
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnablePassthrough

from model_adapter import ModelConfig, create_chat_model

LABELS = frozenset({"booker", "info", "unclear"})

def normalize_label(value: str) -> str:
    value = value.strip().lower()
    return value if value in LABELS else "unclear"

def booking_handler(state: dict) -> str:
    return "DEMO: booking task received: " + state["request"]

def info_handler(state: dict) -> str:
    return "DEMO: information task received: " + state["request"]

def unclear_handler(state: dict) -> str:
    return "DEMO: request needs clarification"

def build_agent(llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Select one handler for a user request. "
                   "booker for booking flights/hotels, info for general factual questions, "
                   "unclear for ambiguous or unsupported requests. "
                   "Reply with exactly one label: booker, info, or unclear."),
        ("human", "{request}"),
    ])
    classify = prompt | llm | StrOutputParser() | RunnableLambda(normalize_label)
    dispatch = RunnableBranch(
        (lambda x: x["route"] == "booker", RunnableLambda(booking_handler)),
        (lambda x: x["route"] == "info", RunnableLambda(info_handler)),
        RunnableLambda(unclear_handler),
    )
    return RunnablePassthrough.assign(route=classify) | dispatch

def main():
    config = ModelConfig.from_env()
    llm = create_chat_model(config)
    agent = build_agent(llm)
    print(f"Router provider={config.provider} model={config.model}")
    for question in ("Book me a flight to London", "What is the capital of Italy?",
                     "Help me with something"):
        try:
            print(agent.invoke({"request": question}))
        except Exception as exc:
            print(f"LLM/Router error: {type(exc).__name__}: {exc}")

if __name__ == "__main__":
    main()
