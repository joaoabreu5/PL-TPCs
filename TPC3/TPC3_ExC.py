import re
from TPC3_ExA import print_distribuicao

def relacoes():
    file = open("processos.txt", "r")
    dict_relacoes = dict()

    for line in file:
        r = re.match(r"\d+::(?P<ano>\d+)-\d{2}-\d{2}::([A-Z][a-z]*) ([A-Z][a-z]* ){0,}([A-Z][a-z]*)", line)
        fall_relacoes = re.findall(r",([a-zA-z]+)((?: +[a-zA-z]+)*)\. +Proc.\d+\.", line)
        
        if r is not None:  
            for match in fall_relacoes:
                rel = ''
                for p in match:
                    rel += p
                
                if rel in dict_relacoes:
                    dict_relacoes[rel] += 1
                else:
                    dict_relacoes[rel] = 1
                        
    file.close()
    return dict(sorted(dict_relacoes.items(), key=lambda x: x[1], reverse=True))


dict_relacoes = relacoes()
print_distribuicao("Relações presentes em registos de processos", ["Relação", "Frequência", "Percentagem (%)"], dict_relacoes)
