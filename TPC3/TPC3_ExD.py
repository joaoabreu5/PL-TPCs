import re
import json

def first_20_registers_to_json():
    first_20_lines = []
    nome_campos = ['id','data','nome','pai','mãe','observações']
    
    read_file = open("processos.txt", "r")
    for line in read_file:
        r = re.match(r"\d+::(?P<ano>\d+)-\d{2}-\d{2}::([A-Z][a-z]*) ([A-Z][a-z]* ){0,}([A-Z][a-z]*)", line)
        if r is not None:
            campos = re.split("::", line)
            line_to_json = dict()
            for i in range(6):
                line_to_json[nome_campos[i]] = campos[i]
            first_20_lines.append(line_to_json)
        
        if len(first_20_lines) >= 20:
            break
    
    read_file.close()
        
    dict_processos = dict()
    dict_processos['processos'] = first_20_lines
    
    write_file = open("processos20.json", "w")
    json.dump(dict_processos, write_file, ensure_ascii=False, indent=2)    
    write_file.close()

            
first_20_registers_to_json()
