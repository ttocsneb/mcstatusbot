import logging
import discord
from discord.ext import commands
import mcstatus
import asyncio

from .config import config


def getPrefix(bot, message):
    prefixes = [config.prefix + ' ', config.prefix]
    prefixes += [i.capitalize() for i in prefixes]
    return prefixes + \
        commands.when_mentioned(bot, message)


bot = commands.Bot(command_prefix=getPrefix)
server = mcstatus.MinecraftServer(config.ip, config.port)

_logger = logging.getLogger(__name__)


async def update_status(online: bool, players: int, max_players: int):
    if online:
        await bot.change_presence(activity=discord.Activity(
            name="{} / {}".format(players, max_players),
            type=discord.ActivityType.watching
        ), status=discord.Status.online
                if players < max_players else discord.Status.idle)
    else:
        await bot.change_presence(status=discord.Status.dnd)


async def auto_status_update():
    while True:
        _logger.debug("Updating Status..")
        try:
            status = server.status()
            await update_status(True, status.players.online,
                                status.players.max)
        except Exception:
            await update_status(False, 0, 0)
        await asyncio.sleep(config.update)


@bot.event
async def on_ready():
    bot.loop.create_task(auto_status_update())
    print("I have logged in as {0.user}".format(bot))


@bot.command(aliases=["s"])
async def status(ctx):
    """
    Get the status of the server
    """
    with ctx.channel.typing():
        await asyncio.sleep(0.25)
        try:
            status = server.status()
            await update_status(True, status.players.online,
                                status.players.max)
        except Exception:
            await update_status(False, 0, 0)
            embed = discord.Embed(title=config.address, type="rich",
                                  colour=discord.Colour.gold())
            embed.add_field(name="Status", value="Offline")
            await ctx.channel.send("", embed=embed)
            return

        embed = discord.Embed(title=config.address, type="rich",
                              colour=discord.Colour.green())
        embed.add_field(name="Ping", value=round(status.latency))
        embed.add_field(
            name="Online",
            value="{st.players.online} / {st.players.max}".format(st=status)
        )
        if status.players.online > 0:
            embed.add_field(name="Players",
                            value="\n".join(
                                p.name for p in status.players.sample
                            ),
                            inline=True)

        await ctx.channel.send("", embed=embed)
