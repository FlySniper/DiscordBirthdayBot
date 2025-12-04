from typing import Optional

import discord

from config import MESSAGE_CHANNEL


async def happy_birthday_message(client: discord.Client, discord_id: str, age: Optional[int]):
    embed = discord.embeds.Embed()
    embed.title = "Happy Birthday"
    if age is not None:
        embed.description = f"Happy Birthday! <@!{discord_id}> is now {age} years old!"
    else:
        embed.description = f"Happy Birthday <@!{discord_id}>!"
    embed.color = 0xFFD700
    channel = client.get_channel(MESSAGE_CHANNEL)
    if channel is not None:
        await channel.send(embed=embed)