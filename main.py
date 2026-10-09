import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("API KEY NOT FOUND")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages = [
    {"role": "user", "content": args.user_prompt},
]
# Now we can access `args.user_prompt`

def main():
    print("Hello from boot-agent!")

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
)

def print_tokens(prompt_tokens, completion_tokens):
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {completion_tokens}")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print_tokens(response.usage.prompt_tokens, response.usage.completion_tokens)

if not response.usage:
    raise RuntimeError("usage is None")

print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
