import time
from yandex_gpt import YandexGPT, YandexGPTConfigManagerForAPIKey
from config import app_config

# Setup configuration (input fields may be empty if they are set in environment variables)
config = YandexGPTConfigManagerForAPIKey(
    model_type="yandexgpt",
    catalog_id=app_config.catalog_key,
    api_key=app_config.yagpt_key
)


yandex_gpt = YandexGPT(config_manager=config)

class YandexGPTClient:
    def __init__(self, config_manager):
        self.yandex_gpt = YandexGPT(config_manager=config_manager)

    def chat(self, system_message=None, user_message=None):
        messages = []
        if system_message:
            messages.append({"role": "system", "text": system_message})
        if user_message:
            messages.append({"role": "user", "text": user_message})
        
        if not messages:
            raise ValueError("At least one of system_message or user_message must be provided.")
        
        completion =  self.yandex_gpt.get_sync_completion(messages=messages)
        return completion


def get_client():
    return YandexGPTClient(config_manager=config)

