from dotenv import load_dotenv
import os
import re
from datetime import datetime

# Load environment variables from the .env file
load_dotenv()

def get_env_tg_api_id():
    return str(os.getenv("TG_API_ID"))

def get_env_tg_api_hash():
    return str(os.getenv("TG_API_HASH"))

def get_env_tg_source_channel():
    return str(os.getenv("TG_SOURCE_CHANNEL"))

def get_dc_bot_token():
    return str(os.getenv("DC_BOT_TOKEN"))

def get_env_dc_channel_id():
    return str(os.getenv("DC_CHANNEL_ID"))

def get_env_x_rapid_api_key():
    return str(os.getenv("X_RAPID_API"))

def get_env_x_rapid_api_host():
    return str(os.getenv("X_RAPID_API_HOST"))

def find_x_account(message):
    # Buscar la cuenta de X
    match = re.search(r"x\.com/([\w_]+)", message)
    if match:
        cuenta_x = match.group(1)
        print(f"Cuenta de X: {cuenta_x}")
        return cuenta_x
    else:
        print("No se encontró una cuenta de X.")
        return ""
    
def format_datetime(datetime_to_convert):
    date_obj = datetime.strptime(datetime_to_convert, "%a %b %d %H:%M:%S +0000 %Y")
    return date_obj.strftime("%d %B %Y")  

def format_launch_response(mensaje_original):
    # Patrón para el nombre y ticker
    name_pattern = r"Launch created\s*(.*?)\((.*?)\)"
    name_match = re.search(name_pattern, mensaje_original)
    name_info = {
        "full_name": name_match.group(1).strip() if name_match else "No disponible",
        "ticker": name_match.group(2).strip() if name_match else "No disponible",
    }

    # Patrón para el creador
    creator_pattern = (
        r"Creator\s*"
        r"Creator username:\s*(@\S+)\s*"
        r"Creator display name:\s*(.*?)\s*"
        r"Rep:\s*(\d+)\s*([^\s]*)\s*"
        r"Dev Lock:\s*(\S+)"
    )
    creator_match = re.search(creator_pattern, mensaje_original, re.DOTALL)
    creator_info = {
        "username": creator_match.group(1) if creator_match else "No disponible",
        "display_name": creator_match.group(2).strip() if creator_match else "No disponible",
        "rep": creator_match.group(3) if creator_match else "No disponible",
        "rep_emoji": creator_match.group(4) if creator_match and creator_match.group(4) else "",
        "dev_lock": creator_match.group(5) if creator_match else "No disponible",
    }

    # Eliminar "Launch created"
    mensaje_sin_launch = re.sub(r"^Launch created.*?\n", "", mensaje_original, flags=re.MULTILINE)

    # Eliminar la sección del creador
    mensaje_limpio = re.sub(
        r"Creator\s*Creator username:.*?Dev Lock:.*?(?:\n|$)", "", mensaje_sin_launch, flags=re.DOTALL
    )

    # Reemplazar enlaces en el mensaje original para evitar vistas previas
    mensaje_limpio = re.sub(r"(http[s]?://\S+)", r"<\1>", mensaje_limpio)

    # Crear el mensaje formateado
    info_message = (
        f"\n===================================\n"
        f"**Información del Launch**\n"
        f"===================================\n"
        f"**Nombre:** {name_info['full_name']} ({name_info['ticker']})\n"
        f"**Descripción:**\n{mensaje_limpio}\n"
        f"**DEV_Nombre:** {creator_info['display_name']}\n"
        f"**DEV_Usuario:** {creator_info['username']}\n"
        f"**DEV_REP:** {creator_info['rep']} {creator_info['rep_emoji']}\n"
        f"**DEV_LOCK:** {creator_info['dev_lock']}"
    )

    return info_message

def generate_telegram_link_from_creator(text):
    pattern = r"Creator username:\s*(@\w+)"
    match = re.search(pattern, text)

    if match:
        username = match.group(1)  # Extrae el usuario incluyendo el "@"
        return f"https://t.me/{username[1:]}"  # Genera el enlace eliminando el "@" inicial
    else:
        return "No disponible"

