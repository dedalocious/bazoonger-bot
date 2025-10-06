#this is a script made to annoy my friend arcluz lelelelelelele
#----------------------------------------------------------------------------------------------------------------------------------
# IMPORTS AND SETUP
#----------------------------------------------------------------------------------------------------------------------------------

import discord
import random
import hashlib
import os
import aiohttp
from flask import Flask
from threading import Thread

# --- START OF WEB SERVER CODE ---
app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
  # Note: Render provides the PORT environment variable.
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# --- END OF WEB SERVER CODE ---


TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#----------------------------------------------------------------------------------------------------------------------------------
# BOT EVENTS
#----------------------------------------------------------------------------------------------------------------------------------

@client.event
async def on_ready():
    print(f'BazoongerBot has logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command_triggers = [
        'arcluz scale this',
        'scale this',
        'size this',
        'rate this',
        'how big is this',
        'whats its size',
        'give it a rating'
    ]

    message_content_lower = message.content.lower()

    # --- START OF NEW CODE BLOCK ---
    # Responds to the gender question
    if "are you a boy or a girl?" in message_content_lower:
        gender_choice = random.choice(["I am a boy", "I am a girl", "My gender is undisclosed"])
        response = f"{gender_choice}, but still not big enough for arcluz in the scale."
        await message.reply(response)
        return # Use return to stop processing after this command
    # --- END OF NEW CODE BLOCK ---
    
    if client.user.mentioned_in(message) and any(command in message_content_lower for command in command_triggers):

        image_url = None

        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type and attachment.content_type.startswith('image/'):
                    image_url = attachment.url
                    break

        if not image_url and message.reference and message.reference.message_id:
            try:
                replied_to_message = await message.channel.fetch_message(message.reference.message_id)
                if replied_to_message.attachments:
                    for attachment in replied_to_message.attachments:
                        if attachment.content_type and attachment.content_type.startswith('image/'):
                            image_url = attachment.url
                            break
            except discord.NotFound:
                print("Replied to message not found.")
            except discord.Forbidden:
                print("Don't have permissions to fetch the replied to message.")

        if image_url:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as resp:
                        if resp.status == 200:
                            image_bytes = await resp.read()
                            image_hash = hashlib.sha256(image_bytes).hexdigest()
                            random.seed(image_hash)
            except Exception as e:
                print(f"Error downloading or hashing image: {e}")
                pass

        arcluz_rating = min(random.randint(1, 10), random.randint(1, 10))
        random.seed()

        if arcluz_rating == 1:
            rating_description = "Way too small."
        elif arcluz_rating == 2:
            rating_description = "Very small."
        elif arcluz_rating == 3:
            rating_description = "A bit on the small side."
        elif arcluz_rating == 4:
            rating_description = "Slightly below average."
        elif arcluz_rating == 5:
            rating_description = "Perfectly average."
        elif arcluz_rating == 6:
            rating_description = "Slightly above average."
        elif arcluz_rating == 7:
            rating_description = "A good size."
        elif arcluz_rating == 8:
            rating_description = "Quite large."
        elif arcluz_rating == 9:
            rating_description = "Very big."
        else: # rating is 10
            rating_description = "It's massive!"

        response = f"**{arcluz_rating}/10** - {rating_description} on the arcluz scale."

        await message.reply(response)

#----------------------------------------------------------------------------------------------------------------------------------
# RUN THE BOT
#----------------------------------------------------------------------------------------------------------------------------------

keep_alive() # <-- ADD THIS LINE TO START THE WEB SERVER

try:
    client.run(TOKEN)
except Exception as e:
    print(f"ERROR: Could not run the bot. Check that the TOKEN is correct. Error: {e}")
