"""App config."""

import os
from dotenv import load_dotenv

load_dotenv()

# app
api_prefix = os.getenv("Avatar_MANAGEMENT_BASE_URL", default="/api/v1")
