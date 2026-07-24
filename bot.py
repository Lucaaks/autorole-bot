import os
import discord
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- Server HTTP fittizio per soddisfare Render ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web_server():
    # Render assegna una porta tramite la variabile d'ambiente 'PORT', di default usiamo la 8080
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Avviamo il server web in un thread separato
web_thread = Thread(target=run_web_server)
web_thread.daemon = True
web_thread.start()
# --------------------------------------------------

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
