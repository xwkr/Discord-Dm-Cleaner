#---IMPORTS---
import discord
from discord.ext import commands
import logging
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

#---LOAD CONFIGURATION---
with open('config.json') as config_file:
    config = json.load(config_file)

TOKEN = config["token"]
PREFIX = config["prefix"]

#---SETUP LOGGING---
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Custom logging formatter to add colors
class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, '')
        message = super().format(record)
        return f"{log_color}{message}{Style.RESET_ALL}"

# Apply the color formatter to the root logger
for handler in logging.root.handlers:
    handler.setFormatter(ColorFormatter(handler.formatter._fmt))

class SelfBot(commands.Bot):
    def __init__(self, command_prefix: str, token: str):
        super().__init__(command_prefix=command_prefix, self_bot=True)
        self.token = token
        self.remove_command("help")

    async def on_ready(self):
        logging.info("Ready! I await your command... (Use !clear in dm or channel)")
        logging.info(f"Name: {self.user.name}")
        logging.info(f"ID: {self.user.id}")

    async def clear_messages(self, ctx: commands.Context, limit: int = None):
        passed = 0
        failed = 0
        async for msg in ctx.message.channel.history(limit=limit):
            if msg.author.id == self.user.id:
                try:
                    await msg.delete()
                    passed += 1
                except Exception as e:
                    logging.error(f"Failed to delete message: {e}")
                    failed += 1
        logging.info(f"Removed {passed} messages with {failed} fails")

    def run_bot(self):
        try:
            logging.info("Logging into Discord")
            self.run(self.token, bot=False)
        except Exception as e:
            logging.error(f"Error logging into Discord: {e}")

if __name__ == "__main__":
    bot = SelfBot(command_prefix=PREFIX, token=TOKEN)

    @bot.command()
    async def clear(ctx: commands.Context, limit: int = None):
        await bot.clear_messages(ctx, limit)

    bot.run_bot()
