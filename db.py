import mysql.connector

def create_connection():
    db_config = {
        'host': '143.244.197.81',
        'user': 'dev',
        'password': 'MyStrongPassword1234$',
        'database': 'haukka99',
    }

    connection = mysql.connector.connect(**db_config)
    return connection

conn = create_connection()

def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
def insert_tuples(exchange_rates):
    query = """
    INSERT INTO currency_list (base_currency, foreign_currency, rate, created_at, updated_at)
    VALUES (%s, %s, %s, NOW(), NOW())
    ON DUPLICATE KEY UPDATE rate = VALUES(rate), updated_at = NOW()
    """
    with conn.cursor() as cur:
        for rate in exchange_rates:
            base_currency, foreign_currency, exchange_rate = rate
            cur.execute(query, (base_currency, foreign_currency, exchange_rate))
        conn.commit()
