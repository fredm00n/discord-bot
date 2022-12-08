import discord
import openai
import os
import random

from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

# Discord configuration
DISCORD_SERVER = 'alfr3do'
DISCORD_TOKEN = os.getenv('TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.typing = True
intents.presences = True
intents.messages = True
intents.guilds = True
intents.reactions = True
client = discord.Client(intents=intents)


# OpenAI configuration
OPENAI_TOKEN = os.getenv('OPENAI_KEY')
MODEL="text-davinci-003"

openai.organization = os.getenv('OPENAI_ORG')
openai.api_key = OPENAI_TOKEN
openai.Model.list()


# Connection to the app
@client.event
async def on_ready():
	for guild in client.guilds:
		if guild.name == DISCORD_SERVER:
			break

	print(
    	f'{client.user} is connected to the following server:\n'
    	f'{guild.name}(id: {guild.id})'
	)

	members = '\n - '.join([member.name for member in guild.members])
	print(f'Guild Members:\n - {members}')




# Message received
@client.event
async def on_message(message):
	print(f'message received in channel: {message.channel}')

	if message.author == client.user:
		return

	if message.content.startswith('troudbal'):
		await message.channel.send('Hello!')


client.run(DISCORD_TOKEN)
