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
#deprecated GEPPETTO_KEYWORD = os.getenv('GEPPETTO_KEYWORD') 
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
@client.event
async def on_ready():
  for guild in client.guilds:
    if guild.name == DISCORD_SERVER:
      break
  
  # Global vars
  global MEMBERS
  global MEMBERS_STRING
  global MENTION_STRING
  MEMBERS = {}
  MEMBERS_STRING = ''

  print(f'---\nSuccess! {client.user} is now connected to the following server: {guild.name} (ID = {guild.id})')
  MENTION_STRING = '<@{}>'.format(client.user.id)
  print(f'Geppetto USER ID:{MENTION_STRING}\n---')

  print(f'Retrieving members list...')
  for member in guild.members:
    MEMBERS[member.id] = member.name
    MEMBERS_STRING += '{0} ({1}), '.format(member.name,member.id)
  
  print(f'{MEMBERS_STRING}\n---')


#  members = '\n - '.join([member.name for member in guild.members])
#  print(f'Guild Members:\n - {members}')


# Message received
@client.event
async def on_message(message):

  if message.author == client.user:
    print(f'OUTBOUND msg in channel: #{message.channel}')
    return

  print(f'INBOUND msg in channel: #{message.channel} {message.content}')
  if MENTION_STRING in message.content.lower():
    print(f'MENTION in: #{message.channel}')
    async with message.channel.typing():
      await asyncio.sleep(TYPING_DURATION)
      await message.reply('Hello!')

  if message.content.startswith('!members'):
    print(f'!MEMBERS cmd in channel: #{message.channel}')
    async with message.channel.typing():
      await asyncio.sleep(TYPING_DURATION)
      await message.reply(MEMBERS_STRING)


client.run(DISCORD_TOKEN)
