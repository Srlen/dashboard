
from discord.abc import *
from bot import MainBot
from errors import *


async def get_guild(bot: MainBot, guild_id: Snowflake):
    if not isinstance(guild_id, Snowflake):
        raise NotGuildId("guild id not found")
    guild = await bot.prisma.guild.find_unique({"id": guild_id})
    return guild


async def get_channel(bot: MainBot, channel_id: Snowflake):
    if not isinstance(channel_id, Snowflake):
        raise NotChannelId("channel id not found")
    channel = await bot.prisma.channel.find_unique({"id": channel_id})
    return channel
