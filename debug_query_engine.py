import sys
import os
from loguru import logger
from dotenv import load_dotenv
load_dotenv()
from QueryEngine.agent import create_agent

# Configure logging to stdout
logger.remove()
logger.add(sys.stdout, level="DEBUG")

try:
    print("Initializing Agent...")
    agent = create_agent()
    print("Agent initialized. Starting research...")
    report = agent.research("aespa", save_report=True)
    print("Research complete.")
    if report:
        print("Report generated successfully length:", len(report))
    else:
        print("Report is empty.")
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
