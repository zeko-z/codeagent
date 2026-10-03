import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        }
    ],
)

def main():
    print("Hello from codeagent!")
    print(f"User prompt: {response.choices[0]

    if respons.usage is None:
        print(f"Prompt tokens: {respone.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    else:
        raise RuntimeError("no usage")

    if api_key is None:
        raise RuntimeError("no api key")
    
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
