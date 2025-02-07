import mysql.connector

def inserir_pedidos_de_vendas(dados_do_pedido):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="books"
    )
    
    cursor = db.cursor()
    
    sql = """
        INSERT INTO pedidos (isbn, pedido, titulo, quantidade, numero, localizacao)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    valores = (
        dados_do_pedido["isbn"],
        dados_do_pedido["pedido"],
        dados_do_pedido["nome"],
        dados_do_pedido["quantidade"],
        dados_do_pedido["numero"],
        dados_do_pedido["localizacao"]
    )
    
    try:
        cursor.execute(sql, valores)
        db.commit()
        print("Pedido inserido com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao inserir pedido: {err}")
        db.rollback()
    finally:
        cursor.close()
        db.close()