import os
from flask import Flask
from threading import Thread
import discord

# --- SERVER WEB PER RENDER / UPTIMEROBOT ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is active!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
# ---------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

TARGET_CHANNEL_ID = 1439333171559661709
ROLE_ID = 1439331331489140856

@client.event
async def on_ready():
    print(f'Bot online come {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == TARGET_CHANNEL_ID:
        guild = message.guild
        role = guild.get_role(ROLE_ID)

        if role and role not in message.author.roles:
            try:
                await message.author.add_roles(role)
                print("Ruolo assegnato con successo!")
            except discord.Forbidden:
                print("Il bot non ha i permessi sufficienti per assegnare questo ruolo.")

client.run(os.environ['TOKEN'])
