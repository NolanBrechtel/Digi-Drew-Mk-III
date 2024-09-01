import nextcord
from nextcord import SlashOption
from nextcord.ext import commands
from nextcord.ext.commands import Bot

from src.values import TESTING_GUILD_ID, PERMITTED_IDS, MC_RCON_PORT, MC_RCON_PASS, PATH_TO_MCSERVER

import subprocess


class Server(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.isServerOn = True

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

    @nextcord.slash_command(description='Start or stop the minecraft server.', guild_ids=[TESTING_GUILD_ID], default_member_permissions=8)
    async def minecraft(self, interaction: nextcord.Interaction) -> None:
        if self.isServerOn:
            await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name='for the server.'))

        else:
            await self.bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name='over the server.'))
            subprocess.run(PATH_TO_MCSERVER, shell=True, capture_output=True, text=True)
            await interaction.send('Starting the server.')

    @nextcord.slash_command(description='Remotely runs a command on the minecraft server.', guild_ids=[TESTING_GUILD_ID], default_member_permissions=8)
    async def command(self, interaction: nextcord.Interaction, command: str) -> None:
        subprocess.run(['./rcon', '-a', MC_RCON_PORT, '-p', MC_RCON_PASS, f'"{command}"'], shell=True, capture_output=True, text=True)


def setup(bot: Bot) -> None:
    bot.add_cog(Server(bot))
