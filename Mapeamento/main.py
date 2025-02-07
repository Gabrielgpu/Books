from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import mysql.connector
from Mapeamento.estantes_mapeamento import estante_rua1, estante_rua2_lado_a, estante_rua2_lado_b, estante_rua3_lado_a, estante_rua3_lado_b, estante_rua4, rua_um_lado_a, rua_um_lado_b, rua_dois_lado_a, rua_dois_lado_b, rua_tres_lado_a, rua_tres_lado_b

app = FastAPI()
templates = Jinja2Templates(directory="templates")



def localizar_livro_up(numero_livro):
    ruas = {
        "rua 1a": range(1, 7591),
        "rua 1b": range(7592, 15091),
        "rua 2a": range(15092, 22504),
        "rua 2b": range(22505, 29875),
        "rua 3a": range(29876, 37236),
        "rua 3b": range(37237, 44689),
    }
    
    rua_merca = ""

    for rua, intervalo in ruas.items():
        if numero_livro in intervalo:
            if rua == "rua 1a":
                rua_merca = "Rua 1A |"
                estantes = rua_um_lado_a()
            elif rua == "rua 1b":
                rua_merca = "Rua 1B |"
                estantes = rua_um_lado_b()
            elif rua == "rua 2a":
                rua_merca = "Rua 2A |"
                estantes = rua_dois_lado_a()
            elif rua == "rua 2b":
                rua_merca = "Rua 2B |"
                estantes = rua_dois_lado_b()
            elif rua == "rua 3a":
                rua_merca = "Rua 3A |"
                estantes = rua_tres_lado_a()
            elif rua == "rua 3b":
                rua_merca = "Rua 3B |"
                estantes = rua_tres_lado_b()



    try:
        for chave, (inicio, fim) in estantes.items():
            if inicio <= numero_livro <= fim:
                return rua_merca + "  " + chave
    except UnboundLocalError:
        return "Não foi mapeado"
    
    return "Não foi mapeado"




def localizar_livro(numero_livro):
    ruas = {
        "rua 1": range(1, 4464),
        "rua 2a": range(4464, 8811),
        "rua 2b": range(8812, 13110),
        "rua 3a": range(13111, 17432),
        "rua 3b": range(17433, 21713),
        "rua 4": range(21714, 23811)

    }
    
    rua_merca = ""

    for rua, intervalo in ruas.items():
        if numero_livro in intervalo:
            if rua == "rua 1":
                rua_merca = "Rua 1 |"
                estantes = estante_rua1()
            elif rua == "rua 2a":
                rua_merca = "Rua 2A |"
                estantes = estante_rua2_lado_a()
            elif rua == "rua 2b":
                rua_merca = "Rua 2B |"
                estantes = estante_rua2_lado_b()
            elif rua == "rua 3a":
                rua_merca = "Rua 3A |"
                estantes = estante_rua3_lado_a()
            elif rua == "rua 3b":
                rua_merca = "Rua 3B |"
                estantes = estante_rua3_lado_b()
            elif rua == "rua 4":
                rua_merca = "Rua 4 |"
                estantes = estante_rua4()
    try:
        for chave, (inicio, fim) in estantes.items():
            if inicio <= numero_livro <= fim:
                return rua_merca + "  " + chave
    except UnboundLocalError:
        return "Não foi mapeado"
    
    return "Não foi mapeado"



def buscar_produtos_por_isbn_ou_sku(valor: str):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="books"
    )
    cursor = db.cursor(dictionary=True)


    if len(valor) < 11:
        query = "SELECT B FROM planilha1 WHERE A LIKE %s"
        cursor.execute(query, ('%' + valor + '%',))
        resultado_planilha1 = cursor.fetchall()

        if resultado_planilha1:
            isbn = resultado_planilha1[0]['B']
            print("Resultado da tabela planilha1:", isbn)
        else:
            cursor.close()
            db.close()
            print("Não encontrou os dados")
            return []

    else:
        isbn = valor

    print(isbn)

    query = "SELECT * FROM produtos WHERE isbn = %s"
    cursor.execute(query, (isbn,))
    resultado_produtos = cursor.fetchall()

    todos_produtos = []

    if resultado_produtos:
        for produto in resultado_produtos:
            numero_livro = int(produto.get('numero'))
            if numero_livro:
                localizacao = localizar_livro(numero_livro)
                produto['localizacao'] = localizacao
                produto['local'] = 'down'
            todos_produtos.append(produto)

    # Segunda consulta na tabela 'produtos_up'
    query = "SELECT * FROM produtos_up WHERE isbn = %s"
    cursor.execute(query, (isbn,))
    resultado_produtos_up = cursor.fetchall()

    if resultado_produtos_up:
        for produto in resultado_produtos_up:
            numero_livro = int(produto.get('numero'))
            if numero_livro:
                localizacao = localizar_livro_up(numero_livro)
                produto['localizacao'] = localizacao
                produto['local'] = 'up'
            todos_produtos.append(produto)
    print(todos_produtos)
    return todos_produtos


def inserir_pedidos_de_vendas(dados_do_pedido):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="books"
    )
    
    cursor = db.cursor()
    
    sql = """
        INSERT INTO pedidos (isbn, pedido, titulo, quantidade, numero, localizacao, local)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    valores = (
        dados_do_pedido["isbn"],
        dados_do_pedido["pedido"],
        dados_do_pedido["titulo"],
        dados_do_pedido["quantidade"],
        dados_do_pedido["numero"],
        dados_do_pedido["localizacao"],
        dados_do_pedido["local"]
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


def buscar_pedidos_de_vendas():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="books"
    )
    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM pedidos"
    cursor.execute(query)
    resultado_pedidos = cursor.fetchall()

    cursor.close()
    db.close()

    return resultado_pedidos

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "produtos": None})

@app.post("/buscar", response_class=HTMLResponse)
async def buscar(request: Request, isbn: str = Form(...)):
    produtos = buscar_produtos_por_isbn_ou_sku(isbn)
    return templates.TemplateResponse("index.html", {"request": request, "produtos": produtos})

@app.post("/receber_callback", response_class=JSONResponse)
async def receber_callback(request: Request):
    try:
        dados_extraidos = await request.json()

        for item in dados_extraidos:
            isbn = item.get("isbn")
            quantidade = str(item.get("quantidade"))[0]
            produto = buscar_produtos_por_isbn_ou_sku(isbn)
            if produto and item.get("situacao") == "Em andamento":
                for prod in produto:
                    produtos_recebidos = {
                        "isbn": isbn,
                        "pedido": item.get("numero_do_pedido"),
                        "titulo": item.get("descricao"),
                        "quantidade": quantidade,
                        "numero": prod["numero"],
                        "localizacao": prod["localizacao"],
                        "local": prod["local"]
                    }
                    break

            else:
                produtos_recebidos = ""
        print(produtos_recebidos)
        if produtos_recebidos:
            inserir_pedidos_de_vendas(produtos_recebidos)
        
        return {"message": "Dados recebidos e armazenados com sucesso."}
    except Exception as e:
        print(f"Erro ao processar dados: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao processar a requisição")

@app.get("/produtos_recebidos", response_class=HTMLResponse)
async def exibir_produtos_recebidos(request: Request):
    todos_pedidos = buscar_pedidos_de_vendas()
    return templates.TemplateResponse("index_call.html", {"request": request, "produtos": todos_pedidos})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
 