from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    reddit_client_id: SecretStr
    reddit_client_secret: SecretStr
    reddit_user_agent: str
    post_url: str = "https://www.reddit.com/r/AskReddit/comments/1kplv0m/whats_the_worst_city_youve_ever_visited/"
    
    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
