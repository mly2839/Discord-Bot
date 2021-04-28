import discord
import os
import requests
import json
import random
from replit import db

client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Nice Guy')
    
  if message.content.startswith('$Rquote'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('$addpp'):
    stringList = message.content.split()
    name = stringList[1]
    pp = random.randrange(1, 10, 1)
    try: 
      value = db[name]
    except Exception as e:
      value = 0
    value = int(pp) + int(value)
    db[name] = value
    await message.channel.send("Successfully added " + str(pp) + " pp for a total of " + str(value))
  
  if message.content.startswith('$pp'):
    stringList = message.content.split()
    name = stringList[1]
    try: 
      value = db[name]
    except Exception as e:
      value = -1
    if value == -1:
      await message.channel.send("No pp")
    else:
      await message.channel.send(str(value) + " pp")

  if message.content.startswith('$spp'):
    stringList = message.content.split()
    name = stringList[2]
    pp = stringList[1]
    try: 
      value = db[name]
    except Exception as e:
      value = 0
    value = int(value) - int(pp)
    db[name] = value
    await message.channel.send("Successfully subtracted " + pp + " pp for a total of " + str(value))

  if message.content.startswith('$help'):
    await message.channel.send("```\n                   LIST OF FUNCTIONS\n------------------------------------------------------\n$help : Displays help message\n$addpp @user : Adds a random number of pp from 1 to 10\n$pp @user : Displays the pp of that user\n$hello : shows a message\n$Rquote : Gives a random quote\n$top5 : Displays top 5 sorted list of members\n$rank : Displays sorted list of members\n$umin : Juice```")

  if message.content.startswith('$top5'):
    keys = db.keys()
    keyList = list(keys)
    valueList = list(keys)
    for x in range(0, len(keyList)):
      name = str(keyList[x])
      valueList[x] = db[name]
    sortKList = [x for _, x in sorted(zip(valueList, keyList), reverse = True)]
    for x in range(0, 5):
      await message.channel.send(str(sortKList[x]) + ": " + str(db[str(sortKList[x])]) + "pp")

  if message.content.startswith('$ranks'):
    keys = db.keys()
    keyList = list(keys)
    valueList = list(keys)
    for x in range(0, len(keyList)):
      name = str(keyList[x])
      valueList[x] = db[name]
    sortKList = [x for _, x in sorted(zip(valueList, keyList), reverse = True)]
    for x in range(0, len(sortKList)):
      await message.channel.send(str(sortKList[x]) + ": " + str(db[str(sortKList[x])]) + "pp")

  if message.content.startswith('$del'):
    stringList = message.content.split()
    name = stringList[1]
    del db[name]

  if message.content.startswith('$umin'):
    await message.channel.send("https://www.youtube.com/watch?v=mzB1VGEGcSU")
  
client.run(os.getenv('TOKEN'))
