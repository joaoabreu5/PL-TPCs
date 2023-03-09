import re
from prettytable import PrettyTable

def processos_ano():
    file = open("processos.txt", "r")
    proc_ano = dict()
    for line in file:
        r = re.match(r"\d+::(?P<ano>\d+)-\d{2}-\d{2}::([A-Z][a-z]*) ([A-Z][a-z]* ){0,}([A-Z][a-z]*)", line)
        if r is not None:
            ano = int(r.group('ano'))
            if ano in proc_ano:
                proc_ano[ano] += 1
            else:
                proc_ano[ano] = 1
                
    file.close()
    return dict(sorted(proc_ano.items(), key=lambda x: x[1], reverse=True))



def print_distribuicao(table_title, table_fields, data):
    table = PrettyTable()
    table.title = table_title
    table.field_names = table_fields
    
    total = sum(data.values())
    for key in data:
        percentage = data[key] / total * 100
        
        precision = 2
        while round(percentage, precision) == 0.00:
            precision += 1
 
        table.add_row([key, data[key], '{:.{}f} %'.format(percentage, precision)])

    print(table)


def main():
    proc_ano = processos_ano()
    print_distribuicao("Processos por ano", ["Ano", "Nº de Processos", "Percentagem (%)"], proc_ano)

if __name__ == '__main__':
    main()
    