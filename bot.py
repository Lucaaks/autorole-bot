import os
import discord

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

# ID del canale specifico e ID del ruolo da assegnare (sostituisci con i tuoi numeri)
TARGET_CHANNEL_ID = 1439333171559661709
ROLE_ID = 1439331331489140856         

@client.event
async def on_ready():
    print(f'Bot online come {client.user}')

@client.event
async def on_message(message):
    # Ignora i messaggi del bot stesso
    if message.author == client.user:
        return

    # Controlla se il messaggio è stato scritto nel canale specifico
    if message.channel.id == TARGET_CHANNEL_ID:
        guild = message.guild
        role = guild.get_role(ROLE_ID)
        
        if role and role not in message.author.roles:
            try:
                await message.author.add_roles(role)
                print("Ruolo assegnato con successo!")
            except discord.Forbidden:
                print("Il bot non ha i permessi sufficienti per assegnare questo ruolo.")

client.run os.environ['TOKEN']
