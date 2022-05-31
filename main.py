# bot.py
import gettext
import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = "private"

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

positiveAffirmations = open('positive_affirmations.txt').read().splitlines()
    
#---------------
# Handles ALL events involving a message sent by the user
#---------------
@client.event
async def on_message(message):
    
    # ------ Make sure the client that sent the message wasn't the bot itself ------ #
    if message.author == client.user:
        return

    # ------ A simple hello ------ # 
    elif message.content.startswith('!hello'):
        await message.channel.send(f'Hello {message.author.display_name}!')


    # ------ List all the commands of this bot ------ #
    elif message.content == '!commands' or message.content == '!Commands':
        
            commands = open('commands.txt').read().splitlines()
            
            await message.channel.send(f'Hello {message.author.display_name}, I can help with a variety of things!\n=========+=========')
            
            for command in commands:
                await message.channel.send(command) 
            
            await message.channel.send(f'=========+========= \n*Please note:* \nI am also able to filter messages based on certain tw. **However** please know that these filters do __not__ apply to any channels that start with tw- .\n=========+=========\n If there is a certain topic or tw that you feel should also be checked for, or if you have any other suggestions that you think should be implemented in the server, please direct message an admin and they would be more than happy to talk to you about it! \n=========+=========\n*You and your feedback matter! Remember, {random.choice(positiveAffirmations)}*\n=========+=========')
            
    # ------ List Important MH Resources ------ # 
    elif message.content == '!Resources' or message.content == '!resources' or message.content == '!Help' or message.content == '!help':
        
        openingStatement = "IF YOU NEED IMMEDIATE MEDICAL ATTENTION DIAL 911"
        resources = ["**National Hotline:** 800-273-8255 \n", "**WPI Campus Police (Emergency):** 508-831-5555 \n", "**WPI Campus Police (Non-Emergency):** 508-831-5433 \n", "**SDCC (24 HR):** 508-831-5540"]
        
        await message.channel.send("```css" + "\n" + "["+ openingStatement + "]" + "\n" + "```")
        for msg in resources: 
         await message.channel.send(msg)

    elif message.content == '!positivity' or message.content == '!Positivity':
        
        positiveQuotes = open('spread_positivity.txt').read().splitlines()
        await message.channel.send(random.choice(positiveQuotes))

    else:
    # ------ Detect Trigger Words ------ #
        async def sendFilteredTriggerMessage(trigger):
           await message.channel.send(f'------ [ *Deleted message with mention of ~~{trigger}~~ by {message.author.display_name}* ] ------ \n \n ------ __Original message from *{message.author.display_name}*__ ------\n\n **TW: ~~{trigger}~~**\n' + f'|| {message.content} ||')
        
        # Checks if the channel is a listed tw channel 
        # - if channel name contains 'tw', this does NOT filter the text in that chat.
        # - if channel name does not contain 'tw', then the bot will filter the text if it contains a tw 
        # *** current tw checked for: 'suicide', 'self harm', 'suicide and self harm'
        if not 'tw' in message.channel.name: 
            
            if 'suicide' in message.content and 'self harm' in message.content:
              await message.delete()
              await sendFilteredTriggerMessage('suicide & self harm')
            
            elif 'suicide' in message.content:
                await message.delete()
                await sendFilteredTriggerMessage('suicide')
        
    
            elif 'self harm' in message.content:
             await message.delete()
             await sendFilteredTriggerMessage('self harm')
        
            else: return
        
        else: return
        
client.run(TOKEN)
