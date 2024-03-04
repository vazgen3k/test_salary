from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    token: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def database_url(self):
        return f"{self.DB_NAME}://{self.DB_HOST}:{self.DB_PORT}"
    
    @property
    def bot_token(self):
        return self.token
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
