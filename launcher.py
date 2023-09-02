import os
import subprocess
from dotenv import load_dotenv as load
load()
k = subprocess.Popen(["python3", "client.py", str(os.getenv("TRIANGLE_KEY_LAUNCHER")), "watching", ".gg/trianglelabs", "a really chill human who loves helping others", "1071612146733039636", "1", ""])
input("press enter to stop bot...")
k.kill()