import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS removidos")

db.database = "removidos"

cursor.execute("""
    CREATE TABLE IF NOT EXISTS dados_up (
        id INT AUTO_INCREMENT PRIMARY KEY,
        numero VARCHAR(100) NOT NULL
    )
""")


db.commit()
cursor.close()
db.close()

print("Banco de dados e tabela criados com sucesso.")
