# Persona Uploader Bot

A simple Telegram bot built with **aiogram 3** that allows users to share any Telegram message through a unique deep link.

Instead of forwarding messages manually, users can send any type of content to the bot. The bot generates a unique Telegram deep link, and anyone who opens that link receives a copy of the original message in their own chat with the bot.

---

## Overview

Persona Uploader Bot accepts virtually any Telegram content, including:

* Text messages
* Photos
* Videos
* Documents
* Audio
* Voice messages
* Stickers
* Animations
* And other supported Telegram message types

### How it works

1. A user sends any content to the bot.
2. The bot stores the message temporarily in memory.
3. The bot generates a unique deep link:

```
https://t.me/<bot_username>?start=<code>
```

4. The user shares the generated link.
5. When another user opens the link and starts the bot, the bot copies the original message to their chat.

---

# Prerequisites

Before running the project, make sure you have:

* Python **3.10+**
* A Telegram Bot Token from **@BotFather**
* Git (optional but recommended)

---

# Setup

Clone the repository:

```bash
git clone https://github.com/1Sohrab1/persona_uploader-bot.git
```

Move into the project directory:

```bash
cd persona_uploader-bot
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

> **Note**
>
> `requirements.txt` is introduced in **Issue #1**:
>
> **chore: add requirements.txt with pinned project dependencies**

---

# Configuration

Create a `.env` file in the project root.

Example:

```env
TOKEN=123456789:ABC-DEF1234567890abcdefghijklmnop
```

The bot reads the token from `.env` through `config.py`.

> **Important**
>
> Never commit your `.env` file.
>
> It contains your bot token and is already included in `.gitignore`.

---

# Run

Start the bot:

```bash
python main.py
```

If everything is configured correctly, the bot will begin polling Telegram for updates.

---

# Usage

### 1. Start the bot

Send:

```
/start
```

The bot responds with a welcome message.

### 2. Upload content

Send any supported Telegram message, for example:

* Text
* Photo
* Video
* File
* Voice message
* Sticker

The bot stores the content and replies with a unique shareable link.

Example:

```
https://t.me/<bot_username>?start=abc123xyz
```

### 3. Share the link

Send the generated link to anyone.

### 4. Receive the content

When another user opens the link and starts the bot, the original message is copied to their chat.

---

# Project Structure

```
persona_uploader-bot/
├── main.py            # Bot handlers and polling
├── config.py          # Loads TOKEN from .env
├── requirements.txt   # Project dependencies
├── .env               # Local secrets (not committed)
└── README.md
```

---

# Limitations

The current implementation has a few important limitations.

### In-memory storage

Uploaded content is stored in an in-memory dictionary (`content_store` in `main.py`).

As a result:

* All stored messages are lost when the bot restarts.
* Previously generated links become invalid after a restart.

For persistent storage, consider using a database such as SQLite, PostgreSQL, or Redis.

---

### Source message availability

The bot must still have access to the original message when it is copied.

If the source message becomes unavailable (for example, deleted or inaccessible), the bot may fail to deliver it.

---

### Hardcoded bot username

Currently, the bot username is hardcoded in `main.py` when generating deep links.

This will be improved in:

**Issue #3**

**refactor: resolve bot username dynamically via `bot.get_me()` on startup**

Once that change is merged, this README should be updated accordingly.

---

# Related Issues

* **#1** — Add `requirements.txt` with pinned project dependencies.
* **#3** — Resolve bot username dynamically using `bot.get_me()` on startup.

---

# Future Improvements

Possible future enhancements include:

* Persistent database storage
* Link expiration
* Admin panel
* Docker support
* Deployment guides (Railway, VPS, systemd, Docker Compose)
* Rate limiting
* Analytics for shared links

---

# License

This project is available under the MIT License unless stated otherwise.


