from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    project_name: str = "eCRM API"
    api_v1_str: str = "/api/v1"
    env: str
    server_uri: str
    server_port: str
    database_uri: str
    ext_db_uri: str
    secret: str
    access_token_expire_minutes: int    
    algorithm: str
    items_per_page: int
    default_password: str
          
    log_format_dev: str
    log_format_prod: str   
    
    pwd_length_min: int
    pwd_length_max: int
    pwd_level: int

    @property
    def log_level(self):
        return 'DEBUG' if self.env == 'dev' or self.env == 'development' else 'INFO'

    @property
    def log_config(self):
        # Logging 
        current_log_format = self.log_format_dev if self.env == 'dev' or self.env == 'development' else self.log_format_prod
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": current_log_format,
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
            },
            "loggers": {
                f"{self.app_name}": {"handlers": ["default"], "level": self.log_level},
            }
        }


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()