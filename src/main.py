import nextcord
from nextcord.ext import commands

import subprocess

from tokens import API_KEY

TESTING_GUILD_ID = 1192706822415597568  # Replace with your guild ID

PERMITTED_IDS = [257989883707129859]  # for running the /terminal command

bot = commands.Bot()


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.slash_command(description='Run command in terminal', guild_ids=[TESTING_GUILD_ID])
async def terminal(interaction: nextcord.Interaction, command: str):
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


@bot.slash_command(description='Run command in Minecraft server (If it is up)', guild_ids=[TESTING_GUILD_ID], default_member_permissions=8)
async def minecraft(interaction: nextcord.Interaction, command: str):
    cmd = f'tmux send -t 0 "{command}" ENTER'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stderr:
        await interaction.send(f'**Error:** {result.stderr}')
    else:
        await interaction.send(f'Executed')


bot.run(API_KEY)
