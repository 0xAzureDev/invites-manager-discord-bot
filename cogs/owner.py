import discord
from discord.ext import commands
from discord.ext.commands import Context
from helpers import checks


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @checks.is_owner()
    async def shutdown(self, context: Context) -> None:
        """
        Shuts down the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="Shutting down. Bye! :wave:",
            color=0x9C84EF
        )
        await context.send(embed=embed)
        await self.bot.close()

    @commands.hybrid_command(
        name="say",
        description="The bot will say anything you want.",
    )
    @checks.is_owner()
    async def say(self, context: Context, message: str) -> None:
        """
        The bot will say anything you want.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        await context.send(message)

async def setup(bot):
    await bot.add_cog(Owner(bot))
