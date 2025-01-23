import json
import httpx
import re
import util


async def get_x_account_info(account_name):
    host = util.get_env_x_rapid_api_host()
    api_key = util.get_env_x_rapid_api_key()

    url = f"https://{host}/screenname.php"
    querystring = {"screenname": account_name}

    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': host
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            data_parsed = response.json()

            # Extraer información importante
            parsed_info = {
                "name": data_parsed.get("name", "Nombre no disponible"),
                "username": data_parsed.get("profile", "Usuario no disponible"),
                "description": data_parsed.get("desc", "Descripción no disponible"),
                "created_at": util.format_datetime(data_parsed.get("created_at", "Fecha no disponible")),
                "followers_count": data_parsed.get("sub_count", 0),  # Cambiado de friends a sub_count
                "following_count": data_parsed.get("friends", 0),    # Cambiado de friends_count a friends
                "statuses_count": data_parsed.get("statuses_count", 0),
                "is_blue_verified": data_parsed.get("blue_verified", False),
                "profile_image_url": data_parsed.get("avatar", ""),
                "profile_banner_url": data_parsed.get("header_image", ""),
                "last_tweet_id": data_parsed.get("pinned_tweet_ids_str", []),
                "is_identity_verified": False  # No está disponible en la respuesta
            }

            return parsed_info

        except httpx.HTTPStatusError as e:
            print(f"Error en la solicitud HTTP: {e}")
            return None
        except KeyError as e:
            print(f"Error al procesar la respuesta: {e}")
            return None

def format_x_info(x_info):
    # Crear el mensaje base
    x_info_message = (
        f"===================================\n"
        f"**Información de la cuenta de X**\n"
        f"===================================\n"
        f"**Nombre:** {x_info['name']}\n"
        f"**Usuario:** @{x_info['username']}\n"
        f"**Descripción:** {x_info['description']}\n"
        f"**Creada en:** {x_info['created_at']}\n"
        f"**Seguidores:** {x_info['followers_count']}\n"
        f"**Siguiendo:** {x_info['following_count']}\n"
        f"**Tweets:** {x_info['statuses_count']}\n"
        f"**Verificado azul:** {'Sí' if x_info['is_blue_verified'] else 'No'}\n"
        f"**Verificación de identidad:** {'Sí' if x_info['is_identity_verified'] else 'No'}\n"
        f"[Imagen de perfil]({x_info['profile_image_url']})\n"
    )
    # Eliminar enlaces en el mensaje
    x_info_message = re.sub(r'http[s]?://(?!\S*pbs.twimg.com\S+)\S+', '', x_info_message)

    return x_info_message

def extract_x_username(mensaje_original):
    # Patrón para capturar el nombre de usuario sin parámetros adicionales
    pattern = r"(?:https?://)?x\.com/([^\s/?]+)"
    match = re.search(pattern, mensaje_original, re.IGNORECASE)
    return match.group(1) if match else None
