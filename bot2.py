import discord
import openai
import os
import random

from collections import defaultdict

# Discord configuration
DISCORD_TOKEN = 'MTA0NzQ5Nzc4OTYzMTkwOTkyMA.GqaBhz.G3VHbYhrJV0U_8J8d6ACfqV-0TAcFh2JeGw8w0'
DISCORD_SERVER = 'alfr3do'
intents = discord.Intents.default()
intents.message_content = True
intents.typing = True
intents.presences = True
intents.messages = True
intents.guilds = True
intents.reactions = True
client = discord.Client(intents=intents)


# OpenAI configuration
OPENAI_TOKEN ='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'
MODEL="text-davinci-003"

openai.organization = "org-qiHwVDeiRwr3LjjxbsLL5KxD"
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
