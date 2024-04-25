import sqlite3

def conectar():
    return sqlite3.connect('financas.db')

def excluir_categoria(id_categoria):
    conn = conectar()
    cursor = conn.cursor()

    try:        ##procura a categoria e retorna ela em 'categoria'
        res = cursor.execute(f"SELECT id FROM categorias WHERE id = {id_categoria}")
        categoria = res.fetchone
    
        if not categoria:   
            print("Categoria não encontrada!")  ##se estiver vazia
            return

        print(f"Categoria encontrada! ID: {id_categoria}.")
            ##função do sqlite3 para deletar pelo seu id
        cursor.execute(f"DELETE FROM categorias WHERE id = {id_categoria}")
        conn.commit()
        print(f"Categoria excluída com sucesso!")
    
    except Exception as e:
        print("Erro ao tentar excluir: ", e)
    
    finally:
        conn.close()


def verificar_categoria(nome):
    conn = conectar()
    cursor = conn.cursor()
                            ##procura a categoria pelo nome
    cursor.execute(f"SELECT id FROM categorias WHERE nome = ?", (nome,))
    categoria = cursor.fetchone()

    conn.close()

    if categoria:   ##se categoria houver valor, então verdadeiro
        return True
    else:           ##senão, falso
        return False
    


def criar_categoria(nome):
    conn = conectar()
    cursor = conn.cursor()
        ##caso a função de verificar retorne verdadeiro
    if verificar_categoria(nome):
        print("Categoria existente!")
        return
    
    try:        ##insere na categoria o nome da nova
        cursor.execute(f"INSERT INTO categorias (nome) VALUES (?)", (nome,))
        conn.commit()
        print("Categoria adicionada com sucesso!")

    except Exception as e:
        print("Erro ao tentar adicionar categoria: ", e)

    finally:
        conn.close()

def listar_categorias():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM categorias")
    categorias = cursor.fetchall()

    conn.close()
    return categorias


def inserir_ganho(descricao, valor, categoria_id, data):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(f"INSERT INTO ganhos (descricao, valor, categoria_id, data) VALUES (?, ?, ?, ?)", (descricao, valor, categoria_id, data))
        conn.commit()
        print("Ganho cadastrado com sucesso!")

    except Exception as e:
        print("Erro ao tentar adicionar ganho: ", e)
    
    finally:
        conn.close()

def inserir_gasto(descricao, valor, categoria_id, data):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO gastos (descricao, valor, categoria_id, data) VALUES (?, ?, ?, ?)", (descricao, valor, categoria_id, data))
        conn.commit()
        print("Gasto cadastrado com sucesso!")

    except Exception as e:
        print("Erro ao tentar adicionar gasto: ", e)

    finally:
        conn.close


def saldo_mensal(mes, ano):

    conn = conectar()
    cursor = conn.cursor()

    total_ganhos = 0.0
    total_gastos = 0.0
    saldo = 0.0


    cursor.execute(f"SELECT SUM(valor) FROM ganhos WHERE strftime('%m-%Y', data) = ?", (f"{mes:02d}-{ano}",))
    res_ganhos = cursor.fetchone()

    if res_ganhos:
        total_ganhos = res_ganhos[0] or 0

    cursor.execute(f"SELECT SUM(valor) FROM gastos WHERE strftime('%m-%Y', data) = ?", (f"{mes:02d}-{ano}",))
    res_gastos = cursor.fetchone()

    if res_gastos:
        total_gastos = res_gastos[0] or 0

    total_ganhos = round(total_ganhos, 2)
    total_gastos = round(total_gastos, 2)
    print(f"Total ganho: R$ {total_ganhos}")
    print(f"Total gasto: R$ {total_gastos}")

    saldo = total_ganhos - total_gastos

    conn.close()

    return round(saldo, 2)


def saldo_total():
    conn = conectar()
    cursor = conn.cursor()

    total_ganhos = 0.0
    total_gastos = 0.0
    ##seleciona de todos os ganhos
    cursor.execute(f"SELECT * from ganhos")

    print("Ganhos:")
    print(f"{'Descrição':^30} | {'Valor':^6} | {'Data':12}")
    print(f"{'-'*30} | {'-'*6} | {'-'*12}")

    for row in cursor.fetchall():
        print(f"{row[1]:<30} | {row[2]:^6.2f} | {row[4]:>12}")
        total_ganhos += row[2]

    ##seleciona de todos os gastos
    cursor.execute(f"SELECT * from gastos")
    print("\nGastos:")
    print(f"{'Descrição':^30} | {'Valor':^6} | {'Data':12}")
    print(f"{'-'*30} | {'-'*6} | {'-'*12}")

    for row in cursor.fetchall():
        print(f"{row[1]:<30} | {row[2]:^6.2f} | {row[4]:>12}")
        total_gastos += row[2]

    conn.close()

    total = total_ganhos - total_gastos

    return total


def gasto_categoria(id_categoria):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT g.descricao, g.valor, c.nome FROM gastos g INNER JOIN categorias c ON g.categoria_id = c.id WHERE c.id = {id_categoria} ORDER BY g.data")

    gastos_por_categoria = {}

    for row in cursor.fetchall():
        descricao = row[0]
        valor = row[1]
        categoria = row[2]

        if categoria not in gastos_por_categoria:
            gastos_por_categoria[categoria] = []

        gastos_por_categoria[categoria].append((descricao, valor))

    conn.close()

    return gastos_por_categoria


def listar_gasto_mes(mes, ano):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT descricao, valor, data FROM gastos WHERE strftime('%m-%Y', data) = ?", (f"{mes:02d}-{ano}", ))
    gastos = cursor.fetchall()

    cursor.execute("SELECT SUM(valor) FROM gastos WHERE strftime('%m-%Y', data) = ?", (f"{mes:02d}-{ano}", ))
    total_gasto = cursor.fetchone()

    total = total_gasto[0]
    total = round(total, 2)

    conn.close()

    return gastos, total

def listar_ganho_mes(mes, ano):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT descricao, valor, data FROM ganhos WHERE strftime('%m-%Y', data) = ?", (f"{mes:02d}-{ano}", ))
    ganhos = cursor.fetchall()

    cursor.execute(f"SELECT SUM(valor) FROM ganhos WHERE strftime('%m-%Y', data) = ?", (f"{mes:02d}-{ano}", ))
    total_ganho = cursor.fetchone()

    total = total_ganho[0]
    total = round(total, 2)

    conn.close()

    return ganhos, total

def def_mes(mes):
    str = ""
    if (mes == 1):
        str = "Janeiro"
    elif (mes == 2):
        str = "Fevereiro"
    elif (mes == 3):
        str = "Março"
    elif (mes == 4):
        str = "Abril"
    elif (mes == 5):
        str = "Maio"
    elif (mes == 6):
        str = "Junho"
    elif (mes == 7):
        str = "Julho"
    elif (mes == 8):
        str = "Agosto"
    elif (mes == 9):
        str = "Setembro"
    elif (mes == 10):
        str = "Outubro"
    elif (mes == 11):
        str = "Novembro"
    elif (mes == 12):
        str = "Dezembro"
    else:
        print("Mês não encontrado!")
    
    return str