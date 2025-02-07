import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS books")

db.database = "books"

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        isbn VARCHAR(100) NOT NULL,
        pedido VARCHAR(255) NOT NULL,
        titulo VARCHAR(255) NOT NULL,
        quantidade VARCHAR(255) NOT NULL,
        numero VARCHAR(255) NOT NULL,
        localizacao VARCHAR(255) NOT NULL
    )
""")


db.commit()
cursor.close()
db.close()

print("Banco de dados e tabela criados com sucesso.")
