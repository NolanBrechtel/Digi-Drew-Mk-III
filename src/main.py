import nextcord
from nextcord import SlashOption, Forbidden
from nextcord.ext import commands
from nextcord.ext.commands import Bot

from values import API_KEY, TESTING_GUILD_ID, PERMITTED_IDS

import os

bot = commands.Bot()
cogsList = []


def loadCogs(bot: Bot):
    for file in os.listdir("./cogs"):
        if file.endswith('.py'):
            cogsList.append(file[:-3])
            print(f'Loading: {file[:-3]}')
            bot.load_extension(f'cogs.{file[:-3]}')
            print(f'Done!')


@bot.slash_command(description='Loads an unloaded cog', guild_ids=[TESTING_GUILD_ID])
async def loadcog(interaction: nextcord.Interaction, cog: str = SlashOption(name="cog", required=True,
                                                                            choices=cogsList)) -> None:
    """
    Loads the specified cog. All cogs are loaded upon starting the bot, so this command should only need to be used if
    the unloadcog command was used to unload a cog.

    :param interaction: Interaction
        The interaction object.
    :param cog: str
        The cog to be loaded. This is required
    :return: None
    """
    if interaction.user.id in PERMITTED_IDS:
        try:
            bot.load_extension(f'cogs.{cog}')
        except commands.ExtensionAlreadyLoaded:
            await interaction.send(f'{cog.title()} is already loaded.')
        except commands.ExtensionNotFound:
            await interaction.send(f'{cog.title()} is not a option.')
        else:
            await interaction.send(f'Loaded Cog: {cog.title()}')
            await bot.sync_application_commands(guild_id=TESTING_GUILD_ID)
    else:
        await interaction.send(f'Not Permitted')


@bot.slash_command(description='Unloads a loaded cog', guild_ids=[TESTING_GUILD_ID])
async def unloadcog(interaction: nextcord.Interaction, cog: str = SlashOption(name="cog", required=True,
                                                                              choices=cogsList)) -> None:
    """
    Unloads an already loaded Cog

    :param interaction: Interaction
        The interaction object
    :param cog: str
        The cog to be unloaded
    :return: None
    """
    if interaction.user.id in PERMITTED_IDS:
        try:
            bot.unload_extension(f'cogs.{cog}')
        except commands.ExtensionNotLoaded:
            await interaction.send(f'{cog.title()} is already unloaded.')
        except commands.ExtensionNotFound:
            await interaction.send(f'{cog.title()} is not a option.')
        else:
            await interaction.send(f'Unloaded Cog: {cog.title()}')
            await bot.sync_application_commands(guild_id=TESTING_GUILD_ID)
    else:
        await interaction.send(f'Not Permitted')


@bot.slash_command(description='Refreshes Slash commands.', guild_ids=[TESTING_GUILD_ID])
async def refreshslash(interaction: nextcord.Interaction) -> None:
    """
    Refreshes Slash commands. Needs to be used when loading a cog.

    :param interaction: Interaction
        The interaction object
    :return: None
    """
    try:
        await bot.sync_application_commands(guild_id=TESTING_GUILD_ID)
        await interaction.send('Slash commands refreshed!')
    except Forbidden:
        await interaction.send('An error has occurred.')


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


loadCogs(bot)
bot.run(API_KEY)
