import eventlet
eventlet.monkey_patch()
import os
import httpx
from openai import OpenAI

def test_connection():
    api_key = os.getenv('REPORT_ENGINE_API_KEY')
    base_url = os.getenv('REPORT_ENGINE_BASE_URL')
    model = os.getenv('REPORT_ENGINE_MODEL_NAME')
    
    print(f"Testing connectivity with custom httpx client (corrected):")
    
    # In httpx 0.28+, use 'proxy' for a single proxy string or None to disable.
    # To disable all proxies, we can pass None or just not provide any.
    # Also explicitly disable http2.
    http_client = httpx.Client(
        http1=True,
        http2=False,
        proxy=None,
        timeout=30.0
    )
    
    client = OpenAI(api_key=api_key, base_url=base_url, http_client=http_client)
    
    try:
        print("Calling models.list()...")
        models = client.models.list()
        print("Success!")
        
        print("\nCalling chat.completions.create...")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hello"}],
        )
        print(f"Success! Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"\nFAILED with exception: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()
