import datetime

import discord
from discord import app_commands
from discord.ext import tasks

from commands import birthday_add, birthday_delete
from config import DISCORD_BOT_TOKEN, COMMAND_GUILD_IDS
from message import happy_birthday_message
from model import read_birthday_file


class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())

    async def setup_hook(self) -> None:
        self.birthday_monitor_task.start()

    @tasks.loop(time=[datetime.time(hour=hour, minute=0, second=0) for hour in range(0, 24)])
    #@tasks.loop(time=[datetime.time(hour=1, minute=min, second=0) for min in range(0, 60)])
    async def birthday_monitor_task(self):
        now = datetime.datetime.now()
        data = read_birthday_file()
        for discord_id in data.keys():
            birthday = data[discord_id]
            if (birthday["month"] == now.month and birthday["day"] == now.day and
                    birthday["notification_hour"] == now.hour):
                await happy_birthday_message(self, discord_id)

    @birthday_monitor_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))
        slash_command = app_commands.CommandTree(client)
        command = discord.app_commands.Command(name="add_birthday",
                                               description="Add your birthday to the bot",
                                               callback=birthday_add,
                                               guild_ids=COMMAND_GUILD_IDS)
        command.guild_only = True
        slash_command.add_command(command)

        command = discord.app_commands.Command(name="delete_birthday",
                                               description="Delete your birthday from the bot",
                                               callback=birthday_delete,
                                               guild_ids=COMMAND_GUILD_IDS)
        command.guild_only = True
        slash_command.add_command(command)
        for guild in COMMAND_GUILD_IDS:
            print(await slash_command.sync(guild=discord.Object(id=guild)))

client = MyClient()
client.run(DISCORD_BOT_TOKEN)