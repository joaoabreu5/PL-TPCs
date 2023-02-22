from prettytable import PrettyTable
import matplotlib.pyplot as plt
import os

def read_file():
    data = dict()
    data['D'] = []
    data['ND'] = []
    
    file = open("myheart.csv", "r")
    i = 0
    for line in file:
        if i>0:
            append = True
            dados_linha = line.strip().split(",")
            if len(dados_linha) >= 6:
                
                idade = dados_linha[0]
                if idade.isnumeric():
                    idade = int(idade)
                else:
                    append = False
                    
                sexo = dados_linha[1]
                if sexo != 'M' and sexo != 'F':
                    append = False

                tensao = dados_linha[2]
                if tensao.isnumeric():
                    tensao = int(tensao)
                else:
                    append = False
                    
                colestrol = dados_linha[3]
                if colestrol.isnumeric():
                    colestrol = int(colestrol)
                else:
                    append = False
                
                batimento = dados_linha[4]
                if batimento.isnumeric():
                    batimento = int(batimento)
                else:
                    append = False
                
                if dados_linha[5] == '1':
                    temDoenca = True
                elif dados_linha[5] == '0':
                    temDoenca = False
                else:
                    append = False
                    
                if append is True:
                    if temDoenca is True:
                        data['D'].append((idade,sexo,tensao,colestrol,batimento))
                    elif temDoenca is False:
                        data['ND'].append((idade,sexo,tensao,colestrol,batimento))                    
        i += 1
        
    file.close()
    return data

def dist_sexo(data):
    dist_sexo = dict()
    dist_sexo['Masculino'] = 0
    dist_sexo['Feminino'] = 0

    for tuplo in data:
        sexo = tuplo[1]
        if sexo == 'M':
            dist_sexo['Masculino'] += 1
        elif sexo == 'F':
            dist_sexo['Feminino'] += 1
        
    return dist_sexo

def dist_idade(data):
    dist_idade = dict()
    x1_idade_min = 30
    x1_idade_max = None

    for tuplo in data:
        idade = tuplo[0]
        int_idade = (idade//5*5, (idade//5+1)*5-1)
        if int_idade not in dist_idade:
            dist_idade[int_idade] = 1
        else:
            dist_idade[int_idade] += 1
        
        if int_idade[0] < x1_idade_min:
            x1_idade_min = int_idade[0]
        
        if x1_idade_max is None:
            x1_idade_max = int_idade[0]
        elif int_idade[0] > x1_idade_max:
            x1_idade_max = int_idade[0]
    
    if x1_idade_max is not None:
        i = x1_idade_min
        while i<=x1_idade_max:
            if (i,i+4) not in dist_idade:
                dist_idade[(i,i+4)] = 0
            i+=5
                
    return dict(sorted(dist_idade.items()))

def colestrol_min_max(data):
    colestrol_min = None
    colestrol_max = None
    for tuplo in data:
        colestrol = tuplo[3]
        
        if colestrol_min is None:
            colestrol_min = colestrol
        elif colestrol < colestrol_min:
            colestrol_min = colestrol
        
        if colestrol_max is None:
            colestrol_max = colestrol
        elif colestrol > colestrol_max:
            colestrol_max = colestrol
            
    return (colestrol_min, colestrol_max)

def dist_colestrol(data):
    colestrol_min, colestrol_max = colestrol_min_max(data)
    dist_colestrol = dict()
    
    i=colestrol_min
    while i<=colestrol_max:
        dist_colestrol[(i,i+9)] = 0
        i+=10
    
    for tuplo in data:
        colestrol = tuplo[3]
        int_colestrol = (colestrol_min+(colestrol-colestrol_min)//10*10, colestrol_min+((colestrol-colestrol_min)//10+1)*10-1)
        if int_colestrol not in dist_colestrol:
            dist_colestrol[int_colestrol] = 1
        else:
            dist_colestrol[int_colestrol] += 1
                
    return dict(sorted(dist_colestrol.items()))

def print_distribuicao(table_title, table_fields, data):
    table = PrettyTable()
    table.title = table_title
    table.field_names = table_fields
    
    total = sum(data.values())
    for key in data:
        percentage = data[key] / total * 100
        table.add_row([key, data[key], '{:.2f} %'.format(percentage)])

    print(table)

def tuplo_para_intervalo(t):
    return f"[{t[0]}-{t[1]}]"

def print_distribuicao_int(table_title, table_fields, data):
    table = PrettyTable()
    table.title = table_title
    table.field_names = table_fields

    total = sum(data.values())
    for key in data:
        percentage = data[key] / total * 100
        table.add_row([tuplo_para_intervalo(key), data[key], '{:.2f} %'.format(percentage)])

    print(table)
    
def grafico_barras(titulo, eixo_x, eixo_y, data):
    x_values = [str(key) for key in data.keys()]
    y_values = data.values()

    barras = plt.bar(x_values, y_values)
    plt.bar_label(barras, labels=y_values)

    manager = plt.get_current_fig_manager()
    manager.set_window_title(titulo)

    plt.title(titulo)
    plt.xlabel(eixo_x)
    plt.ylabel(eixo_y)
    
    plt.show()
    
def grafico_barras_int(titulo, eixo_x, eixo_y, data):
    x_values = [tuplo_para_intervalo(key) for key in data.keys()]
    y_values = data.values()   

    barras = plt.bar(x_values, y_values)
    plt.bar_label(barras, labels=y_values)
    
    manager = plt.get_current_fig_manager()
    manager.set_window_title(titulo)

    plt.title(titulo)
    plt.xlabel(eixo_x)
    plt.ylabel(eixo_y)
    plt.xticks(rotation=45)
    
    plt.show()
    
def grafico_circular(titulo, data):
    tuplos_filtrados = [(key,value) for (key,value) in zip(data.keys(),data.values()) if value > 0]
    filtered_labels = [x[0] for x in tuplos_filtrados]
    filtered_values = [x[1] for x in tuplos_filtrados]
    
    plt.pie(filtered_values, labels=filtered_labels, autopct='%.2f %%')
    
    total = sum(filtered_values)
    plt.legend(
        labels=[('%s, %.2f %%') % (label, (value/total)*100) for (label,value) in tuplos_filtrados],
        prop={'size': 11},
        loc='upper left', 
        bbox_to_anchor=(-0.4, 1.03)
    )

    manager = plt.get_current_fig_manager()
    manager.set_window_title(titulo)   
    plt.title(titulo)

    plt.show()
    
def grafico_circular_int(titulo, data):
    tuplos_filtrados = [(tuplo_para_intervalo(key),value) for (key,value) in zip(data.keys(),data.values()) if value > 0]
    filtered_labels = [x[0] for x in tuplos_filtrados]
    filtered_values = [x[1] for x in tuplos_filtrados]
    
    plt.pie(filtered_values, labels=filtered_labels, autopct='%.2f %%')
    
    total = sum(filtered_values)
    plt.legend(
        labels=[('%s, %.2f %%') % (label, (value/total)*100) for (label,value) in tuplos_filtrados],
        prop={'size': 11},
        loc='upper left', 
        bbox_to_anchor=(-0.4, 1.03)
    )
        
    manager = plt.get_current_fig_manager()
    manager.set_window_title(titulo)
    plt.title(titulo)
    
    plt.show()

def menu():
    data = read_file()
    dict_dist_sex = dist_sexo(data['D'])
    dict_dist_idade = dist_idade(data['D'])
    dict_dist_colestrol = dist_colestrol(data['D'])
    
    table = PrettyTable()
    table.title = "Menu"
    table.field_names = ["Nº", "Opção"]
    table.align['Opção'] = 'l'
    
    table.add_row(["", "Tabela"])
    table.add_row(["---", "-------------------------------------------------------"])
    table.add_row(["1", "Distribuição da doença por sexo"])
    table.add_row(["2", "Distribuição da doença por escalão etário"])
    table.add_row(["3", "Distribuição da doença por nível de colestrol"])
    table.add_row(["---", "-------------------------------------------------------"])
    table.add_row(["", "Gráfico de Barras"])
    table.add_row(["---", "-------------------------------------------------------"])
    table.add_row(["4", "Distribuição da doença por sexo"])
    table.add_row(["5", "Distribuição da doença por escalão etário"])
    table.add_row(["6", "Distribuição da doença por nível de colestrol"])
    table.add_row(["---", "-------------------------------------------------------"])
    table.add_row(["", "Gráfico Circular"])
    table.add_row(["---", "-------------------------------------------------------"])    
    table.add_row(["7", "Distribuição da doença por sexo"])
    table.add_row(["8", "Distribuição da doença por escalão etário"])
    table.add_row(["9", "Distribuição da doença por nível de colestrol"])
    table.add_row(["---", "-------------------------------------------------------"])
    table.add_row(["0", "Sair"])
    
    saida = -1
    opcao_invalida = False
    while saida != 0:
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        
        if not opcao_invalida:
            print(table)

        option_flag = False
        opcao = input("\nIntroduza a sua opção: ")
        while not option_flag:
            try:
                opcao = int(opcao)
                if opcao < 0 or opcao > 9:
                    print("Opção inválida!")
                    option_flag = False
                    opcao = input("\nIntroduza novamente a sua opção: ")
                else:
                    option_flag = True
            except ValueError:
                print("Opção inválida!")
                option_flag = False
                opcao = input("\nIntroduza novamente a sua opção: ")

        saida = opcao
        opcao_invalida = False
        
        if saida == 1:
            os.system('cls' if os.name in ('nt', 'dos') else 'clear')
            print_distribuicao("Distribuição da doença por sexo", ["Sexo", "Frequência", "Percentagem (%)"], dict_dist_sex)
            input("\nPrima ENTER para continuar... ")

        elif saida == 2:
            os.system('cls' if os.name in ('nt', 'dos') else 'clear')
            print_distribuicao_int("Distribuição da doença por escalão etário", ["Idade", "Frequência", "Percentagem (%)"], dict_dist_idade)
            input("\nPrima ENTER para continuar... ")

        elif saida == 3:
            os.system('cls' if os.name in ('nt', 'dos') else 'clear')
            print_distribuicao_int("Distribuição da doença por nível de colestrol", ["Colestrol", "Frequência", "Percentagem (%)"], dict_dist_colestrol)
            input("\nPrima ENTER para continuar... ")

        elif saida == 4:
            grafico_barras("Distribuição da doença por sexo", "Sexo", "Frequência", dict_dist_sex)

        elif saida == 5:
            grafico_barras_int("Distribuição da doença por escalão etário", "Idade", "Frequência", dict_dist_idade)

        elif saida == 6:
            grafico_barras_int("Distribuição da doença por nível de colestrol", "Colestrol", "Frequência", dict_dist_colestrol)

        elif saida == 7:
            grafico_circular("Distribuição da doença por sexo", dict_dist_sex)

        elif saida == 8:
            grafico_circular_int("Distribuição da doença por escalão etário", dict_dist_idade)

        elif saida == 9:
            grafico_circular_int("Distribuição da doença por nível de colestrol", dict_dist_colestrol)

        elif saida != 0:
            print("Opção inválida!")
            opcao_invalida = True


if __name__ == "__main__":
    menu()
