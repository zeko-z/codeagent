import os
import argparse
import json
from call_function import available_functions, call_function
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]


response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
    )

message = response.choices[0].message

def main() -> None:
    print("Hello from codeagent!")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
 
    if response.usage is None:
        raise RuntimeError("no usage")
    

    if api_key is None:
        raise RuntimeError("no api key")


    for tool_call in message.tool_calls:
        result_message = call_function(tool_call)
        
        if not result_message['content']:
            raise Exception("content missing")

        if args.verbose:
            print(f"-> {result_message['content']}")

        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")
    
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
