import sys
import subprocess
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "line-bot-sdk<3.0.0"], check=True, stdout=subprocess.DEVNULL)
    from linebot import LineBotApi
    try:
        api = LineBotApi(None)
        print("Success")
    except Exception as e:
        print(f"Exception: {type(e).__name__}: {e}")
except Exception as e:
    print(f"Failed to test: {e}")
