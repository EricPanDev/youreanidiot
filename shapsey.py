import requests
import os, asyncio, sys, random
from trianglelabs import database, utils
from dotenv import load_dotenv as load
load()

bots_store = "database/client_launchers"

import nest_asyncio
nest_asyncio.apply()

class vars:
    ok = {}
from discord.ext import tasks
async def testtoken(token, num):
    import discord
    from discord.ext import commands
    e = 0
    client = commands.Bot(command_prefix=">", intents=discord.Intents.all())
    @client.event
    async def on_ready():
        avatar = ""
        try:
            avatar = client.user.avatar.url
        except:
            try:
                avatar = client.user.avatar_url
            except:
                avatar = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTRjL2_25sD9RaTkTsLT_bXPv4lkwMIBcWyUhU2wOruwQ&s"
        vars.ok[num] =  [1, client.user.id,client, [client.user.name, avatar]]
        await client.close()
    try:
        client.run(token)
    except discord.errors.PrivilegedIntentsRequired:
        vars.ok[num] =  [0,0,0]
    except discord.errors.LoginFailure:
        vars.ok[num] =  [2,0,0]
    return 


bots = {}
import subprocess
import discord
from discord import ui
from discord.ext import commands
Client = commands.Bot(command_prefix=commands.when_mentioned_or(">>>"), intents=discord.Intents.all())
async def ainput(string: str) -> str:
    await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s+' '))
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)

class Bot_Creation_Form(ui.Modal, title="BeyondAI Bot Creation Form"):
    def __init__(self):
        super().__init__(timeout=None)
    status = ui.TextInput(label="Bot's Status Type", placeholder="playing/listening/watching/streaming", style=discord.TextStyle.short, required=True)
    text = ui.TextInput(label="Bot's Status Text", placeholder="ex: my DMs, .gg/server, etc", style=discord.TextStyle.short, required=True)
    stream_link = ui.TextInput(label="Optional Streaming link", placeholder="only fill this out if bot's status is streaming", style=discord.TextStyle.short, required=False)
    token = ui.TextInput(label="token", placeholder="Paste your token here", style=discord.TextStyle.short, required=True)
    personality = ui.TextInput(label="Bot's Personality",placeholder="Write some things that the bot likes and dislikes...\nGIVE BOT ALL INTENTS BEFORE SUBMITTING", style=discord.TextStyle.long, min_length=100, required=True)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Validating Info...\n(If you see this message for more than a minute, create a support ticket)")
        message = await interaction.original_response()
        is_safe = await utils.Moderation.is_flagged_message(self.personality.value)
        if not is_safe:
            await message.edit(
                content=f"I'm sorry but the bot's backstory/personality is too inappropriate to be used. Please try again with something more PG-13, thank you!"
            )
            return
            
        num = random.randint(0, 1000000)
        await testtoken(self.token.value, num)
        e = vars.ok[num]
        if e[0] == 0:
            await message.edit(content=f'Bot is missing Intents.\nThe bot\'s personality is below so you don\'t need to re-type it.\n```{self.personality.value}```')
        elif e[0] == 2:
            await message.edit(content=f'Token is invalid.\nThe bot\'s personality is below so you don\'t need to re-type it.\n```{self.personality.value}```')
        else:
            await message.edit(content=f'Bot has been created. It can be invited at https://discord.com/api/oauth2/authorize?client_id={e[1]}&permissions=139586718784&scope=applications.commands%20bot')
            num = e[1]
            bots[f"{num}"] = subprocess.Popen(["python3", "client.py", self.token.value, str(self.status.value).lower(), str(self.text.value), self.personality.value, str(interaction.user.id), str(num), self.stream_link.value])
            os.system(f"mkdir '{bots_store}/{num}'")
            with open(f'{bots_store}/{num}/status', "w") as f:
                f.write(self.status.value)
                f.close()
            with open(f'{bots_store}/{num}/text', "w") as f:
                f.write(self.text.value)
                f.close()
            with open(f'{bots_store}/{num}/stream_link', "w") as f:
                f.write(self.stream_link.value)
                f.close()
            with open(f'{bots_store}/{num}/token', "w") as f:
                f.write(self.token.value)
                f.close()
            with open(f'{bots_store}/{num}/personality', "w") as f:
                f.write(self.personality.value)
                f.close()
            with open(f'{bots_store}/{num}/owner', "w") as f:
                f.write(str(interaction.user.id))
                f.close()
            if interaction.user.id != 308045225295872001:
                guild = Client.get_guild(1079258976111304744)
                channel = guild.get_channel(1094015878087049347)
                if len(self.personality.value) > 2000:
                    # Split it in two
                    await channel.create_thread(
                        name=e[3][0], 
                        content=f"{e[3][1]}\n**{e[3][0]}** - Created by <@{interaction.user.id}>\n**Invite Link**\nhttps://discord.com/api/oauth2/authorize?client_id={e[1]}&permissions=139586718784&scope=applications.commands%20bot\n**Shape Backstory**```{self.personality.value[:2000]}```"
                    ).send(f"```{self.personality.value[2000:]}```")
                else:
                    await channel.create_thread(
                        name=e[3][0], 
                        content=f"{e[3][1]}\n**{e[3][0]}** - Created by <@{interaction.user.id}>\n**Invite Link**\nhttps://discord.com/api/oauth2/authorize?client_id={e[1]}&permissions=139586718784&scope=applications.commands%20bot\n**Shape Backstory**```{self.personality.value}```"
                    )
            else:
                await interaction.channel.send("helo miss para :D\nur bot has not been posted xd")

async def start_bots():
    global bots
    if "0000" in bots:
        print(f"[Trianglelabs] > RESTARTING CLIENT 0000...")
        bots[f"0000"].kill()
        await asyncio.sleep(2)
    bots["0000"] = subprocess.Popen(["python3", "client.py", str(os.getenv("TRIANGLE_TOKEN")), "playing", "v3.0.2", "a really chill human who loves helping others", "746446670228619414", "0000000000", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"])
    for num in os.listdir(bots_store):
        if os.path.exists(bots_store+f"/{num}"):
            __loc = bots_store+f"/{num}/"
            if not os.path.exists(__loc + "DONOTTOUCH"):
                if not os.path.exists(__loc + "DONOTTOUCH2"):
                    with open(__loc + "status") as f:
                        status = f.read()
                        f.close()
                    with open(__loc + "text") as f:
                        text = f.read()
                        f.close()
                    with open(__loc + "stream_link") as f:
                        stream_link = f.read()
                        f.close()
                    with open(__loc + "token") as f:
                        token = f.read()
                        f.close()
                    with open(__loc + "personality") as f:
                        personality = f.read()
                        f.close()
                    try:
                        with open(__loc + "owner") as f:
                            owner = f.read()
                            f.close()
                    except:
                        owner = ""
                    if f"{num}" in bots:
                        print(f"[Trianglelabs] > RESTARTING CLIENT {num}...")
                        bots[f"{num}"].kill()
                        await asyncio.sleep(2)
                    print(f"started bot {token}")
                    bots[f"{num}"] = subprocess.Popen(["python3", "client.py", token, status, text, personality, owner, str(num), stream_link])
                else:
                    print(f"[Trianglelabs] > Skipping Client {num} due to Missing Intents")
            else:
                print(f"[Trianglelabs] > Skipping Client {num} due to Invalid Token")

@Client.event
async def on_ready():
    await Client.tree.sync()
    global bots
    await Client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="my DMs"))
    myLoop.start()
    await start_bots()
    __exit = 0
    while not __exit:
        print("await command...")
        command = await ainput("Command: ")
        print("received: " + command)
        if "r" in command:
            await start_bots()
        elif "e" in command:
            print("\nKILLING")
            for i in bots:
                try:
                    bots[i].kill()
                except Exception:
                    pass
            print("KILLED")
            __exit = 1
    exit()

@Client.event
async def on_message(message):
    if (message.channel.type is discord.ChannelType.private) and not message.author.bot:
        await message.channel.send(content="lets goooo\n:warning: make sure to give bot all Intents before submitting the form otherwise it wont work", view=Confirm())

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
    @discord.ui.button(label='Create Bot', style=discord.ButtonStyle.green, custom_id="create_bot")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        ...
updated_val = 0
@tasks.loop(seconds = 30)
async def myLoop():
    global updated_val
    Guild = Client.get_guild(1079258976111304744)
    Channel = Guild.get_channel(1093564458930020384)
    if updated_val != len(bots):
        updated_val = len(bots)
        await Channel.edit(name=f"Chatbots: {len(bots)}")

@Client.event
async def on_interaction(interaction):
    if 'custom_id' in interaction.data:
        if interaction.data['custom_id'] == "create_bot":
            await interaction.response.send_modal(Bot_Creation_Form())

async def asyncify(func, *args):
    coro = asyncio.to_thread(func, *args)
    task = asyncio.create_task(coro)
    result = await task
    return result

async def generate_character_backstory(character):
    data = await asyncify(generate_character_backstory_coro, character)
    return data

def generate_character_backstory_coro(character):
    url = "https://chatgpt-api7.p.rapidapi.com/ask"
    payload = { "query": f"Generate a max 3000 character prompt for a how the character {character} acts. Be very descritive about their personality, hobbies, likes and dislikes, how they would text, names of people they like, and how they would respond to certain words. do not introduce. Replace the character's name with {'{shape}'} and the user's name with {'{user}'}. Prompt: " }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": str(os.getenv("RAPID_API")),
        "X-RapidAPI-Host": "chatgpt-api7.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()['response'].replace("assistant:", "").replace("system:", "").replace("user:", "").strip()
    return data

@Client.tree.command(name="generate_backstory", description="Use BeyondAI to create a backstory on a existing character.")
async def generate_backstory(interaction:discord.Interaction, prompt:str):
    if not database.is_generation_limited(interaction.user.id):
        database.log_generation(interaction.user.id)
        await interaction.response.send_message("Generating... ETA: 20s")
        try:
            data = await generate_character_backstory(prompt)
            message = await interaction.original_response()
            await message.edit(content=f"Here is your generated backstory!\n```{data}```")
        except Exception as e:
            message = await interaction.original_response()
            await message.edit(content="An error occured while generating your backstory. Please try again later.")
    else:
        await interaction.response.send_message("You've reached your daily quota for that command!")

@Client.tree.command(name="create_bot", description="Create a Bot with BeyondLabs")
async def create_bot_slash(interaction: discord.Interaction):
    await interaction.response.send_modal(Bot_Creation_Form())

Client.run(str(os.getenv("SHAPSEY_KEY")))
