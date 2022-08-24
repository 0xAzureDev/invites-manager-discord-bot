import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="invites",
        description="Check how many invites you have.",
    )
    async def invites(self, context: Context, user: discord.User = None) -> None:
        """
        Check how many invites you have.

        :param context: The hybrid command context.
        :param user: User to query for invites
        """

        match_user = (user if user else context.user)
        string_user = (user.display_name if user else context.author.display_name)

        totalInvites = 0
        for i in await context.guild.invites():
            if i.inviter == match_user:
                totalInvites += i.uses

        embed = discord.Embed(
            title="",
            description=f"**{string_user}** invited {totalInvites} member{'' if totalInvites == 1 else 's'} to the server!",
            color=0x0878FC
        )

        await context.send(embed=embed)


    @commands.hybrid_command(
        name="leaderboard",
        description="Returns the top invites leaderboard.",
    )
    async def leaderboard(self, context: Context) -> None:
        """
        Returns the top invites leaderboard.

        :param context: The hybrid command context.
        """

        inviters = []
        for i in await context.guild.invites():
            inviters.append({
                "user": f'{i.inviter.mention}',
                "uses": i.uses
            })

            # Give first 100 users a role for inviting 5 people
            role = get(context.guild.roles, name = "Beta")
            user_with_role = [m for m in context.guild.members if role in m.roles]

            if (i.uses >= 5 and len(user_with_role) <= 100):
                member = context.guild.get_member(i.inviter.id)
                if (member):
                    await member.add_roles(role)

        sorted_inviters = sorted(inviters, key=lambda d: d['uses'], reverse=True)

        desc_output = ''
        for index, inviter in enumerate(sorted_inviters):
            if (index != 0):
                desc_output += '\n'
            desc_output += f'`{index+1}. `{inviter["user"]} • {inviter["uses"]}'

        embed = discord.Embed(
            title="🏆 Invites Leaderboard",
            description=f"{desc_output}",
            color=0x0878FC
        )

        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
