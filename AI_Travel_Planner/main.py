
import os
from pathlib import Path
from dotenv import load_dotenv

# Yeh project ke root folder tak ka absolute path nikaalega aur .env load karega
base_dir = Path(__file__).resolve().parent
env_path = base_dir / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"--- SUCCESS: Loaded .env from {env_path} ---")
else:
    # Agar root par nahi mili, toh check karega ek folder piche
    backup_env_path = base_dir.parent / ".env"
    load_dotenv(dotenv_path=backup_env_path)
    print(f"--- SUCCESS: Loaded backup .env from {backup_env_path} ---")

# Debugging ke liye check karte hain ki key load hui ya nahi
print("DEBUG: GOOGLE_API_KEY exists in env:", bool(os.getenv("GOOGLE_API_KEY")))  