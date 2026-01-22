import os
import sys
from dotenv import load_dotenv

# Add project root to path to import LLMClient
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(project_root)

from MediaEngine.llms.base import LLMClient

def test_gemini():
    load_dotenv()
    
    api_key = os.getenv("MEDIA_ENGINE_API_KEY")
    base_url = os.getenv("MEDIA_ENGINE_BASE_URL")
    model_name = os.getenv("MEDIA_ENGINE_MODEL_NAME", "gemini-2.5-pro")
    
    print(f"Testing Gemini connection...")
    print(f"Model: {model_name}")
    print(f"Base URL: {base_url}")
    
    if not api_key:
        print("Error: MEDIA_ENGINE_API_KEY not found in .env")
        return
        
    try:
        client = LLMClient(api_key=api_key, model_name=model_name, base_url=base_url)
        print("Client initialized. Sending test message...")
        
        response = client.invoke(
            system_prompt="You are a helpful assistant.",
            user_prompt="Hello, this is a connection test. Please reply with 'SUCCESS' if you receive this message.",
            temperature=0.0
        )
        
        print(f"Response: {response}")
        if "SUCCESS" in response.upper():
            print("\nVerification: Gemini interface is NORMAL.")
        else:
            print("\nVerification: Gemini interface returned unexpected response.")
            
    except Exception as e:
        print(f"\nVerification: Gemini interface ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini()
