from typing import Optional

import discord
from discord import Interaction

from model import append_to_birthday_file, remove_from_birthday_file


async def birthday_add(interaction: Interaction,
                       year:Optional[int],
                       month: int,
                       day: int,
                       notification_hour: int):
    await interaction.response.defer()
    embed = discord.embeds.Embed()
    embed.title = "Birthday Added"
    if year is None:
        append_to_birthday_file({"month": month, "day": day, "notification_hour": notification_hour},
                                str(interaction.user.id))
        embed.description = (f"<@!{interaction.user.id}>'s birthday has been registered for "
                             f"{month}/{day}-{notification_hour}:00.")
    else:
        append_to_birthday_file({"year": year, "month": month, "day": day,
                                 "notification_hour": notification_hour}, str(interaction.user.id))
        embed.description = (f"<@!{interaction.user.id}>'s birthday has been registered for "
                             f"{month}/{day}/{year}-{notification_hour}:00.")
    embed.color = 0xFE1493
    await interaction.followup.send(embed=embed)


async def birthday_delete(interaction: Interaction):
    await interaction.response.defer()
    remove_from_birthday_file(str(interaction.user.id))
    embed = discord.embeds.Embed()
    embed.title = "Birthday Removed"
    embed.description = f"<@!{interaction.user.id}>'s birthday has been removed."
    embed.color = 0xFF0000
    await interaction.followup.send(embed=embed)