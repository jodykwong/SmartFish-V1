import os
# Must be set BEFORE eventlet is imported or monkey_patch is called
os.environ["EVENTLET_NO_GREENDNS"] = "yes"

import eventlet
eventlet.monkey_patch()

import httpx
from openai import OpenAI

def test_workaround():
    print("Testing with EVENTLET_NO_GREENDNS=yes...")
    try:
        # Test direct httpx
        with httpx.Client(http2=False) as client:
            resp = client.get("https://www.google.com", timeout=5)
            print(f"Direct httpx success! Status: {resp.status_code}")
            
        # Test OpenAI client
        api_key = os.getenv('REPORT_ENGINE_API_KEY')
        base_url = os.getenv('REPORT_ENGINE_BASE_URL')
        model = os.getenv('REPORT_ENGINE_MODEL_NAME')
        
        client = OpenAI(api_key=api_key, base_url=base_url)
        print("Calling OpenAI models.list()...")
        models = client.models.list()
        print("OpenAI success!")
        
    except Exception as e:
        print(f"FAILED with: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_workaround()
