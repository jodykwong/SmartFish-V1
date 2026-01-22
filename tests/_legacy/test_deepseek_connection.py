import os
import sys
from dotenv import load_dotenv

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(project_root)

from QueryEngine.llms.base import LLMClient

def test_deepseek():
    load_dotenv()
    
    api_key = os.getenv("QUERY_ENGINE_API_KEY")
    base_url = os.getenv("QUERY_ENGINE_BASE_URL")
    model_name = os.getenv("QUERY_ENGINE_MODEL_NAME")
    
    print(f"Testing DeepSeek connection...")
    print(f"Model: {model_name}")
    print(f"Base URL: {base_url}")
    
    if not api_key:
        print("Error: QUERY_ENGINE_API_KEY not found in .env")
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
            print("\nVerification: DeepSeek interface is NORMAL.")
        else:
            print("\nVerification: DeepSeek interface returned unexpected response.")
            
    except Exception as e:
        print(f"\nVerification: DeepSeek interface ERROR: {e}")

if __name__ == "__main__":
    test_deepseek()
