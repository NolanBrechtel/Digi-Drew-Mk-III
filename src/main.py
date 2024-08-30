import nextcord
from nextcord.ext import commands

from tokens import API_KEY

TESTING_GUILD_ID = 1192706822415597568  # Replace with your guild ID

bot = commands.Bot()


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.slash_command(description="My first slash command", guild_ids=[TESTING_GUILD_ID])
async def hello(interaction: nextcord.Interaction):
    await interaction.send("Hello!")


bot.run(API_KEY)
