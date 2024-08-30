import nextcord
from nextcord.ext import commands

from tokens import API_KEY

TESTING_GUILD_ID = 1192706822415597568  # Replace with your guild ID

PERMITTED_IDS = [257989883707129859]  # for running the /terminal command

bot = commands.Bot()


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.slash_command(description='Run command in terminal', guild_ids=[TESTING_GUILD_ID])
async def terminal(interaction: nextcord.Interaction):
    if interaction.user.id in PERMITTED_IDS:
        await interaction.send('Permitted!')
    else:
        await interaction.send('Not Permitted.')


bot.run(API_KEY)
