from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def get_env_tg_api_id():
    return str(os.getenv("TG_API_ID"))

def get_env_tg_api_hash():
    return str(os.getenv("TG_API_HASH"))

def get_env_tg_source_channel():
    return str(os.getenv("TG_SOURCE_CHANNEL"))

def get_env_tg_destination_channel():
    return str(os.getenv("TG_DESTINATION_CHANNEL"))

def get_dc_bot_token():
    return str(os.getenv("DC_BOT_TOKEN"))

def get_env_dc_channel_id():
    return str(os.getenv("DC_CHANNEL_ID"))