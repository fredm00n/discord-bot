import asyncio
import discord
import openai
import os
import random

from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

# Discord configuration
DISCORD_SERVER = 'alfr3do'
DISCORD_TOKEN = os.getenv('GEPPETTO_DISCORD_TOKEN')
GEPPETTO_KEYWORD = os.getenv('GEPPETTO_KEYWORD')
TYPING_DURATION = 3
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True
intents.presences = True
intents.reactions = True
intents.typing = True
client = discord.Client(intents=intents)


# OpenAI configuration
OPENAI_TOKEN = os.getenv('OPENAI_KEY')
MODEL = "text-davinci-003"

openai.organization = os.getenv('OPENAI_ORG')
openai.api_key = OPENAI_TOKEN
openai.Model.list()


# Initialise the members variables
members = {} # storage dictionary
memberslist = '' # string for the console

# Connection to the Discord app
# Initialisation of the members list
@client.event
async def on_ready():
  global memberslist 

  for guild in client.guilds:
    if guild.name == DISCORD_SERVER:
      break

  print(f'---\nSuccess! {client.user} is now connected to the following server: {guild.name} (ID = {guild.id})\n---')

  print(f'Retrieving members list...')
  for member in guild.members:
    members[member.id] = member.name
    memberslist += '{0} ({1}), '.format(member.name,member.id)
  
  print(f'{memberslist}\n---')


#  members = '\n - '.join([member.name for member in guild.members])
#  print(f'Guild Members:\n - {members}')


# Message received
@client.event
async def on_message(message):

  if message.author == client.user:
    print(f'OUTBOUND msg in channel: #{message.channel}')
    return

  print(f'INBOUND msg in channel: #{message.channel}')
  if GEPPETTO_KEYWORD in message.content.lower():
    async with message.channel.typing():
      await asyncio.sleep(TYPING_DURATION)
      await message.reply('Hello!')

  if message.content.startswith('!members'):
      async with message.channel.typing():
        await asyncio.sleep(TYPING_DURATION)
        await message.reply(members)


client.run(DISCORD_TOKEN)
