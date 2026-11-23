"""LIB-0040 CH02: demonstration of LLM routing to simulated handlers.

Requires: pip install langchain-core langchain-google-genai
          GOOGLE_API_KEY environment variable.
This example does NOT book anything and does not run privileged tools.
"""
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda, RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI

LABELS = {"booker", "info", "unclear"}

def normalize_label(value: str) -> str:
    label = value.strip().lower()
    return label if label in LABELS else "unclear"

def booking_handler(data: dict) -> str:
    return f"DEMO: booking handler received: {data['request']}"

def info_handler(data: dict) -> str:
    return f"DEMO: information handler received: {data['request']}"

def unclear_handler(data: dict) -> str:
    return "Please clarify the request."

def build_agent(llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Classify the user request. Flights/hotels reservation -> booker; "
                   "ordinary factual information -> info; otherwise -> unclear. "
                   "Return EXACTLY one label: booker, info, or unclear."),
        ("human", "{request}"),
    ])
    router = prompt | llm | StrOutputParser() | RunnableLambda(normalize_label)
    branch = RunnableBranch(
        (lambda x: x["decision"] == "booker", RunnableLambda(booking_handler)),
        (lambda x: x["decision"] == "info", RunnableLambda(info_handler)),
        RunnableLambda(unclear_handler),
    )
    return RunnablePassthrough.assign(decision=router) | branch

def main():
    if not os.getenv("GOOGLE_API_KEY"):
        raise SystemExit("Set GOOGLE_API_KEY before running this example.")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    agent = build_agent(llm)
    for request in ("Book me a flight to London", "What is the capital of Italy?",
                    "Help me with something"):
        try:
            print(agent.invoke({"request": request}))
        except Exception as exc:
            print(f"Router invocation failed: {type(exc).__name__}: {exc}")

if __name__ == "__main__":
    main()
