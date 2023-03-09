import re
from prettytable import PrettyTable

def nomes_e_apelidos():
    file = open("processos.txt", "r")
    dict_pnomes = dict()
    dict_apelidos = dict()
    
    for line in file:
        m_ano = re.match(r"\d+::(?P<ano>\d+)-\d{2}-\d{2}::([A-Z][a-z]*) ([A-Z][a-z]* ){0,}([A-Z][a-z]*)", line)
        fall_nomes = re.findall(r"::([A-Z][a-z]*) ([A-Z][a-z]* ){0,}([A-Z][a-z]*)", line)
        
        if m_ano is not None and fall_nomes is not None:
            ano = int(m_ano.group('ano'))
            seculo = (ano - 1) // 100 + 1

            fall_nomes = fall_nomes[:3]
            for match in fall_nomes:
                primeiro_nome = match[0]
                apelido = match[-1]
                
                if seculo in dict_pnomes:
                    if primeiro_nome in dict_pnomes[seculo]:
                        dict_pnomes[seculo][primeiro_nome] += 1
                    else:
                        dict_pnomes[seculo][primeiro_nome] = 1
                else:
                    dict_pnomes[seculo] = dict()
                    dict_pnomes[seculo][primeiro_nome] = 1
                    
                if seculo in dict_apelidos:
                    if apelido in dict_apelidos[seculo]:
                        dict_apelidos[seculo][apelido] += 1
                    else:
                        dict_apelidos[seculo][apelido] = 1
                else:
                    dict_apelidos[seculo] = dict()
                    dict_apelidos[seculo][apelido] = 1     
    
    file.close()
    
    dict_pnomes = dict(sorted(dict_pnomes.items(), reverse=True))
    for seculo in dict_pnomes:
        dict_pnomes[seculo] = dict(sorted(dict_pnomes[seculo].items(), key=lambda x: x[1], reverse=True))
    
    dict_apelidos = dict(sorted(dict_apelidos.items(), reverse=True))
    for seculo in dict_apelidos:
        dict_apelidos[seculo] = dict(sorted(dict_apelidos[seculo].items(), key=lambda x: x[1], reverse=True))

    return (dict_pnomes, dict_apelidos)


def print_top5_nomes_por_seculo(table_title, table_fields, data):
    for seculo in data:
        if len(data[seculo]) > 0:    
            table = PrettyTable()
            table.title = table_title + " " + str(seculo)
            table.field_names = table_fields
            
            total = sum(data[seculo].values())
            pos = 1
            ref_value = None
            
            i = 0
            for nome in data[seculo]:
                freq = data[seculo][nome]
                
                if ref_value is None:
                    ref_value = freq

                elif freq < ref_value:
                    pos = i+1;
                    ref_value = freq
            
                if pos <= 5:
                    percentage = freq / total * 100
                    
                    precision = 2
                    while round(percentage, precision) == 0.00:
                        precision += 1
                        
                    table.add_row([pos, nome, freq, '{:.{}f} %'.format(percentage, precision)])
                
                else:
                    break
                
                i+=1
                
            print(table)
            print("\n", end='')
    
    
dict_pnomes, dict_apelidos = nomes_e_apelidos()
print_top5_nomes_por_seculo("Top 5 de primeiros nomes no século", ["Pos.", "Primeiro nome", "Frequência", "Percentagem (%)"], dict_pnomes)
print("\n")
print_top5_nomes_por_seculo("Top 5 de apelidos no século", ["Pos.", "Apelido", "Frequência", "Percentagem (%)"], dict_apelidos)
