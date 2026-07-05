import asyncio
import logging
import random

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from config import TOKEN

# ==================== تنظیمات ====================

bot_username: str = ""          # یوزرنیم بات بدون @ (برای ساخت لینک)
# ===================================================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.startup()
async def on_startup() -> None:
    global bot_username

    me = await bot.get_me()

    if not me.username:
        raise RuntimeError(
            "This bot has no @username. Set one via @BotFather."
        )

    bot_username = me.username
    logging.info("Resolved bot username: @%s", bot_username)

# دیکشنری نگهداری محتوا در حافظه:
#   کلید   -> کد رندومی که در انتهای لینک قرار می‌گیرد
#   مقدار  -> (chat_id پیام اصلی, message_id پیام اصلی)
content_store: dict[str, tuple[int, int]] = {}


def generate_unique_code() -> str:
    """یک کد رندوم تولید می‌کند که در content_store تکراری نباشد."""
    while True:
        code = str(random.randint(10**8, 10**9 - 1))  # عدد ۹ رقمی
        if code not in content_store:
            return code


@dp.message(CommandStart(deep_link=True))
async def handle_deep_link(message: Message, command: CommandObject) -> None:
    """
    وقتی کاربر روی لینک t.me/<bot>?start=<code> کلیک می‌کند،
    همین هندلر با /start <code> صدا زده می‌شود.
    """
    code = command.args
    stored = content_store.get(code)

    if stored is None:
        await message.answer("این لینک نامعتبره یا محتواش دیگه در دسترس نیست.")
        return

    source_chat_id, source_message_id = stored
    try:
        await bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=source_chat_id,
            message_id=source_message_id,
        )
    except TelegramBadRequest:
        # مثلاً پیام اصلی حذف شده یا بات دیگه به اون چت دسترسی نداره
        await message.answer("متأسفانه محتوای اصلی دیگه در دسترس نیست.")


@dp.message(CommandStart())
async def handle_plain_start(message: Message) -> None:
    """پاسخ به /start ساده (بدون کد)."""
    await message.answer(
        "سلام! هر چیزی برام بفرستی (متن، عکس، ویدیو، فایل و ...)، "
        "یه لینک اختصاصی بهت می‌دم که با فرستادنش برای هرکسی، "
        "همون محتوا رو دریافت می‌کنه."
    )


@dp.message()
async def handle_incoming_content(message: Message) -> None:
    """
    هندلر عمومی: چون بعد از هندلرهای بالا ثبت شده،
    فقط پیام‌هایی که /start نیستن به اینجا می‌رسن (متن، عکس، ویدیو، ویس، فایل، استیکر و ...).
    """
    code = generate_unique_code()
    content_store[code] = (message.chat.id, message.message_id)

    link = f"https://t.me/{bot_username}?start={code}"
    await message.answer(f"لینک اختصاصی محتوات آماده شد:\n{link}")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())