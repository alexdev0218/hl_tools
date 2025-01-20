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

def get_social_links_patterns():
    return {
        "X": r"(https?://x\.com/\S+|x\.com/\S+)",
        "Telegram": r"(https?://t\.me/\S+|t\.me/\S+)",
        "Github": r"(https?://github\.com/\S+|github\.com/\S+)",
        "Website": r"(https?://\S+)"
    }

def extract_social_links(text):
    patterns = get_social_links_patterns()
    extracted_links = {}

    for platform, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            url = match.group(0)
            extracted_links[platform] = ensure_url_scheme(url)
        else:
            extracted_links[platform] = "No disponible"

    return extracted_links

def ensure_url_scheme(url):
    """
    Agrega 'https://' al inicio de una URL si no tiene un esquema válido.
    """
    if not url.startswith(('http://', 'https://')):
        return f"https://{url}"
    return url

def format_launch_response(mensaje_original):
    # Patrón para el nombre y ticker
    name_pattern = r"Launch created\s*(.*?)\((.*?)\)"
    name_match = re.search(name_pattern, mensaje_original)
    name_info = {
        "full_name": name_match.group(1).strip() if name_match else "No disponible",
        "ticker": name_match.group(2).strip() if name_match else "No disponible",
    }

    # Patrón para la descripción
    description_pattern = r"\)\s*(.*?)(?=\nCreator|$)"
    description_match = re.search(description_pattern, mensaje_original, re.DOTALL)
    description = description_match.group(1).strip() if description_match else "No disponible"
    # Eliminar enlaces de la descripción y saltos de línea
    description = re.sub(r"http[s]?://\S+", "", description).replace("\n", " ").strip()

    # Patrón para el creador
    creator_pattern = r"Creator\s*Creator username:\s*(@\S+)\s*Creator display name:\s*(.*?)\s*Rep:\s*(\d+)\s*[⚠️❌]*\s*Dev Lock:\s*(\S+)"
    creator_match = re.search(creator_pattern, mensaje_original)
    creator_info = {
        "username": creator_match.group(1) if creator_match else None,
        "display_name": creator_match.group(2).strip() if creator_match else "No disponible",
        "rep": creator_match.group(3) if creator_match else "No disponible",
        "dev_lock": creator_match.group(4) if creator_match else "No disponible",
    }

    # Generar enlace de Telegram solo si el username existe
    telegram_link = f"https://t.me/{creator_info['username'][1:]}" if creator_info["username"] else ""

    # Crear el mensaje formateado
    info_message = (
        f"\n===================================\n"
        f"**Información del Launch**\n"
        f"===================================\n"
        f"**Nombre:** {name_info['full_name']} ({name_info['ticker']})\n"
        f"**Descripción:** {description}\n"
        f"{f'**Telegram:** {telegram_link}' if telegram_link else ''}\n"
        f"**DEV_Nombre:** {creator_info['display_name']}\n"
        f"**DEV_Usuario:** {creator_info['username']}\n"
        f"**DEV_REP:** {creator_info['rep']}\n"
        f"**DEV_LOCK:** {creator_info['dev_lock']}\n"
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