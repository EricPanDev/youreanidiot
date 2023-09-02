# dont delete lol

import trianglelabs
import aiohttp
import os
import requests
import discord
import time
from discord import Embed, app_commands
import datetime
from discord.ext import commands
from trianglelabs import generate_from_prompt, database, generate_bar, crop_quadrant, utils
from discord.ext.commands import cooldown, BucketType
from discord import ui, ButtonStyle
import random
from discord.ui import View, Button
def write_text_to_file(filename, text):
    if os.path.exists(filename):
        with open(filename, 'a') as file:
            file.write(text + '\n')
    else:
        with open(filename, 'w') as file:
            file.write(text + '\n')

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, custom_id="NTTS_Accept_ycvgbhkjn")
    async def accept_btn(self,interaction:discord.Interaction, button:discord.ui.Button):
        if os.path.exists("NTTS/accepted.txt"):
            with open("NTTS/accepted.txt", "a") as file:
                file.write(interaction.message.embeds[0].description)
                file.write("\n")
        else:
            with open("NTTS/accepted.txt", "w") as file:
                file.write(interaction.message.embeds[0].description)
                file.write("\n")
        await interaction.response.edit_message(content=f"Accepted by {interaction.user.mention}!", view=None)
    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red, custom_id="NTTS_Deny_ycvgbhkjn")
    async def deny_btn(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.edit_message(content=f"Denied by {interaction.user.mention}!", view=None)
            
class NTTSCog(commands.Cog):
    def __init__(self, bot: commands.Bot, owner):
        self.bot = bot
        self.client = bot
        self.owner = str(owner) or ""
        self.authorization_url = "https://discord.com/api/oauth2/authorize?client_id=" + str(bot.user.id) + "&permissions=139586718784&scope=applications.commands%20bot"
        
    @app_commands.command(name="suggesttopic",
        description="Suggest a topic for the bots to talk about!",
        )
    async def suggesttopic(self, interaction: discord.Interaction, topic: str):
        if interaction.guild_id in [1118816089569230911, 820745488231301210]:
            write_text_to_file("NTTS/suggestion_queue.txt", topic.replace("\n", ""))
            await interaction.response.send_message(embed=discord.Embed(
                title="Suggestion Sent!",
                color=discord.Color.blurple()
            ))
        channel = self.bot.get_guild(820745488231301210).get_channel(1123681892412182528)
        embed = Embed(
            title="Suggestion Received!",
            description=topic,
            color=discord.Color.blurple()
        )
        embed.set_footer(text=f"Suggested by {interaction.user.name} ({interaction.user.id})")
        await channel.send(embed=embed, view=Buttons())

async def setup(bot):
    await bot.add_cog(NTTSCog(bot))