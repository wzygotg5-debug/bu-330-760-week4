"""Math agent that solves questions using tools in a ReAct loop."""

import json
import time

from dotenv import load_dotenv
from pydantic_ai import Agent
from calculator import calculate

load_dotenv()

MODEL = "openai:gpt-4o-mini"

agent = Agent(
    MODEL,
    system_prompt=(
        "You are a helpful assistant. Solve each question step by step. "
        "Use the calculator tool only for valid Python arithmetic expressions. "
        "Do not use ^ for powers; use ** instead. "
        "Do not send equations with variables such as x or = into the calculator tool. "
        "If algebra is needed, reason it out in text first, then use the calculator only for final arithmetic. "
        "Use the product_lookup tool when a question mentions products from the catalog. "
        "Keep the final answer concise, usually one sentence. "
        "Do not repeat the full derivation in the final answer. "
        "Round money answers to two decimal places when appropriate."
    ),
)


@agent.tool_plain
def calculator_tool(expression: str) -> str:
    return calculate(expression)


@agent.tool_plain
def product_lookup(product_name: str) -> str:
    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    if product_name in products:
        return str(products[product_name])

    available_products = ", ".join(products.keys())
    return f"Product not found. Available products: {available_products}"


def load_questions(path: str = "math_questions.md") -> list[str]:
    questions = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and line[0].isdigit() and ". " in line[:4]:
                questions.append(line.split(". ", 1)[1])
    return questions


def main():
    questions = load_questions()

    for i, question in enumerate(questions, 1):
        print(f"## Question {i}")
        print(f"> {question}\n")

        result = agent.run_sync(question)

        print("### Trace")
        for message in result.all_messages():
            for part in message.parts:
                kind = part.part_kind
                if kind in ("user-prompt", "system-prompt"):
                    continue
                elif kind == "text":
                    print(f"- **Reason:** {part.content}")
                elif kind == "tool-call":
                    print(f"- **Act:** `{part.tool_name}({part.args})`")
                elif kind == "tool-return":
                    print(f"- **Result:** `{part.content}`")

        print(f"\n**Answer:** {result.output}\n")
        print("---\n")

        if i < len(questions):
            time.sleep(2)


if __name__ == "__main__":
    main()
