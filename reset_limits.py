import time, os

while True:
    for i in os.listdir("database/limits"):
        if os.path.exists(f"database/limits/{i}/messages/usage"):
            os.remove(f"database/limits/{i}/messages/usage")
        if os.path.exists(f"database/limits/{i}/art/usage"):
            os.remove(f"database/limits/{i}/art/usage")
        if os.path.exists(f"database/limits/{i}/backstory/usage"):
            os.remove(f"database/limits/{i}/backstory/usage")
    time.sleep(86400)