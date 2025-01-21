import util
import dc_listener
from telethon import TelegramClient, events
import x_tools

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

    # Procesar los botones del mensaje original
    botones_info = []
    if botones and hasattr(botones, 'rows'):
        for fila in botones.rows:
            for boton in fila.buttons:
                texto = boton.text
                enlace = boton.url
                botones_info.append({'texto': texto, 'enlace': enlace})

    # Extraer el enlace de Telegram del creador y añadir el botón correspondiente
    dev_telegram = util.generate_telegram_link_from_creator(mensaje_original)
    if dev_telegram != "No disponible":
        botones_info.append({'texto': 'DEV-Telegram', 'enlace': dev_telegram})

    # Verificar si existe un enlace de X en el mensaje
    x_username = x_tools.extract_x_username(mensaje_original)
    x_info_message = ""
    if x_username:
        x_info = await x_tools.get_x_account_info(x_username)
        if x_info:
            x_info_message = x_tools.format_x_info(x_info)

    # Formatear el mensaje eliminando las partes innecesarias
    mensaje_formateado = util.format_launch_response(mensaje_original)

    # Añadir información de la cuenta de X si está disponible
    if x_info_message:
        mensaje_formateado += f"\n\n{x_info_message}"

    # Enviar el mensaje a Discord con los botones procesados
    await dc_listener.send_discord_message_to_channel(message=mensaje_formateado, buttons=botones_info)

# Función para iniciar el cliente y escuchar mensajes
async def iniciar_tg_escucha():
    async with client:
        print("Escuchando mensajes...")
        await client.run_until_disconnected()
