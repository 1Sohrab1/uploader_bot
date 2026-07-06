import os
from dotenv import load_dotenv

# بارگذاری از فایل .env
load_dotenv()

# خوندن توکن
TOKEN = os.getenv("TOKEN")

# چک کن که خالی نباشه
if not TOKEN:
    raise ValueError("TOKEN not found in .env file!")


VIDEO_DELETE_DELAY_SECONDS = int(
    os.getenv("VIDEO_DELETE_DELAY_SECONDS", "60")
)

if VIDEO_DELETE_DELAY_SECONDS <= 0:
    raise ValueError(
        "VIDEO_DELETE_DELAY_SECONDS must be a positive integer"
    )