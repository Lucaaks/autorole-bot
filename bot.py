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

# Definiamo le coppie di Canale e Ruolo (sostituisci i numeri con i tuoi ID reali)
TARGETS = {
    1439333171559661709: 1439331331489140856,  # Canale 1 -> Ruolo 1
    1530932899707228170: 1530934849353814086, # Canale 2 -> Ruolo 2
    1439335573323124776: 1437828449635930152  # Canale 3 -> Ruolo 3
}

@client.event
async def on_ready():
    print(f'Bot online come {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Controlla se il canale in cui è stato scritto il messaggio è tra quelli monitorati
    if message.channel.id in TARGETS:
        guild = message.guild
        role_id = TARGETS[message.channel.id]
        role = guild.get_role(role_id)

        if role and role not in message.author.roles:
            try:
                await message.author.add_roles(role)
                print(f"Ruolo {role.name} assegnato con successo a {message.author}!")
            except discord.Forbidden:
                print("Il bot non ha i permessi sufficienti per assegnare questo ruolo.")

client.run(os.environ['TOKEN'])
