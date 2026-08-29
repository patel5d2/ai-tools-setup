"""§3.5 — call a hosted model with a key loaded from .env (never hard-coded).

Works from a local .env (python-dotenv) or from Colab Secrets, which inject the
key into the environment directly — so os.getenv covers both. Uses Anthropic if
ANTHROPIC_API_KEY is set, else OpenAI.
"""
import os

from dotenv import load_dotenv

load_dotenv()  # no-op in Colab (no .env); key comes from Secrets → env there

PROMPT = "Reply with one short sentence confirming the API call worked."


def main() -> None:
    if os.getenv("ANTHROPIC_API_KEY"):
        from anthropic import Anthropic

        client = Anthropic()  # reads ANTHROPIC_API_KEY from env
        model = os.getenv("MODEL", "claude-opus-4-8")  # override e.g. claude-haiku-4-5 to save cost
        msg = client.messages.create(
            model=model, max_tokens=100,
            messages=[{"role": "user", "content": PROMPT}],
        )
        print(f"[Anthropic {model}] {msg.content[0].text}")
    elif os.getenv("OPENAI_API_KEY"):
        from openai import OpenAI

        client = OpenAI()  # reads OPENAI_API_KEY from env
        model = os.getenv("MODEL", "gpt-4o-mini")
        r = client.chat.completions.create(
            model=model, max_tokens=100,
            messages=[{"role": "user", "content": PROMPT}],
        )
        print(f"[OpenAI {model}] {r.choices[0].message.content}")
    else:
        raise SystemExit("No API key found. Copy .env.example to .env and fill one in.")


if __name__ == "__main__":
    main()
