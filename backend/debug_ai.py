import asyncio
import os
import requests
import httpx
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load env vars
load_dotenv()

api_key = os.getenv("LLM_API_KEY")
base_url = os.getenv("LLM_BASE_URL")
model = os.getenv("LLM_MODEL")

print(f"Testing with requests (trust_env=False)...")
try:
    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 10
    }
    
    session = requests.Session()
    session.trust_env = False  # Disable system proxy
    
    print(f"POST {url}")
    resp = session.post(url, json=data, headers=headers, timeout=10)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print("Response:", resp.json()['choices'][0]['message']['content'])
    else:
        print("Error:", resp.text)
except Exception as e:
    print(f"Requests failed: {e}")

print(f"\nTesting with OpenAI SDK (trust_env=False)...")
async def test_chat():
    try:
        # Create custom httpx client ignoring system proxy
        http_client = httpx.AsyncClient(trust_env=False)
        
        client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
            http_client=http_client
        )
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Hello, are you there?"}
            ]
        )
        print("SDK Success!")
        print("Response:", response.choices[0].message.content)
    except Exception as e:
        print(f"SDK Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_chat())
