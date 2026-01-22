import eventlet
eventlet.monkey_patch()
import httpx
import os

def test_httpx():
    print("Testing direct httpx call with eventlet...")
    try:
        # Test a simple GET request
        with httpx.Client(http2=False) as client:
            resp = client.get("https://www.google.com", timeout=5)
            print(f"Success! Status: {resp.status_code}")
            
        # Test DeepSeek specifically
        print("Testing DeepSeek models endpoint...")
        api_key = os.getenv('REPORT_ENGINE_API_KEY')
        headers = {"Authorization": f"Bearer {api_key}"}
        with httpx.Client(http2=False) as client:
            resp = client.get("https://api.deepseek.com/v1/models", headers=headers, timeout=10)
            print(f"Success! Status: {resp.status_code}")
            print(f"Response: {resp.text[:50]}...")
            
    except Exception as e:
        print(f"FAILED with: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_httpx()
