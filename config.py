import os
from dotenv import load_dotenv

# بارگذاری از فایل .env
load_dotenv()

# خوندن توکن
TOKEN = os.getenv("TOKEN")

# چک کن که خالی نباشه
if not TOKEN:
    raise ValueError("TOKEN not found in .env file!")