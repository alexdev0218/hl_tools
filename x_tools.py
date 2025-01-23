import httpx
import re
import util


async def get_x_account_info(account_name):
    host = util.get_env_x_rapid_api_host()
    api_key = util.get_env_x_rapid_api_key()

    url = f"https://{host}/user"
    querystring = {"username":account_name}

    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': host
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers,params=querystring)
        response.raise_for_status()
        data_parsed = response.json()

        # Extraer información importante
        try:
            user_data = data_parsed["result"]["data"]["user"]["result"]
            legacy_data = user_data["legacy"]

            parsed_info = {
                "name": legacy_data["name"],
                "username": legacy_data["screen_name"],
                "description": legacy_data["description"],
                "created_at": util.format_datetime(legacy_data["created_at"]),
                "followers_count": legacy_data["followers_count"],
                "following_count": legacy_data["friends_count"],
                "statuses_count": legacy_data["statuses_count"],
                "is_blue_verified": user_data["is_blue_verified"],
                "profile_image_url": legacy_data["profile_image_url_https"],
                "profile_banner_url": legacy_data.get("profile_banner_url"),
                "last_tweet_id": legacy_data.get("pinned_tweet_ids_str", []),
                "is_identity_verified": user_data.get("verification_info", {}).get("is_identity_verified", False),
            }

            return parsed_info

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
