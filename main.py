import os
import argparse
import json
import sys
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

def main() -> None:
    print("Hello from codeagent!")
    
    for i in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            )
        
        message = response.choices[0].message
        messages.append(message)        

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
     
        if response.usage is None:
            raise RuntimeError("no usage")
        

        if api_key is None:
            raise RuntimeError("no api key")

        if message.tool_calls:
            for tool_call in message.tool_calls:
                
                result_message = call_function(tool_call, args.verbose)
                
                if not result_message['content']:
                    raise Exception("content missing")

                if args.verbose:
                    print(f"-> {result_message['content']}")

                messages.append(result_message)
        else:   
            print(response.choices[0].message.content)
            return

    print('Failed to produce a response in 20 iterations')
    sys.exit(1)

if __name__ == "__main__":
    main()
