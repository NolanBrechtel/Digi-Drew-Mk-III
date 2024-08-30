import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Bot

from src.values import TESTING_GUILD_ID, PERMITTED_IDS

import subprocess


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description='Run command in terminal', guild_ids=[TESTING_GUILD_ID])
    async def terminal(self, interaction: nextcord.Interaction, command: str) -> None:
        if interaction.user.id in PERMITTED_IDS:
            cmd = command.split(' ')
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.stdout:
                output = f'**Running:**\n```> {command}```\n**Output:**\n```{result.stdout}```'
            else:
                output = f'**Running:**\n```> {command}```\n**Error:**```{result.stderr}```'
            await interaction.send(output)
        else:
            await interaction.send(f'Not Permitted.')


def setup(bot: Bot) -> None:
    bot.add_cog(Server(bot))
