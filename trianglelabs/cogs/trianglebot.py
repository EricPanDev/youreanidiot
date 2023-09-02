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
from discord import ui
import random

timemodule = time
startTime=time.time()

class Bot_Info:
    client = None
    id = None

class Edit_Backstory(ui.Modal, title="Editing Backstory"):
    personality = ui.TextInput(
        label="Bot's Personality",
        placeholder="Enter a backstory...",
        style=discord.TextStyle.long,
        min_length=100,
        required=True,
    )
    # On Submit
    async def on_submit(self, interaction: discord.Interaction):
        is_unsafe = await utils.Moderation.is_flagged_message(self.personality.value)
        if is_unsafe:
            await interaction.response.send_message(
                ephemeral=True,
                content="Sorry but we can't allow you to have a backstory like that!\nPlease try something else!"
            )
        new_backstory = self.personality.value
        with open(f"database/client_launchers/{Bot_Info.id}/personality", "w") as store_file: store_file.write(new_backstory); store_file.close()
        await interaction.response.send_message("Backstory has been updated!")

class Edit_Stream_Link(ui.Modal, title="Editing Stream Link"):
    personality = ui.TextInput(
        label="Enter a Stream Link",
        placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        style=discord.TextStyle.short,
        required=True,
    )
    # On Submit
    async def on_submit(self, interaction: discord.Interaction):
        new_backstory = self.personality.value
        with open(f"database/client_launchers/{Bot_Info.id}/stream_link", "w") as store_file: store_file.write(new_backstory); store_file.close()
        await interaction.response.send_message("Stream Link has been updated!")

class Edit_Status_Type(ui.Modal, title="Editing Status Type"):
    personality = ui.TextInput(
        label="Bot's Status Type",
        placeholder="playing/watching/listening/streaming/competing",
        style=discord.TextStyle.short,
        required=True,
    )
    # On Submit
    async def on_submit(self, interaction: discord.Interaction):
        new_backstory = self.personality.value
        with open(f"database/client_launchers/{Bot_Info.id}/status", "w") as store_file: store_file.write(new_backstory); store_file.close()
        await interaction.response.send_message("Status Type has been updated!")
        original_status = open(f"database/client_launchers/{Bot_Info.id}/text").read()
        await utils.parse_presence(Bot_Info.client, new_backstory, original_status)

class Edit_Status_Text(ui.Modal, title="Editing Status Text"):
    personality = ui.TextInput(
        label="Bot's Status Text",
        placeholder="my DMs",
        style=discord.TextStyle.short,
        required=True,
    )
    # On Submit
    async def on_submit(self, interaction: discord.Interaction):
        new_backstory = self.personality.value
        with open(f"database/client_launchers/{Bot_Info.id}/text", "w") as store_file: store_file.write(new_backstory); store_file.close()
        await interaction.response.send_message("Status Text has been updated!")
        original_status = open(f"database/client_launchers/{Bot_Info.id}/status").read()
        await utils.parse_presence(Bot_Info.client, original_status, new_backstory)

class MainCog(commands.Cog):
    def __init__(self, bot: commands.Bot, owner):
        self.bot = bot
        self.client = bot
        self.owner = str(owner) or ""
        self.authorization_url = "https://discord.com/api/oauth2/authorize?client_id=" + str(bot.user.id) + "&permissions=139586718784&scope=applications.commands%20bot"
        
    @commands.hybrid_command(name="about", description="About the Bot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def about(self, ctx):
        if ctx.guild:
            shard_info = f"Shard ID: {str((ctx.guild.id >> 22) % 2)}"
        else:
            shard_info = ""
        embed = Embed(
            title=f"{self.bot.user.name} • About",
            description=f"Help Command: /help\n{shard_info}\nUptime: {datetime.timedelta(seconds=int(round(time.time()-startTime)))}\nSupport: https://discord.gg/trianglelabs",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        embed.set_footer(text="Powered by TriangleLabs • v3.0.2")
        view = discord.ui.View()
        join_guild = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Support Server", url="https://discord.gg/trianglelabs")
        add_to_guild = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Invite Bot", url=self.authorization_url)
        view.add_item(item=join_guild)
        view.add_item(item=add_to_guild)
        await ctx.reply(embed=embed, view=view)

    @commands.command(name="setmessagelimit", description="Set a message limit for the bot")
    async def setmessagelimit(self, ctx, user, limit):
        if ctx.author.id == 746446670228619414:
            database.set_message_limit(user, limit)
        

    @commands.hybrid_command(name="ping", description="Get the Latency of the Bot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        embed = Embed(
            title="📡 Latency",
            description="Latency: %sms" % str(round(self.bot.latency*100000) / 100),
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        if ctx.guild:
            embed.set_footer(text="Shard %s" % ((ctx.guild.id >> 22) % 2))
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="usage", description="View your remaining daily quota.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def usage(self, ctx):
        message_limit, art_limit, gen_limit = database.get_limits(ctx.author.id)
        message_used, art_used, gen_used = database.get_usage(ctx.author.id)
        message_limit, art_limit, message_used, art_used = int(message_limit), int(art_limit), int(message_used), int(art_used)
        gen_used, gen_limit = int(gen_used), int(gen_limit)
        embed = Embed(
            title="Daily Quota",
            description=f"Daily Quota for {ctx.author.mention}\n\n{message_used}/{message_limit} Messages ({round((message_used/message_limit)*100)}%)\n[ {generate_bar(message_used/message_limit)} ]\n\n{art_used}/{art_limit} Art Generation ({round((art_used/art_limit)*100)}%)\n[ {generate_bar(art_used/art_limit)} ]\n\n{art_used}/{art_limit} Backstory Generation ({round((gen_used/gen_limit)*100)}%)\n[ {generate_bar(gen_used/gen_limit)} ]",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        if ctx.guild:
            embed.set_footer(text="Shard %s" % ((ctx.guild.id >> 22) % 2))
        await ctx.reply(embed=embed)

    @app_commands.command(
        name="generate_art",
        description="Generate Art Using AI"
    )
    @app_commands.choices(
        style=[
            app_commands.Choice(name='Cute Animal', value='cute-creature-generator'),
            app_commands.Choice(name='Fantasy World', value='fantasy-world-generator'),
            app_commands.Choice(name='Cyberpunk', value='cyberpunk-generator'),
            app_commands.Choice(name='Anime Portrait', value='anime-portrait-generator'),
            app_commands.Choice(name='3D Objects', value='3d-objects-generator'),
            app_commands.Choice(name='3D Origami', value='origami-3d-generator'),
            app_commands.Choice(name='3D Hologram', value='hologram-3d-generator'),
            app_commands.Choice(name='3D Character', value='3d-character-generator'),
            app_commands.Choice(name='Watercolor', value='watercolor-painting-generator'),
            app_commands.Choice(name='Pop Art', value='pop-art-generator'),
            app_commands.Choice(name='Architecture', value='contemporary-architecture-generator'),
            app_commands.Choice(name='Futuristic Architecture', value='future-architecture-generator'),
            app_commands.Choice(name='Watercolor Architecture', value='watercolor-architecture-generator'),
            app_commands.Choice(name='Fantasy Character', value='fantasy-character-generator'),
            app_commands.Choice(name='Steampunk', value='steampunk-generator'),
            app_commands.Choice(name='Pixel Art', value='pixel-art-generator'),
            app_commands.Choice(name='Street Art', value='street-art-generator'),
            app_commands.Choice(name='Surreal Portrait', value='surreal-portrait-generator'),
            app_commands.Choice(name='Anime World', value='anime-world-generator'),
            app_commands.Choice(name='Fantasy Portrait', value='fantasy-portrait-generator'),
            app_commands.Choice(name='Comic Protrait', value='comics-portrait-generator'),
            app_commands.Choice(name='Cyberpunk Portrait', value='cyberpunk-portrait-generator'),
        ]
    )
    async def generate_art(self, interaction: discord.Interaction, prompt: str, style: app_commands.Choice[str] = "default", negative_prompt:str=""):
        if not database.is_art_limited(interaction.user.id):
            is_flagged = await utils.Moderation.is_flagged_message(prompt)
            if not is_flagged:
                database.log_art(interaction.user.id)
                await interaction.response.send_message(embed=discord.Embed(title="Generating...", color=discord.Color.blurple()))
                message = await interaction.original_response()
                try:
                    image_url = await generate_from_prompt(prompt, style=(style.value if style != "default" else "default"), negative_prompt=negative_prompt)
                    embed=discord.Embed(title="Image Generation Result", url=image_url, color=discord.Color.blurple())
                    embed.set_footer(text=f"Requested by {interaction.user.name} ({interaction.user.id})")
                    embed.set_image(url=image_url)
                    view = discord.ui.View()
                    one = discord.ui.Button(style=discord.ButtonStyle.blurple, label="1", custom_id="one")
                    two = discord.ui.Button(style=discord.ButtonStyle.blurple, label="2", custom_id="two")
                    three = discord.ui.Button(style=discord.ButtonStyle.blurple, label="3", custom_id="three")
                    four = discord.ui.Button(style=discord.ButtonStyle.blurple, label="4", custom_id="four")
                    async def crop(interaction: discord.Interaction, quadrant):
                        if str(interaction.user.id) == interaction.message.embeds[0].footer.text[:-1][::-1].split("(", 1)[0][::-1]:
                            await interaction.message.edit(view=discord.ui.View())
                            embed = interaction.message.embeds[0]
                            result = crop_quadrant(embed.image.url,quadrant)
                            file = discord.File(os.getcwd() + "/" + result, filename='image.png')
                            msg = await interaction.channel.send(file=file, content='Processing...', reference=interaction.message, mention_author=False)
                            url = msg.attachments[0].url
                            await msg.delete()
                            embed.set_image(url=url)
                            await interaction.message.edit(embed=embed)
                            os.remove(result)
                        else:
                            await interaction.response.send_message("That is not your interaction!", ephemeral=True)
                except:
                    message = await interaction.original_response()
                    await message.edit(embed=discord.Embed(color=discord.Color.red(), title="Error", description="Image Generation is either unavaliable, or you made a inappropriate request"))
            else:
                await interaction.response.send_message("I refuse to generate art of inappropriate requests.")
        else:
            await interaction.response.send_message("You have used all of your daily quota!")
            

        async def crop_quadrant_one(interaction: discord.Interaction):
            await crop(interaction,1)
        async def crop_quadrant_two(interaction):
            await crop(interaction,2)
        async def crop_quadrant_three(interaction):
            await crop(interaction,3)
        async def crop_quadrant_four(interaction):
            await crop(interaction,4)

        one.callback = crop_quadrant_one
        two.callback = crop_quadrant_two
        three.callback = crop_quadrant_three
        four.callback = crop_quadrant_four
        view.add_item(item=one)
        view.add_item(item=two)
        view.add_item(item=three)
        view.add_item(item=four)
        await message.edit(embed = embed, view=view)
    
    @app_commands.command(
        name="edit_image",
        description="Edit a Image via a text prompt using AI"
    )
    async def edit_image(self, interaction: discord.Interaction, prompt:str, file: discord.Attachment):
        if not database.is_art_limited(interaction.user.id):
            database.log_art(interaction.user.id)
            is_flagged = await utils.Moderation.is_flagged_message(prompt)
            if not is_flagged:
                await interaction.response.send_message("Generating... (ETA: 20s)")
                try:
                    headers = {
                        'api-key': os.getenv("DEEPAI_API_KEY"),
                    }

                    num = random.randint(0,100000)
                    await file.save(str(num) + ".png")

                    files = {
                        'image': open(str(num) + ".png", "rb").read(),
                        'text': bytes(prompt, "utf-8"),
                    }

                    os.remove(str(num) + ".png")

                    response = requests.post('https://api.deepai.org/api/image-editor', headers=headers, files=files).json()['output_url']
                    message = await interaction.original_response()
                    embed = discord.Embed(title="Image Edit Result", color=discord.Color.blurple())
                    embed.set_image(url=response)
                    await message.edit(content="", embed=embed)
                except Exception as Error:
                    print(Error)
                    message = await interaction.original_response()
                    await message.edit(content="", embed=discord.Embed(title="Something Went Wrong", description="Image Editing is either unavaliable or you made a naughty request.", color=discord.Color.red()))
            else:
                await interaction.response.send_message("I refuse to generate inappropriate edits.")
        else:
            await interaction.response.send_message("You have used all of your daily quota!")


    @app_commands.command(
        name="stable_diffusion",
        description="Use Stable Diffusion to generate art"
    )
    async def stable_diffusion(self, interaction: discord.Interaction, prompt:str, negative_prompt:str=""):
        if not database.is_art_limited(interaction.user.id):
            database.log_art(interaction.user.id)
            is_flagged = await utils.Moderation.is_flagged_message(prompt)
            if not is_flagged:
                await interaction.response.send_message("Generating... (ETA: 20s)")
                try:
                    headers = {
                        'api-key': os.getenv("DEEPAI_API_KEY"),
                    }

                    files = {
                        'text': bytes(prompt, "utf-8"),
                        "grid_size": bytes("1","utf-8"),
                        "width": bytes("850", "utf-8"),
                        "height": bytes("610", "utf-8")
                    }

                    if negative_prompt != "":
                        files["negative_prompt"] = bytes(negative_prompt,"utf-8")

                    response = requests.post('https://api.deepai.org/api/stable-diffusion', headers=headers, files=files).json()['output_url']
                    message = await interaction.original_response()
                    embed = discord.Embed(title="Stable Diffusion Result", color=discord.Color.blurple())
                    embed.set_image(url=response)
                    await message.edit(content="", embed=embed)
                except Exception as Error:
                    print(Error)
                    message = await interaction.original_response()
                    await message.edit(content="", embed=discord.Embed(title="Something Went Wrong", description="Image Editing is either unavaliable or you made a naughty request.", color=discord.Color.red()))
            else:
                await interaction.response.send_message("I refuse to generate inappropriate edits.")
        else:
            await interaction.response.send_message("You have used all of your daily quota!")

    @commands.hybrid_command(name="enable", description="Enable this bot in the current channel.", aliases=["activate"])
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def enable(self, ctx):
        database.enable_channel(ctx.channel.id, self.bot.user.id)
        await ctx.reply(f"{self.bot.user.name} has been activated in this channel.\nUse /disable to deactivate this bot.")

    @commands.hybrid_command(name="disable", description="Disable this bot in the current channel.", aliases=["deactivate"])
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def disable(self, ctx):
        database.disable_channel(ctx.channel.id, self.bot.user.id)
        await ctx.reply(f"{self.bot.user.name} has been deactivated in this channel.\nUse /enable to re-enable the bot.")

    @commands.hybrid_command(name="wack", description="Reset Conversation History with the bot", aliases=["reset"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wack(self, ctx):
        database.clear_channel(self.bot.user.id, ctx.channel.id, ctx.author.id)
        await ctx.reply(f"oww my head hurts...")

    @app_commands.command(name="roleplay", description="Allows the bot to add actions inside italics")
    @app_commands.choices(
        mode=[
            app_commands.Choice(name='Enabled', value='enable'),
            app_commands.Choice(name='Disabled', value='disable'),
        ]
    )
    async def roleplay(self, interaction: discord.Interaction, mode: app_commands.Choice[str]):
        if mode.value == "enable":
            database.enable_roleplay(self.bot.user.id, interaction.user.id)
            return await interaction.response.send_message(f"Roleplay Mode Enabled!")
        elif mode.value == "disable":
            database.disable_roleplay(self.bot.user.id, interaction.user.id)
            return await interaction.response.send_message(f"Roleplay Mode Disabled!")
        await interaction.response.send_message("I don't know how you triggered this message but hi i guess - devs")

    @app_commands.command(name="webhook", description="Set a webhook for the bot to use")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @app_commands.choices(
        mode=[
            app_commands.Choice(name='Enabled', value='enable'),
            app_commands.Choice(name='Disabled (Default)', value='disable'),
        ]
    )
    async def set_webhook(self, interaction: discord.Interaction, mode: app_commands.Choice[str], url: str = ""):
        if interaction.user.guild_permissions.manage_guild or interaction.user.id in ["746446670228619414"]:
            if mode.value == "enable":
                if "url" == "":
                    await interaction.response.send_message("Missing required `url` paramater!", ephemeral=True)
                    return
                database.enable_webhook(self.bot.user.id, interaction.channel.id, url)
                return await interaction.response.send_message(f"Webhook Set!", ephemeral=True)
            elif mode.value == "disable":
                database.disable_webhook(self.bot.user.id, interaction.channel.id)
                return await interaction.response.send_message(f"Webhook Disabled!", ephemeral=True)
        else:
            await interaction.response.send_message("Missing Permissions!", ephemeral=True)

    @app_commands.command(name="memory", description="[CREATOR ONLY] Add Memories to the bot")
    @app_commands.choices(
        choice=[
            app_commands.Choice(name='Remember', value='remember'),
            app_commands.Choice(name='Forget', value='forget'),
            app_commands.Choice(name='List All', value='list')
        ]
    )
    async def memory(self, interaction: discord.Interaction, choice: app_commands.Choice[str], data:str = None):
        if str(interaction.user.id) in ["746446670228619414", str(self.owner)]:
            if choice.value == "remember":
                if data == None:
                    return await interaction.response.send_message("You need to add the text to remember in the `data` paramater!", ephemeral=True)
                database.add_memory(self.bot.user.id, data)
                await interaction.response.send_message("Memory Added!", ephemeral=True)
            elif choice.value == "forget":
                if data == None:
                    return await interaction.response.send_message("You need to add the number of the ID to forget!", ephemeral=True)
                database.remove_memory(self.bot.user.id, data)
                await interaction.response.send_message("Memory Removed!", ephemeral=True)
            elif choice.value == "list":
                memories = database.memories(self.bot.user.id)
                wrapped = ""
                for i in range(len(memories)):
                    wrapped += f"{i+1}. {memories[i]}\n"
                if wrapped=="": wrapped = "Bot has no memories set!"
                await interaction.response.send_message(f"**Bot Memories**\n```{wrapped}```", ephemeral=True)
        elif self.owner in [None, ""]:
            await interaction.response.send_message("This shape has no registered owner. If this is your shape, create a ticket at discord.gg/trianglelabs .", ephemeral=True)
        else:
            await interaction.response.send_message("This isn't your shape! You can make your own at discord.gg/trianglelabs tho :)", ephemeral=True)

    @app_commands.command(name="language", description="Change the Language the Bot Speaks to you")
    @app_commands.choices(
        language=[
            app_commands.Choice(name='Afrikaans (Afrikaans)', value='af'),
            app_commands.Choice(name='Bulgarian (Български)', value='bg'),
            app_commands.Choice(name='Czech (Čeština)', value='cs'),
            app_commands.Choice(name='Welsh (Cymreig)', value='cy'),
            app_commands.Choice(name='Danish (Dansk)', value='da'),
            app_commands.Choice(name='German (Deutsch)', value='de'),
            app_commands.Choice(name='Greek (Ελληνικά)', value='el'),
            app_commands.Choice(name='English (English)', value='en'),
            app_commands.Choice(name='Spanish (Español)', value='es'),
            app_commands.Choice(name='Finnish (Suomi)', value='fi'),
            app_commands.Choice(name='French (Français)', value='fr'),
            app_commands.Choice(name='Irish (Gaeilge)', value='ga'),
            app_commands.Choice(name='Hebrew (עברית)', value='he'),
            app_commands.Choice(name='Hindi (नहीं)', value='hi'),
            app_commands.Choice(name='Turkish (Türkçe)', value='tr'),
            app_commands.Choice(name='Korean (한국어)', value='ko'),
            app_commands.Choice(name='Dutch (Nederlands)', value='nl'),
            app_commands.Choice(name='Portuguese (Português)', value='pt'),
            app_commands.Choice(name='Russian (Русский)', value='ru'),
            app_commands.Choice(name='Slovak (Slovenčina)', value='sk'),
            app_commands.Choice(name='Swedish (Svenska)', value='sv'),
            app_commands.Choice(name='Ukrainian (Українська)', value='uk'),
            app_commands.Choice(name='Vietnamese (Tiếng Việt)', value='vi'),
            app_commands.Choice(name='Simplified Chinese (简体中文)', value='zh-Hans'),
            app_commands.Choice(name='Traditional Chinese (繁體中文)', value='zh-Hant'),
    ])
    async def set_language(self, interaction: discord.Interaction, language: app_commands.Choice[str]):
        database.set_language(interaction.user.id, language.value)
        await interaction.response.send_message(f"Language set to {language.name}!")

    @app_commands.command(name="typing_style", description="ChAnGe ThE tYpInG sTyLe Of ThE bOt")
    @app_commands.choices(
        style=[
            app_commands.Choice(name='All lowercase', value='lower'),
            app_commands.Choice(name='All UPPERCASE', value='upper'),
            app_commands.Choice(name='End messages with text', value='custom'),
            app_commands.Choice(name='None (Default)', value='none'),
    ])
    async def set_typing_style(self, interaction: discord.Interaction, style: app_commands.Choice[str], end_with: str=""):
        if style.value == "custom":
            if end_with != "":
                database.set_typing_style(interaction.user.id, end_with)
                return await interaction.response.send_message(f"Bot will now end all messages with {end_with}!")
            else:
                return await interaction.response.send_message(f"Missing required `end_with` paramater!")
        database.set_typing_style(interaction.user.id, style.value)
        await interaction.response.send_message(f"Typing style set to {style.name}!")


    @app_commands.command(name="update", description="[CREATOR ONLY] Edit this bot")
    @app_commands.choices(
        mode=[
            app_commands.Choice(name='Backstory', value='personality'),
            app_commands.Choice(name='Status Type', value='status_type'),
            app_commands.Choice(name='Status Text', value='status_text'),
            app_commands.Choice(name='Streaming Link (Optional)', value='link'),
            app_commands.Choice(name='Profile Picture', value='pfp'),
    ])
    async def edit_shape(self, interaction: discord.Interaction, mode: app_commands.Choice[str], image_url:str = "", image_file: discord.Attachment = None):
        if not str(interaction.user.id) in ["746446670228619414", str(self.owner)]:
            return await interaction.response.send_message("You don't own this bot!\nYou can make your own at discord.gg/trianglelabs though :>", ephemeral=True)
        Bot_Info.id = self.client.user.id
        Bot_Info.client = self.client
        data = image_file or image_url
        if mode.value == "pfp":
            if data != "":
                if image_file != None:
                    data = await image_file.read()
                    await self.client.user.edit(avatar=data)
                    await interaction.response.send_message('Profile Picture has been Updated!')
                else:
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(image_url) as resp:
                                if resp.status != 200:
                                    return await interaction.response.send_message('Failed to download image...')
                                data = await resp.read()

                        await self.client.user.edit(avatar=data)
                        await interaction.response.send_message('Profile Picture has been Updated!')
                    except Exception as e:
                        await interaction.response.send_message(f'An error occurred: {str(e)}')
                    else:
                        await interaction.response.send_message("You need to specify the `image_url` paramater!")
        if mode.value == "personality":
            file = f"database/client_launchers/{self.client.user.id}/personality"
            Modal = Edit_Backstory()
            Modal.personality.default = open(file).read()
            await interaction.response.send_modal(Modal)
        if mode.value == "status_type":
            file = f"database/client_launchers/{self.client.user.id}/status"
            Modal = Edit_Status_Type()
            Modal.personality.default = open(file).read()
            await interaction.response.send_modal(Modal)
        if mode.value == "status_text":
            file = f"database/client_launchers/{self.client.user.id}/text"
            Modal = Edit_Status_Text()
            Modal.personality.default = open(file).read()
            await interaction.response.send_modal(Modal)
        if mode.value == "link":
            file = f"database/client_launchers/{self.client.user.id}/stream_link"
            Modal = Edit_Stream_Link()
            if os.path.exists(file):
                Modal.personality.default = open(file).read()
            await interaction.response.send_modal(Modal)


    @app_commands.command(name="enforce_typing_style", description="[CREATOR ONLY] Edit the bot's typing style")
    @app_commands.choices(
        mode=[
            app_commands.Choice(name='None (Default)', value='none'),
            app_commands.Choice(name='all lowercase', value='lower'),
            app_commands.Choice(name='all lowercase w no punctuation', value='lower_no_p'),
    ])
    async def enforce_typing_style(self, interaction: discord.Interaction, mode: app_commands.Choice[str]):
        if not str(interaction.user.id) in ["746446670228619414", str(self.owner)]:
            return await interaction.response.send_message("You don't own this bot!\nYou can make your own at discord.gg/trianglelabs though :>", ephemeral=True)
        database.set_enforced_typing_style(self.bot.user.id, mode.value)
        await interaction.response.send_message("Typing Style Changed!")

    @app_commands.command(name="change_font", description="Change the font the bot uses")
    @app_commands.choices(
        font=[
            app_commands.Choice(name='None (Default)', value='default'),
            app_commands.Choice(name='𝕋𝕙𝕖 𝕢𝕦𝕚𝕔𝕜 𝕓𝕣𝕠𝕨𝕟 𝕗𝕠𝕩 𝕛𝕦𝕞𝕡𝕤 𝕠𝕧𝕖𝕣 𝕥𝕙𝕖 𝕝𝕒𝕫𝕪 𝕕𝕠𝕘', value="""𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ 𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘~!@#$%^&*()_+`-=[]\{}|;':",./<>?"""),
            app_commands.Choice(name='𝕿𝖍𝖊 𝖖𝖚𝖎𝖈𝖐 𝖇𝖗𝖔𝖜𝖓 𝖋𝖔𝖝 𝖏𝖚𝖒𝖕𝖘 𝖔𝖛𝖊𝖗 𝖙𝖍𝖊 𝖑𝖆𝖟𝖞 𝖉𝖔𝖌', value="""𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅 1234567890~!@#$%^&*()_+`-=[]\{}|;':",./<>?"""),
            app_commands.Choice(name='𝔗𝔥𝔢 𝔮𝔲𝔦𝔠𝔨 𝔟𝔯𝔬𝔴𝔫 𝔣𝔬𝔵 𝔧𝔲𝔪𝔭𝔰 𝔬𝔳𝔢𝔯 𝔱𝔥𝔢 𝔩𝔞𝔷𝔶 𝔡𝔬𝔤', value="""𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ 1234567890~!@#$%^&*()_+`-=[]\{}|;':",./<>?"""),
            app_commands.Choice(name='𝒯𝒽𝑒 𝓆𝓊𝒾𝒸𝓀 𝒷𝓇𝑜𝓌𝓃 𝒻𝑜𝓍 𝒿𝓊𝓂𝓅𝓈 𝑜𝓋𝑒𝓇 𝓉𝒽𝑒 𝓁𝒶𝓏𝓎 𝒹𝑜𝑔', value="""𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵 𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫𝟢~!@#$%^&*()_+`-=[]\{}|;':",./<>?"""),
            app_commands.Choice(name='ᴛʜᴇ Qᴜɪᴄᴋ ʙʀᴏᴡɴ ꜰᴏx ᴊᴜᴍᴘꜱ ᴏᴠᴇʀ ᴛʜᴇ ʟᴀᴢʏ ᴅᴏɢ', value="""ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘQʀꜱᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘQʀꜱᴛᴜᴠᴡxʏᴢ 1234567890~!@#$%^&*()_+`-=[]\{}|;':",./<>?"""),
            # app_commands.Choice(name='🇹​​🇭​​🇪​ ​🇶​​🇺​​🇮​​🇨​​🇰​ ​🇧​​🇷​​🇴​​🇼​​🇳​ ​🇫​​🇴​​🇽​ ​🇯​​🇺​​🇲​​🇵​​🇸​ ​🇴​​🇻​​🇪​​🇷​ ​🇹​​🇭​​🇪​ ​🇱​​🇦​​🇿​​🇾​ ​🇩​​🇴​​🇬​', value="""🇦​​🇧​​🇨​​🇩​​🇪​​🇫​​🇬​​🇭​​🇮​​🇯​​🇰​​🇱​​🇲​​🇳​​🇴​​🇵​​🇶​​🇷​​🇸​​🇹​​🇺​​🇻​​🇼​​🇽​​🇾​​🇿​​🇦​​🇧​​🇨​​🇩​​🇪​​🇫​​🇬​​🇭​​🇮​​🇯​​🇰​​🇱​​🇲​​🇳​​🇴​​🇵​​🇶​​🇷​​🇸​​🇹​​🇺​​🇻​​🇼​​🇽​​🇾​​🇿​ 1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣0️⃣͠❗@#$%^&*()_+`-=[]\{}|⨾❜⦂❝,./<>?"""),
    ])
    async def change_font(self, interaction: discord.Interaction, font: app_commands.Choice[str]):
        database.set_user_font(interaction.user.id, self.bot.user.id, font.value)
        await interaction.response.send_message("Font Changed!")

    @app_commands.command(name="shutup", description="Makes the bot ignore you")
    @app_commands.choices(
        time=[
            app_commands.Choice(name='Stop Ignoring', value='stop'),
            app_commands.Choice(name='1 minute', value="60"),
            app_commands.Choice(name='10 minutes', value="600"),
            app_commands.Choice(name='1 hour', value="3600"),
            app_commands.Choice(name='1 day', value="86400"),
            app_commands.Choice(name='Until I turn it back on', value="""99999999999999999999999999999999999999999"""), # Set the value insanely high so that by the time the bot will start aknowledging your messages, you would already be dead
    ])
    async def shutup(self, interaction: discord.Interaction, time: app_commands.Choice[str]):
        if time.value != "stop":
            await interaction.response.send_message("ok ill shut up for u :c")
            database.set_user_ignore(interaction.user.id, timemodule.time() + float(time.value))
        else:
            await interaction.response.send_message("yayy i can talk again :D")
            database.set_user_ignore(interaction.user.id, 0)

    @commands.hybrid_command(name="feedback", description="Submit Feedback / Bug Reports to the developers")
    async def send_feedback(self, ctx, feedback:str):
        webhook = discord.SyncWebhook.from_url(os.getenv("FEEDBACK_WEBHOOK_URL"))
        embed = discord.Embed(title="Feedback Received", description=feedback, colour=discord.Colour.blurple())
        embed.set_footer(text=f"{ctx.author} ({ctx.author.id})")
        webhook.send(embed=embed)
        await ctx.reply("Your feedback has been sent!", ephemeral=True)

    @commands.hybrid_command(name="help", description="Get help for the bot and its commands")
    async def help_hybrid(self, ctx):
        help_message = discord.Embed(
            title=f"""{self.bot.user.name} Help""",
            description="""
            
**Main Commands**
`/help` - Shows this message
`/enable` - Enable the bot in the current channel
`/disable` - Disable the bot in the current channel
`/generate_art [prompt] [style] [negative_prompt]` - Generate art using AI from 25 unique styles
`/stable_diffision [prompt] [netative_prompt]` - Generate art with the Stable Diffusion AI
`/edit_image` [prompt] [image: attachment]` - Edit a image with a text prompt
`/language [language]` - Choose a language for the bot to speak to you in
`/wack` - Reset the bot's conversation history with yourself

**General Commands**
`/about` - Get general information about the bot
`/ping` - Get the latency of the bot in ms
`/usage` - View your remaining daily quota
`/shutup [time]` - Makes the bot ignore you for a amount of time you choose
`/roleplay [mode]` - Makes the bot add actions in italics

**Configuration**
`/webhook [webhook url]` - Give the bot a webhook to use
`/change_font [font]` - Allows you to choose a 𝔸𝕊ℂ𝕀𝕀 𝕥𝕖𝕩𝕥

**Misc Commands**
`/feedback [feedback]` - Have a suggestion? Let us know!

**Notes**
- If you want the bot to not respond to you while talking in a channel where it is enabled, add a "." before your message
- To get the bot to temporarily ignore you, use the `/shutup` command

            """.strip(),
            colour=discord.Colour.blurple()
        )
        help_message.set_footer(text="Powered by TriangleLabs")
        await ctx.reply(embed=help_message, ephemeral=True)

async def setup(bot):
    await bot.add_cog(MainCog(bot))