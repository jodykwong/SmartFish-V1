import sys
import os
import subprocess
import time
import requests
from pathlib import Path

# Add root to sys.path
root_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(root_dir)

from MindSpider.main import MindSpider
from ReportEngine.flask_interface import initialize_report_engine

def test_startup():
    print("=== Diagnostic Startup Test ===")
    
    # 1. Test MindSpider DB Init
    print("\n1. Testing MindSpider Database Initialization...")
    spider = MindSpider()
    # Mocking the log capture and output
    try:
        success = spider.initialize_database()
        print(f"MindSpider DB Init Success: {success}")
    except Exception as e:
        print(f"MindSpider DB Init Exception: {e}")

    # 2. Test Report Engine Init
    print("\n2. Testing Report Engine Initialization...")
    try:
        success = initialize_report_engine()
        print(f"Report Engine Init Success: {success}")
    except Exception as e:
        print(f"Report Engine Init Exception: {e}")

    # 3. Test Streamlit Apps (Check if ports are busy)
    print("\n3. Checking Streamlit Ports (8501, 8502, 8503)...")
    ports = [8501, 8502, 8503]
    for port in ports:
        try:
            res = requests.get(f"http://127.0.0.1:{port}/_stcore/health", timeout=2)
            print(f"Port {port} healthcheck: {res.status_code} {res.text}")
        except Exception as e:
            print(f"Port {port} is NOT reachable/running: {e}")

    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_startup()
