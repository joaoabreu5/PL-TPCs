import re
import json
import sys

def get_json_file_path(csv_file_path):
    fp_splited = re.split(r"\.", csv_file_path)
    json_file_path = ""
    
    if fp_splited is not None:
        for i in range(len(fp_splited)-1):
            json_file_path += fp_splited[i]
        json_file_path += ".json"
        
    return json_file_path


def is_numbers_list(lista):
    for n in lista:
        match = re.match(r"^[+-]?\d*\.?\d+$", str(n))
        if match is None:
            return False
               
    return True

def convert_str_list(lista):
    for i in range(len(lista)):
        lista[i] = float(lista[i])
        if lista[i].is_integer():
            lista[i] = int(lista[i])
    
    return lista

def manage_functions(funcao, lista):
    r = ""
    lista_nums = is_numbers_list(lista)
    
    if lista_nums:    
        if funcao == 'sum':
            r = sum(lista)
            if isinstance(r, float) and r.is_integer():
                r = int(r)
        elif funcao == 'media':
            r = sum(lista)/len(lista)
            if isinstance(r, float) and r.is_integer():
                r = int(r)
        elif funcao == 'max':
            r = max(lista)
            if isinstance(r, float) and r.is_integer():
                r = int(r)
        elif funcao == 'min':
            r = min(lista)
            if isinstance(r, float) and r.is_integer():
                r = int(r)
            
    return r
    
def convert_csv_to_json(file_path):
    file_read = open(file_path, "r")
    i = 0
    lista_dict_json = []
    campos = []
    for line in file_read:
        val_linha = re.split(r",(?![^{]*\})", line)
        
        if val_linha[-1][-1] == '\n':
            val_linha[-1] = val_linha[-1][0:-1]
        
        if i == 0:  
            campos = val_linha      
        else:
            dict_json = dict()
            j = 0
            while j < len(campos):
                val = val_linha[j]
                
                if val is not None:
                    match1 = re.match(r"(?P<nome>\w+){(?P<N>\d+),(?P<M>\d+)}::(?P<func>[a-zA-Z]+)", campos[j])
                    match2 = re.match(r"(?P<nome>\w+){(?P<N>\d+)}::(?P<func>[a-zA-Z]+)", campos[j])
                    match3 = re.match(r"(?P<nome>\w+){(?P<N>\d+),(?P<M>\d+)}", campos[j])
                    match4 = re.match(r"(?P<nome>\w+){(?P<N>\d+)}", campos[j])
                    
                    if match1:
                        N = int(match1.group('N'))
                        M = int(match1.group('M'))                        
                        aux = []
                        for k in range(j, j+M):
                            if val_linha[k] != "":
                                aux.append(val_linha[k])
                        
                        if len(aux) >= N and len(aux) <= M:
                            flag_lista_nums = is_numbers_list(aux)
                            if flag_lista_nums:    
                                aux = convert_str_list(aux)
                            
                            key = match1.group('nome') + '_' + match1.group('func')
                            dict_json[key] = manage_functions(match1.group('func'), aux)
                        
                        j += M+1
                        
                    elif match2:
                        N = int(match2.group('N'))                      
                        aux = []
                        for k in range(j, j+N):
                            if val_linha[k] != "":
                                aux.append(val_linha[k])

                        if len(aux) == N:
                            flag_lista_nums = is_numbers_list(aux)
                            if flag_lista_nums:    
                                aux = convert_str_list(aux)
                            
                            key = match2.group('nome') + '_' + match2.group('func')
                            dict_json[key] = manage_functions(match2.group('func'), aux)
                            
                        j += N+1
                    
                    elif match3:
                        N = int(match3.group('N'))
                        M = int(match3.group('M'))                        
                        aux = []
                        for k in range(j, j+M):
                            if val_linha[k] != "":
                                aux.append(val_linha[k])
                        
                        if len(aux) >= N and len(aux) <= M:
                            flag_lista_nums = is_numbers_list(aux)
                            if flag_lista_nums:    
                                aux = convert_str_list(aux)
                            
                            key = match3.group('nome')
                            dict_json[key] = aux
                            
                        j += M+1
                    
                    elif match4:
                        N = int(match4.group('N'))                      
                        aux = []
                        for k in range(j, j+N):
                            if val_linha[k] != "":
                                aux.append(val_linha[k])
                        
                        if len(aux) == N:
                            flag_lista_nums = is_numbers_list(aux)
                            if flag_lista_nums:    
                                aux = convert_str_list(aux)
                            
                            key = match4.group('nome')
                            dict_json[key] = aux
                        
                        j += N+1
                    
                    else:
                        dict_json[campos[j]] = val      
                        j += 1
                        
            lista_dict_json.append(dict_json)                 
        i += 1
        
    file_read.close()
    
    file_write = open(get_json_file_path(file_path), "w")
    json.dump(lista_dict_json, file_write, ensure_ascii=False, indent=2)
    file_write.close()


def main():
    if len(sys.argv) >= 2:
        convert_csv_to_json(sys.argv[1])
    else:
        file_path = input("Introduza o caminho do ficheiro .csv a converter: ")
        convert_csv_to_json(file_path)

main()
