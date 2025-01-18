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
    x_account = util.find_x_account(mensaje_original)

    # Procesar los botones y extraer los enlaces
    botones_info = []
    if botones and hasattr(botones, 'rows'):
        for fila in botones.rows:
            for boton in fila.buttons:
                texto = boton.text  # Texto del botón
                enlace = boton.url  # Enlace asociado al botón
                botones_info.append({'texto': texto, 'enlace': enlace})

    # Buscar enlaces en el mensaje original (usando expresiones regulares)
    link_patterns = util.get_social_links_patterns()

    # Extraer los enlaces según los patrones definidos
    found_links = util.extract_social_links(mensaje_original)

    # Crear botones a partir de los enlaces encontrados
    for label, url in found_links.items():
        if(url != "No disponible"):
            botones_info.append({'texto': label, 'enlace': url})

    botones_info.append({'texto': 'DEV-Telegram', 'enlace': util.generate_telegram_link_from_creator(mensaje_original)})
    mensaje_original = util.format_launch_response(mensaje_original)

    if x_account:
        # Obtener información de la cuenta de X
        x_info = await x_tools.get_x_account_info(x_account)

        # Formatear la información de la cuenta de X
        if x_info:
            x_info_message = x_tools.format_x_response(x_info)
        else:
            x_info_message = "No se pudo obtener la información de la cuenta de X."

        # Añadir la información al mensaje original
        mensaje_original += f"\n\n{x_info_message}"
    
    # Enviar mensaje y botones a Discord
    await dc_listener.send_discord_message_to_channel(message=mensaje_original, buttons=botones_info)

# Función para iniciar el cliente y escuchar mensajes
async def iniciar_tg_escucha():
    async with client:
        print("Escuchando mensajes...")
        await client.run_until_disconnected()
