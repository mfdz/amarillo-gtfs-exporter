from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    generator_url: str = 'http://localhost:8002'
    model_config = ConfigDict(extra='allow')

config = Config(_env_file='config', _env_file_encoding='utf-8')
