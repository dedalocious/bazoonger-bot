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

    message_content_lower = message.content.lower().strip()

    # --- START OF TEXT COMMANDS SECTION ---

    # Responds to the gender question more flexibly
    gender_keywords = ["are you a boy or a girl", "what is your gender", "are you a boy", "are you a girl"]
    if any(keyword in message_content_lower for keyword in gender_keywords):
        gender_choice = random.choice(["I am a boy", "I am a girl", "My gender is undisclosed"])
        response = f"{gender_choice}, but still not big enough for arcluz in the scale."
        await message.reply(response)
        return

    # Responds to the "inverted or protuberant" question
    if "inverted or protuberant" in message_content_lower:
        type_choice = random.choice(["Inverted", "Protuberant"])
        scale_rating = random.randint(1, 10)
        response = f"{type_choice}, but only on the scale {scale_rating}/10."
        await message.reply(response)
        return

    # --- START OF NEW COMPARISON CODE ---
    # Responds to comparison questions like "is X bigger than Y" or "A vs B"
    comparison_triggers = ['bigger than', 'vs']
    for trigger in comparison_triggers:
        if trigger in message_content_lower:
            try:
                # Split the message into two parts based on the trigger
                parts = message_content_lower.split(trigger, 1)
                
                # Extract the last word from the first part as item 1
                item1 = parts[0].strip().split(' ')[-1]
                
                # Extract the first word from the second part as item 2, cleaning punctuation
                item2 = parts[1].strip().split(' ')[0].rstrip('?!.')

                if not item1 or not item2: # Basic check to see if items were extracted
                    continue

                # Generate two different random scores
                score1 = random.randint(1, 10)
                score2 = random.randint(1, 10)

                # Construct the response
                response = (f"Let's compare them on the arcluz scale...\n"
                            f"**{item1.capitalize()}** scores a **{score1}/10**.\n"
                            f"**{item2.capitalize()}** scores a **{score2}/10**.\n\n")

                if score1 > score2:
                    response += f"Looks like **{item1.capitalize()}** is bigger!"
                elif score2 > score1:
                    response += f"Looks like **{item2.capitalize()}** is bigger!"
                else:
                    response += "It's a tie! They are perfectly balanced on the scale."
                
                await message.reply(response)
                return
            except IndexError:
                # This can happen if the trigger is at the very start/end of the message
                continue # Try the next trigger
    # --- END OF NEW COMPARISON CODE ---


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
