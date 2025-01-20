import discord
from discord.ext import commands
import util

# Configura el token del bot
BOT_TOKEN = util.get_dc_bot_token()
ROLE_NAME = "Hyperdegen"

# Configura el bot
intents = discord.Intents.default()
intents.message_content = True  # Activa el intent para leer mensajes
intents.guilds = True  # Permite obtener información de servidores
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # Usaremos app_commands para slash commands

async def send_discord_message_to_channel(message: str, buttons: list = None):
    """
    Envía un mensaje a un canal de Discord con botones interactivos.
    """
    channel_id = util.get_env_dc_channel_id()  # ID del canal desde tus utilidades
    channel = bot.get_channel(channel_id)  # Busca el canal por ID
    if channel is None:
        print(f"No se pudo encontrar el canal con ID: {channel_id}. Intentando obtener de nuevo...")
        try:
            channel = await bot.fetch_channel(channel_id)
        except Exception as e:
            print(f"Error al obtener el canal: {e}")
            return

    if channel:
        try:
            # Buscar el rol en el servidor
            guild = channel.guild  # Obtén la guild del canal
            role = discord.utils.get(guild.roles, name=ROLE_NAME)  # Busca el rol por nombre
            if role is None:
                print(f"No se encontró el rol '{ROLE_NAME}' en el servidor.")
                return

            # Construye el mensaje con la mención al rol
            role_mention = f"<@&{role.id}>"
            content = f"{role_mention} {message}"

            # Crear la vista con los botones si existen
            view = None
            if buttons:
                view = discord.ui.View()
                for button in buttons:
                    # Crea un botón con el texto y el enlace
                    discord_button = discord.ui.Button(label=button['texto'], url=button['enlace'])
                    view.add_item(discord_button)

            # Envía el mensaje con o sin botones
            await channel.send(content, view=view)
            print(f"Mensaje enviado a {channel_id}: {content}")
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
    else:
        print(f"No se encontró el canal tras múltiples intentos.")

# Evento cuando el bot está listo
@bot.event
async def on_ready():
    await tree.sync()  # Sincroniza los comandos de aplicación con Discord
    print(f'Conectado como {bot.user}')

async def iniciar_dc_bot():
    await bot.start(BOT_TOKEN)
