import psycopg2

DB_NAME = "Online store"
DB_USER = "postgres"
DB_PASSWORD = "RafalRogal"
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print("Успешное подключение к PostgreSQL")

    cursor = conn.cursor()

    #BEGINNING

    cursor.execute("CREATE TABLE beg (id SERIAL PRIMARY KEY NOT NULL, name VARCHAR(255), lname VARCHAR(225),address VARCHAR(255));")

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    #ENDING    

    cursor.close()
    conn.close()
except Exception as e:
    print("Ошибка подключения:", e)    