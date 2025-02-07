from enviar.send import enviar_email

import mysql.connector

def inserir_produto(isbn):

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="books"
    )
    
    cursor = db.cursor()

    try:
        cursor.execute("SELECT numero FROM removidos.dados ORDER BY numero ASC LIMIT 1")
        numero_removido = cursor.fetchone()

        if numero_removido:
            numero_usado = numero_removido[0]

            
            cursor.execute("DELETE FROM removidos.dados WHERE numero = %s", (numero_usado,))
        else:
            
            cursor.execute("SELECT MAX(CAST(numero AS UNSIGNED)) FROM produtos")
            max_numero = cursor.fetchone()[0] or 0
            numero_usado = max_numero + 1

        index = len(str(numero_usado))

        isbn_modificado = isbn[:-index] + str(numero_usado)

        cursor.execute("INSERT INTO produtos (numero, isbn_modificado, isbn) VALUES (%s, %s, %s)", (numero_usado, isbn_modificado, isbn))
        db.commit()

        print(f"Produto inserido na tabela de produtos com número {numero_usado} e ISBN {isbn}.")

        return numero_usado

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        db.rollback()

    finally:
        cursor.close()
        db.close()

    return numero_usado

def remover_pedidos(isbn, numero):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="books"
    )
    cursor = db.cursor()
    try:
        
        query_check = "SELECT COUNT(*) FROM pedidos WHERE isbn = %s"
        cursor.execute(query_check, (isbn,))
        (count,) = cursor.fetchone()
        
        if count == 0:
            enviar_email(isbn, numero)
            print("Produto não encontrado na tabela pedidos.")
            return

        
        query_delete = "DELETE FROM pedidos WHERE isbn = %s"
        cursor.execute(query_delete, (isbn,))
        db.commit()
        print("Produto removido da tabela pedidos com sucesso.")
        return
    
    except mysql.connector.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        db.rollback()
        return
    finally:
        cursor.close()
        db.close()




def remover_produto_por_isbn(isbn_modificado):
    
    success_or_error = False

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="books"
    )

    cursor = db.cursor()

    try:
        if len(str(isbn_modificado)) > 10:
            query_select = "SELECT numero, isbn FROM produtos WHERE isbn_modificado = %s"
            query_delete = "DELETE FROM produtos WHERE isbn_modificado = %s"
        else:
            query_select = "SELECT numero, isbn FROM produtos WHERE numero = %s"
            query_delete = "DELETE FROM produtos WHERE numero = %s"
        
        cursor.execute(query_select, (isbn_modificado,))
        resultado = cursor.fetchone()

        if resultado:
            print(f"Resultado do valor de NUMERO {resultado}")
            numero, isbn = resultado

            cursor.execute("SELECT numero FROM removidos.dados WHERE numero = %s", (numero,))
            numero_existente = cursor.fetchone()

            if not numero_existente:

                cursor.execute(query_delete, (isbn_modificado,))
                db.commit()

                if cursor.rowcount > 0:
                    print(f"Produto com identificador {isbn_modificado} removido da tabela 'produtos'.")

                    cursor.execute("INSERT INTO removidos.dados (numero) VALUES (%s)", (numero,))
                    db.commit()

                    print(f"Número {numero} armazenado na tabela 'removidos'.")
                    success_or_error = True

                    remover_pedidos(isbn, numero)
                else:
                    raise ValueError(f"Produto com identificador {isbn_modificado} não foi encontrado na tabela 'produtos' para remoção.")
            else:
                raise ValueError(f"O número {numero} já existe na tabela 'removidos'.")
        else:
            raise ValueError(f"O identificador {isbn_modificado} não existe na tabela 'produtos'.")

    except mysql.connector.Error as err:
        print(f"Erro de banco de dados: {err}")
        db.rollback()

    except ValueError as ve:
        print(f"Erro: {ve}")

    finally:
        cursor.close()
        db.close()
        return success_or_error



# remover_produto_por_isbn('97888782')




    
