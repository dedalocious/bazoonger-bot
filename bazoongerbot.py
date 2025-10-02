# -----------------------------------------------------------------------------------------------------------------
#
# BAZOONGERBOT - IMPORTS
#
# -----------------------------------------------------------------------------------------------------------------

import discord
import random
import os
from flask import Flask
from threading import Thread

# -----------------------------------------------------------------------------------------------------------------
#
# KEEP ALIVE SERVER
#
# -----------------------------------------------------------------------------------------------------------------

app = Flask('')

@app.route('/')
def home():
    return "BazoongerBot is alive!"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -----------------------------------------------------------------------------------------------------------------
#
# DISCORD BOT SETUP
#
# -----------------------------------------------------------------------------------------------------------------

TOKEN = os.environ.get("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# -----------------------------------------------------------------------------------------------------------------
#
# BOT EVENTS
#
# -----------------------------------------------------------------------------------------------------------------

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        if 'arcluz scale this' in message.content.lower():
            
            arcluz_rating = min(random.randint(1, 10), random.randint(1, 10))
            
            if arcluz_rating == 1:
                response = f"**{arcluz_rating}/10** - Way too small."
            elif arcluz_rating == 2:
                response = f"**{arcluz_rating}/10** - Very small."
            elif arcluz_rating == 3:
                response = f"**{arcluz_rating}/10** - A bit on the small side."
            elif arcluz_rating == 4:
                response = f"**{arcluz_rating}/10** - Slightly below average."
            elif arcluz_rating == 5:
                response = f"**{arcluz_rating}/10** - Perfectly average."
            elif arcluz_rating == 6:
                response = f"**{arcluz_rating}/10** - Slightly above average."
            elif arcluz_rating == 7:
                response = f"**{arcluz_rating}/10** - A good size."
            elif arcluz_rating == 8:
                response = f"**{arcluz_rating}/10** - Quite large."
            elif arcluz_rating == 9:
                response = f"**{arcluz_rating}/10** - Very big."
            else:
                response = f"**{arcluz_rating}/10** - It's massive!"

            await message.reply(response)

# -----------------------------------------------------------------------------------------------------------------
#
# RUN THE BOT
#
# -----------------------------------------------------------------------------------------------------------------

keep_alive()
try:
    client.run(TOKEN)
except discord.errors.LoginFailure:
    print("ERROR: Improper Discord token has been passed.")