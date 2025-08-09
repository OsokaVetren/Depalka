from sqlalchemy import create_engine, text
from Config.config_reader import config

conn_str = (
    f"postgresql+psycopg2://"
    f"{config.user}:{config.password.get_secret_value()}@"
    f"{config.server_ip}/{config.database_name}"
)
engine = create_engine(conn_str)

def isUserValid():
    #implement validation function
    return

def NewUser():
    #implement user addition
    return

def eballs_change():
    #implement points change
    return