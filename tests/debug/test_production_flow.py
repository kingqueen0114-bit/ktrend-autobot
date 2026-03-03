import os
from dotenv import load_dotenv

load_dotenv()

# We need to act like a Flask request for functions_framework
class DummyRequest:
    def __init__(self):
        self.is_json = False
        self.method = "POST"
        self.data = b""

    def get_json(self, silent=True):
        return {}

def run_production_test():
    try:
        from handlers.schedulers import trigger_daily_fetch
        
        print("🚀 Triggering the daily fetch pipeline locally to send LINE notification...")
        req = DummyRequest()
        response, status_code = trigger_daily_fetch(req)
        
        print(f"✅ Pipeline Finished!")
        print(f"Status: {status_code}")
        print(f"Response: {response}")
        
    except Exception as e:
        import traceback
        print("❌ CRASHED!")
        traceback.print_exc()

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = "AIzaSyDnssaqiBmzXI2I_3aupeU_N1Fgx0bB6tk"
    run_production_test()
