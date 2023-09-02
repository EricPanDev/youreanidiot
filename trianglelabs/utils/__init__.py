import json, requests
import discord, asyncio
from dotenv import load_dotenv
import openai
from os import getenv

load_dotenv()

Moderations_Key = getenv("MOD_KEY")

async def parse_presence(Client, activitytype, status, url=""):
    if activitytype == "listening":
        await Client.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening, name=status))
    elif activitytype == "watching":
        await Client.change_presence(activity=discord.Activity(
                type=discord.ActivityType.watching, name=status))
    elif activitytype == "playing":
        await Client.change_presence(activity=discord.Activity(
                type=discord.ActivityType.playing, name=status))
    elif activitytype == "streaming":
        await Client.change_presence(activity=discord.Streaming(
            name=status,
            url=url))
    print("[Trianglelabs] > Bot Activity set to type %s with name %s (%s)" % (activitytype, status, str(Client.user.id)))

class Moderation:
    async def asyncify(func, *args):
        coro = asyncio.to_thread(func, *args)
        task = asyncio.create_task(coro)
        result = await task
        return result

    async def is_flagged_message(input: str):
        res = await Moderation.asyncify(Moderation.is_safe_message_coro, input)
        return res

    def is_safe_message_coro(input: str):
        out = openai.Moderation().create(
            input=input,
            api_key=Moderations_Key,
        )

        final = out["results"][0]

        stat = any

        try:
            for category in final["categories"]:
                r = final["categories"][category]
                if r == True:
                    stat = True
                else:
                    stat = False
            
            # Now double check the numeric values
            for num in final["category_scores"]:
                r = float(final["category_scores"][num])
                if r >= 0.64:
                    stat = True
                else:
                    stat = False
                    
        except openai.APIError as e:
            print("Exception when calling ModerationAPI->create: %s\n" % e)
            return False
        
        return stat