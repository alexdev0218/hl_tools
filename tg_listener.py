import util
import dc_listener
from telethon import TelegramClient, events

# Credenciales de la API de Telegram
tg_api_id = util.get_env_tg_api_id()
tg_api_hash = util.get_env_tg_api_hash()
tg_source_channel = util.get_env_tg_source_channel()

# Crear cliente de Telegram
client = TelegramClient('session_name', tg_api_id, tg_api_hash)

# Iniciar el cliente global al inicio de la aplicación
async def start_client():
    await client.start()

# Detener el cliente global de Telegram
async def stop_client():
    await client.disconnect()


# Escuchar nuevos mensajes y reenviarlos al canal destino
@client.on(events.NewMessage(chats=tg_source_channel))
async def handler(event):
    mensaje_original = event.message.message
    botones = event.message.reply_markup

    # Procesar los botones y extraer los enlaces
    botones_info = []
    if botones and hasattr(botones, 'rows'):
        for fila in botones.rows:
            for boton in fila.buttons:
                texto = boton.text  # Texto del botón
                enlace = boton.url  # Enlace asociado al botón
                botones_info.append({'texto': texto, 'enlace': enlace})

    # Enviar mensaje y botones a Discord
    await dc_listener.send_discord_message_to_channel(message=mensaje_original, buttons=botones_info)

# Función para iniciar el cliente y escuchar mensajes
async def iniciar_tg_escucha():
    async with client:
        print("Escuchando mensajes...")
        await client.run_until_disconnected()
