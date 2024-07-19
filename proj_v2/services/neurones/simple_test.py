import asyncio
from yandex_gpt import YandexGPT, YandexGPTConfigManagerForAPIKey


config = YandexGPTConfigManagerForAPIKey(
    model_type="yandexgpt", catalog_id="b1g3viogkeeft7t0gdl5", api_key="AQVNym4OX9klkEsN3jMA8-tj-8nu2MIky8k-gYsY")


yandex_gpt = YandexGPT(config_manager=config)



async def get_completion():
    messages = [
        {"role": "user", "text": "Hello, world!"},
        ]
    completion = await yandex_gpt.get_async_completion(messages=messages)
    print(completion)


asyncio.run(get_completion())
