import os
from dotenv import load_dotenv

load_dotenv()

MODE = os.getenv("ENVIRONMENT", "dev").lower()

BACKEND_URL = os.getenv(f"BACKEND_URL_{MODE.upper()}")
FRONTEND_URL = os.getenv(f"FRONTEND_URL_{MODE.upper()}")
GOOGLE_CLIENT_ID = os.getenv(f"GOOGLE_CLIENT_ID_{MODE.upper()}")
GOOGLE_CLIENT_SECRET = os.getenv(f"GOOGLE_CLIENT_SECRET_{MODE.upper()}")

ENVIRONMENT = MODE  # optional alias
