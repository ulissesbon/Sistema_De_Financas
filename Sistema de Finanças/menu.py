import funcoes

def retornar():
    print("\nEscolha uma opção: ")
    print("1) VOLTAR")
    print("2) FECHAR")

    op = input("Opção: ")

    if op == '1':
        menu_principal()
    elif op == '2':
        print("Programa finalizado!")
        return
    else:
        print("Opção inválida!")
        menu_principal()

def menu_principal():

    print("\n_-⎺-_-⎺-_-⎺-_-⎺-_Menu inicial_-⎺-_-⎺-_-⎺-_-⎺-_\n")
    print(f"Escolha uma das opções:")
    print("1.  Adicionar categoria;")
    print("2.  Adicionar ganho;")
    print("3.  Adicionar gasto;")
    print("4.  Calcular saldo mensal;")
    print("5.  Listar ganhos mensal;")
    print("6.  Listar gastos mensal;")
    print("7.  Calcular saldo total;")
    print("8.  Mostrar gastos por categoria;")
    print("9.  Listar categorias;")
    print("10. Excluir categoria;")
    print("11. Sair.\n")

    op = input("Escolha uma opção: ")

    if op == '1':
        add_categoria()
    elif op == '2':
        add_ganho()
    elif op == '3':
        add_gasto()
    elif op == '4':
        saldo_mes()
    elif op == '5':
        ganho_mes()
    elif op == '6':
        gasto_mes()
    elif op == '7':
        total()
    elif op == '8':
        gasto_categoria()
    elif op == '9':
        lista_de_categorias()
        retornar()
    elif op == '10':
        excluir()
    elif op == '11':
        print("Programa finalizado!")
        return
    else:
        print("ERROR!\nEscolha uma opção válida!")
        menu_principal()



def add_categoria():
    nome = input("Adicionar categoria:\nDigite o nome da categoria: ")
    funcoes.criar_categoria(nome)
    retornar()

def add_ganho():
    print("Adicionar ganho:\n")
    descricao = input("Adicione uma descrição ao ganho: ")
    lista_de_categorias()
    categoria_id = int(input("Digite o id da categoria do ganho: "))
    valor = float(input("Digite o valor: "))
    data = input("Data(AAAA-MM-DD): ")
    
    funcoes.inserir_ganho(descricao, valor, categoria_id, data)
    print("Ganho cadastrado!")
    retornar()

def add_gasto():
    print("Adicionar gasto:\n")
    lista_de_categorias()
    descricao = input("Adicione uma descrição ao gasto: ")
    categoria_id = int(input("Digite o id da categoria do gasto: "))
    valor = float(input("Digite o valor: "))
    data = input("Data(AAAA-MM-DD): ")
    
    funcoes.inserir_gasto(descricao, valor, categoria_id, data)
    print("Gasto cadastrado!")
    retornar()

def saldo_mes():
    print("Saldo por mês:")
    ano = int(input("Digite o ano desejado: "))
    mes = int(input("Digite o mes desejado: "))

    nome = funcoes.def_mes(mes)
    saldo = funcoes.saldo_mensal(mes, ano)
    print(f"Saldo do mês de {nome} de {ano}: R${saldo}")
    retornar()


def ganho_mes():
    print("Ganho do mês:")
    ano = int(input("Digite o ano desejado: "))
    mes = int(input('Digite o mês desejado: '))

    ganho, total = funcoes.listar_ganho_mes(mes, ano)
    print("GANHOS:")
    print(f"{'Descrição':^30} | {'Valor':^10} | {'Data':^12}")
    print(f"{'-'*30} | {'-'*10} | {'-'*12}")
    for row in ganho:
        print(f"{row[0]:<30} | {row[1]:^10} | {row[2]:>12}")

    nome = funcoes.def_mes(mes)
    print(f"Total ganho em {nome} de {ano}: R${total}")
    retornar()


def gasto_mes():
    print("Gasto por mês:")
    ano = int(input("Digite o ano desejado: "))
    mes = int(input("Digite o mes desejado: "))

    gasto, total = funcoes.listar_gasto_mes(mes, ano)
    print("GASTOS:")
    print(f"{'Descrição':^30} | {'Valor':^10} | {'Data':^12}")
    print(f"{'-'*30} | {'-'*10} | {'-'*12}")
    for row in gasto:
        print(f"{row[0]:<30} | {row[1]:^10} | {row[2]:>12}")

    nome = funcoes.def_mes(mes)
    print(f"Total gastos em {nome} de {ano}: R${total}")
    retornar()


def total():
    saldo = funcoes.saldo_total()

    print(f"\nSaldo total: R${saldo}")

    retornar()


def gasto_categoria():
    print("Gastos por categoria:")
    lista_de_categorias()
    id = int(input("Digite o id da categoria: "))
    gastos_da_categoria = funcoes.gasto_categoria(id)


    for categoria, gastos in gastos_da_categoria.items():
        total_categoria = sum(gasto[1] for gasto in gastos)
        print(f"Categoria: {categoria}  === Total: R${total_categoria}.2f")
        print("Gastos:")
        print(f"{'Descrição':^30} | {'Valor':^8}")
        print(f"{'-'*30} | {'-'*8}")
        for gasto in gastos:
            print(f"{gasto[0]:<30} | R${gasto[1]}")
    retornar()


def lista_de_categorias():
    categorias = funcoes.listar_categorias()
    if categorias:
        print(f"{'ID':^3} | {'Categoria':^15}")
        print(f"{'-'*3} | {'-'*15}")
        for categoria in categorias:
            print(f"{categoria[0]:<3} | {categoria[1]}")
    else:
        print("Nenhuma categoria encontrada.")


def excluir():
    lista_de_categorias()
    id = int(input("Digite o id da categoria a ser excluida: "))
    funcoes.excluir_categoria(id)
    retornar()