import asyncio
import discord
import openai
import os
import random

from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
OPENAI_KEY = os.getenv('OPENAI_KEY')
GUILD = 'alfr3do'
openai.api_key = OPENAI_KEY
MODEL="text-davinci-003"


#client = discord.Client()

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True
intents.reactions = True
client = discord.Client(intents=intents)

def ask_prompt(prompt, model=MODEL, num_results=1, max_tokens=250, stopSequences=["You:", "Troudbal:"],
                  temperature=0.8, topP=1.0, topKReturn=2):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=topP,
        frequency_penalty=0.3,
        presence_penalty=0.3,
        stop=stopSequences
    )
    if response != 0:
        for choice in response.choices:
            return choice.text
    return "[idk]"


ask_god = ask_prompt





DISCORD_BOT_TOKEN = TOKEN

COMMAND_Troudbal="Troudbal god: "
COMMAND_ENABLE="Troudbal enable"
COMMAND_DISABLE="Troudbal disable"
COMMAND_CLEAN="Troudbal clean"
COMMAND_PRESENCE="Troudbal are you there?"

MEMORY_LIMIT = 5
JUMP_IN_HISTORY = 10
JUMP_IN_PROBABILITY_DEFAULT = 15

COMMAND_SHAKESPEARE="Shakespeare: "

COMMAND_MARV="Marv: "
MARV_PROMPT = """Marv is a chatbot that reluctantly answers questions.
You: How many pounds are in a kilogram?
Marv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.
You: What does HTML stand for?
Marv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.
You: When did the first airplane fly?
Marv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.
You: What is the meaning of life?
Marv: I’m not sure. I’ll ask my friend Google. Not to Bing, it would just say to buy Microsofts products.
You: {0}
Marv:"""


class AIPromptResponse:
    def __init__(self, prompt, response, author = "You"):
        self.prompt = prompt
        self.resp = response.strip()
        self.author = author
    def __str__(self):
        return "".join(["\n", self.author, ": ", self.prompt, "\nTroudbal: ", self.resp, "\n"])

class AIMemory:
    #BASE_TEXT="Troudbal is the god of all beings. Yet, he is the most lovely god and answers in a very complete manner.\n\n"
    #BASE_PROMPT=AIPromptResponse("Who is god?", "Well, now that you ask, I can tell you. I, Troudbal is the great goddess is the god of everybody!\n", "AlexisTM")
    BASE_TEXT=""
    BASE_PROMPT=""
    def __init__(self):
        self.req_resps = []
    def update(self, prompt, response, author="You"):
        self.req_resps.append(AIPromptResponse(prompt, response))
        if len(self.req_resps) > MEMORY_LIMIT:
            self.req_resps.pop(0)
    def clear(self):
        self.req_resps = []
    def get(self):
        result = "".join([self.BASE_TEXT])
        if len(self.req_resps) <= 2:
            result += str(self.BASE_PROMPT)
        else:
            for val in self.req_resps:
                result += str(val)
        return result


last_ai_request = defaultdict(AIMemory)
enabled_channels = dict()


@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    data = message.content
    source = ""
    if type(message.channel) is discord.DMChannel:
        source = "".join(["#", message.channel.recipient.name])
    elif message.guild:
        source = "".join([message.guild.name, "#", message.channel.name])
    else:
        source = "".join(["#", message.channel.name])
	
    if "troudbal" in data.lower():
        prompt = data
        ai_prompt = "{0}\nYou: {1}\nTroudbal:".format(last_ai_request[source].get(), prompt)
        print('Prompt: {0}'.format(ai_prompt))
        result = ask_god(ai_prompt)
        if result != "":
            last_ai_request[source].update(prompt, result, message.author.name)
            print(result)
            print('END OF PROMPT -------------')
            async with message.channel.typing():
                await asyncio.sleep(3)
                await message.reply('{0}'.format(result))
    elif type(message.channel) is discord.DMChannel:
        prompt = data
        ai_prompt = "{0}\nYou: {1}\nTroudbal:".format(last_ai_request[source].get(), data)
        print('Prompt: {0}'.format(ai_prompt))
        result = ask_god(ai_prompt)
        if result != "":
            last_ai_request[source].update(prompt, result, message.author.name)
            await message.channel.send('{0}'.format(result))

    else: # Random responses
        if hash(message.channel) not in enabled_channels: return
        if enabled_channels[hash(message.channel)] <= random.randint(0, 99): return

        prompt = "This is a conversation between Troudbal, god of all beings and his subjects.\n\n"
        prompt = "\n\nTroudbal god: I am Troudbal. What can I do for you?"

        hisory = await message.channel.history(limit=10).flatten()
        #.flatten()
        for history_message in reversed(hisory):
            prompt += "\n\n" + str(history_message.author.name) + ": " + str(history_message.content)
            if history_message.author == client.user:
                pass
        prompt += "\n\nTroudbal god: "
        print(prompt)

        result = ask_god(prompt)
        if result != "":
            last_ai_request[source].update(prompt, result, message.author.name)
            await message.channel.send('{0}'.format(result))




"""

@client.event
async def on_ready():
	for guild in client.guilds:
		if guild.name == GUILD:
			break

	print(
    	f'{client.user} is connected to the following guild:\n'
    	f'{guild.name}(id: {guild.id})'
	)

	members = '\n - '.join([member.name for member in guild.members])
	print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
	print(f'message received in channel: {message.channel}')

	if message.author == client.user:
		return

	if message.content.startswith('hello'):
		await message.channel.send('Hello!')
#		await message.author.create_dm()
#		await message.author.dm_channel.send('Hello!')


"""

client.run(TOKEN)


print('hello world2')
