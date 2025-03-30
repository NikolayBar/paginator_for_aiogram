import asyncio
from loader import setup_bot
from logger import setup_logger

logger = setup_logger()

async def main():
    try:
        logger.info("Starting bot...")
        bot, dp = await setup_bot()
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot stopped with error: {e}")
    finally:
        logger.info("Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())