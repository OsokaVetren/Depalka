from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from Config.config_reader import config
import json
from datetime import datetime

conn_str = (
    # временно для отладки — не оставляй в продеssword ->", config.password.get_secret_value())
    f"postgresql+psycopg2://"
    f"{config.db_user}:{config.password.get_secret_value()}@"
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

def new_user(user_id, username, password):
    query = text("""
                 INSERT INTO users (user_id, username, password, eballs)
                 VALUES (:user_id, :username, crypt(:password, gen_salt('bf')), 100)
                 """)
    try:
        with engine.begin() as conn:
            conn.execute(query, {"user_id": user_id, "username": username, "password": password})
        return True
    except IntegrityError:
        return False

def update_user(old_username, username, password):
    query = text("""
                UPDATE users
                SET username = :username, password = crypt(:password, gen_salt('bf'))
                WHERE username = :old_username
                  """)
    with engine.begin() as conn:
        conn.execute(query, {"old_username": old_username, "username": username, "password": password})
        return True

def eballs_balance(username):
    query = text("""
                 SELECT eballs
                 FROM users
                 WHERE username = :username
                 LIMIT 1
                 """)
    with engine.begin() as conn:
        result = conn.execute(query, {"username": username}).first()
    return result[0]

def eballs_change(username, delta):
    query = text("""
                 UPDATE users
                 SET eballs = eballs + :delta
                 WHERE username = :username
                 """)
    with engine.begin() as conn:
        result = conn.execute(query, {"username": username, "delta": delta})
    return result.rowcount > 0

def dodep_update_all():
    query = text(f"""
        UPDATE users
        SET eballs = GREATEST(eballs, 10)
    """)
    with engine.begin() as conn:
        conn.execute(query)
    print('вовчик лох')


def log_game(username, game_type, bet_amount, result, prize_amount=0, details=None):
    query = text("""
                 INSERT INTO game_logs (username, game_type, bet_amount, result, prize_amount, details)
                 VALUES (:username, :game_type, :bet_amount, :result, :prize_amount, :details)
                 """)
    
    details_json = json.dumps(details) if details else None
    
    try:
        with engine.begin() as conn:
            conn.execute(query, {
                "username": username,
                "game_type": game_type,
                "bet_amount": bet_amount,
                "result": result,
                "prize_amount": prize_amount,
                "details": details_json
            })
        return True
    except Exception as e:
        print(f"Ошибка при записи: {e}")
        return False

def get_user_stats(username, limit=10):
    query = text("""
                 SELECT timestamp, game_type, bet_amount, result, prize_amount, details
                 FROM game_logs
                 WHERE username = :username
                 ORDER BY timestamp DESC
                 LIMIT :limit
                 """)
    
    with engine.connect() as conn:
        result = conn.execute(query, {"username": username, "limit": limit}).fetchall()
    return [dict(row._mapping) for row in result]

def stats_advanced(username):
    query = text("""
                 SELECT 
                    COUNT(*) AS spins_count,
                    COALESCE(SUM(bet_amount), 0) AS total_deposit
                FROM game_logs
                WHERE username = :username;
                """)
    with engine.connect() as conn:
        result = conn.execute(query, {"username": username}).mappings().first()
        return result["spins_count"], result["total_deposit"]
      
def get_top_players(limit=10):
    query = text("""
                 SELECT u1.username, u1.eballs
                 FROM users u1
                 WHERE u1.id = (
                    SELECT MIN(u2.id) 
                    FROM users u2
                    WHERE u2.user_id = u1.user_id
                 )
                 ORDER BY u1.eballs DESC
                 LIMIT :limit
                 """)
    
    with engine.connect() as conn:
        result = conn.execute(query, {"limit": limit}).fetchall()
    return [dict(row._mapping) for row in result]
