from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str = ""
    base_url: str = "https://hellchicken.ru/"


settings = Settings()
