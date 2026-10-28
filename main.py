import os
import json
from call_function import available_functions
from call_function import call_function
from prompts import system_prompt
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
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    temperature=0,
    tools=available_functions,
    )

def print_tokens(prompt_tokens, completion_tokens):
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {completion_tokens}")

if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print_tokens(response.usage.prompt_tokens, response.usage.completion_tokens)

if not response.usage:
    raise RuntimeError("usage is None")

message = response.choices[0].message

if message.tool_calls is None:
    print(response.choices[0].message.content)
else:
    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")
        result_message = call_function(tool_call)
        if not result_message['content']:
            raise Exception("Result message content is empty.")
        if args.verbose is True:
            print(f"-> {result_message['content']}")
