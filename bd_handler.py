from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from Config.config_reader import config

conn_str = (
    f"postgresql+psycopg2://"
    f"{config.user}:{config.password.get_secret_value()}@"
    f"{config.server_ip}/{config.database_name}"
)
engine = create_engine(conn_str)

def is_user_valid(username, password):
    query = text("""
                 SELECT 1
                 FROM users
                 WHERE username = :username
                 AND password = crypt(:password, password)
                 LIMIT 1
                 """)
    with engine.connect() as conn:
        result = conn.execute(query, {"username": username, "password": password}).first()
    return result is not None

def new_user(username, password):
    query = text("""
                 INSERT INTO users (username, password)
                 VALUES (:username, crypt(:password, gen_salt('bf')))
                 """)
    try:
        with engine.begin() as conn:
            conn.execute(query, {"username": username, "password": password})
        return True
    except IntegrityError:
        return False

def eballs_change(username, delta):
    query = text("""
                 UPDATE users
                 SET eballs = eballs + :delta
                 WHERE username = :username
                 """)
    with engine.begin() as conn:
        result = conn.execute(query, {"username": username, "delta": delta})
    return result.rowcount > 0