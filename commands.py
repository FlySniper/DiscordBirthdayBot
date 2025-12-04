from typing import Optional

import discord
from discord import Interaction, app_commands

from model import append_to_birthday_file, remove_from_birthday_file, read_birthday_file


async def birthday_add(interaction: Interaction,
                       year:Optional[app_commands.Range[int, 0, 9999]],
                       month: app_commands.Range[int, 1, 12],
                       day: app_commands.Range[int, 1, 31],
                       notification_hour: app_commands.Range[int, 0, 23]):
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

async def birthday_get(interaction: Interaction):
    await interaction.response.defer()
    data = read_birthday_file()
    if str(interaction.user.id) not in data:
        embed = discord.embeds.Embed()
        embed.title = "No Birthday"
        embed.description = "Your birthday isn't registered with the bot."
        embed.color = 0xFF0000
        await interaction.followup.send(embed=embed)
        return
    birthday_data = data[str(interaction.user.id)]
    month = birthday_data.get("month", 1)
    day = birthday_data.get("day", 1)
    hour = birthday_data.get("notification_hour", 0)
    year = birthday_data.get("year", -1)
    embed = discord.embeds.Embed()
    embed.title = "Your Birthday"
    if year != -1:
        embed.description = f"<@!{interaction.user.id}>'s birthday is {month}/{day}/{year}-{hour}:00."
    else:
        embed.description = f"<@!{interaction.user.id}>'s birthday is {month}/{day}-{hour}:00."
    embed.color = 0xFF3EA5
    await interaction.followup.send(embed=embed)