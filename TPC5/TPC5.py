import re
from decimal import Decimal

def saldo_to_string(saldo):
    cent = int((saldo - int(saldo)) * 100)
    eur = int(saldo)
    return str(eur) + 'e' + str(cent) + 'c'

  
def soma_moedas(lista_moedas):
    valor = Decimal('0')
    moedas_invalidas = []

    i = 0
    for moeda in lista_moedas:
        match_moeda = True
        moeda = moeda.strip()
        
        if i == len(lista_moedas) - 1:
            match_moeda = re.match(r"([0-9a-zA-Z]+)", moeda)
            if match_moeda is not None:
                moeda = match_moeda.group(1)
            
        if match_moeda is not None:
            moeda_l = moeda.lower()
            
            if moeda_l == "1c":
                valor += Decimal('0.01')
                        
            elif moeda_l == "2c":
                valor += Decimal('0.02')
                
            elif moeda_l == "5c":
                valor += Decimal('0.05')
                
            elif moeda_l == "10c":
                valor += Decimal('0.10')
                
            elif moeda_l == "20c":
                valor += Decimal('0.20')
                
            elif moeda_l == "50c":
                valor += Decimal('0.50')
                
            elif moeda_l == "1e":
                valor += Decimal('1')
                
            elif moeda_l == "2e":
                valor += Decimal('2')
                
            elif moeda not in moedas_invalidas:
                    moedas_invalidas.append(moeda)
        
        elif moeda not in moedas_invalidas:
                    moedas_invalidas.append(moeda)
    
        i += 1

    return (valor, moedas_invalidas)


def moedas_troco(troco):
    dict_moedas = {'2e': 200, '1e': 100, '50c': 50, '20c': 20, '10c': 10, '5c': 5, '2c': 2, '1c': 1}

    troco_cent = int(troco * 100)
    moedas_troco = dict()
    
    for moeda, valor_cent in dict_moedas.items():
        num_moedas = troco_cent // valor_cent
        
        if num_moedas > 0:
            moedas_troco[moeda] = num_moedas
            troco_cent -= num_moedas * valor_cent
        
    return moedas_troco


def imprime_troco(troco):
    if troco > 0:
        dict_moedas_troco = moedas_troco(troco)
        print('maq: "troco = ', end='')
        
        i = 0
        for moeda, num in dict_moedas_troco.items():
            if i == 0:
                print(f'{num}x{moeda}', end='')
            else:
                print(f', {num}x{moeda}', end='')
            i += 1
            
        print('; Volte sempre!"')
        
    elif troco == 0:
        print('maq: "troco = ' + saldo_to_string(troco) + '; Volte sempre!"')

      
def cabine_telefonica():
    estado = True
    on = False
    saldo = Decimal('0')
    
    while estado:
        line = input()
        if re.match(r"(?i)\s*LEVANTAR\b", line):
            if not on:
                print('maq: "Introduza moedas."')
            else:
                print('maq: "O auscultador já se encontra levantado."')
            on = True
            
        elif re.match(r"(?i)\s*POUSAR\b", line):
            if on:
                on = False
                estado = False
                imprime_troco(saldo)
            else:
                print('maq: "O auscultador do telefone não foi levantado. Queira levantar o auscultador do mesmo!"')
            
        elif re.match(r"(?i)\s*MOEDA\b", line):
            if on:
                ms = re.match(r"(?i)\s*MOEDA\b", line).span()
                string_moedas = line[ms[1]:]
                
                lista_moedas = []
                if string_moedas.strip() != "":
                    lista_moedas = re.split(r",", string_moedas)
                else:
                    print('maq: "Não introduziu um quaisquer moedas. Queira introduzir moedas!"')
                
                soma, moedas_invalidas = soma_moedas(lista_moedas)
                saldo += soma
                
                if len(moedas_invalidas) == 0:
                    print('maq: "saldo = ' + saldo_to_string(saldo) + '"')                
                
                else:
                    print('maq: "', end='')
                    for moeda in moedas_invalidas:
                        print(moeda + ' - moeda inválida; ', end='')
                    print('saldo = ' + saldo_to_string(saldo) + '"')        
                    
            else:
                print('maq: "O auscultador do telefone não foi levantado. Queira levantar o auscultador do mesmo!"')
                
        elif re.match(r"(?i)\s*T *=", line):
            if on:
                num = re.search(r"(?i)\s*T *= *([0-9]+)", line)
                
                if num is not None:
                    num = num.group(1)
                    
                    if len(num) == 9:
                        if num[0] == "2":
                            if saldo >= 0.25:
                                saldo -= Decimal('0.25')
                                print('maq: "saldo = ' + saldo_to_string(saldo) + '"')
                            else:
                                print('maq: "Saldo insuficiente. Custo da chamada = 0e25c."')
                            
                        elif num[:3] == "800":
                            print('maq: "saldo = ' + saldo_to_string(saldo) + '"')
                        
                        elif num[:3] == "808":
                            if saldo >= 0.10:
                                saldo -= Decimal('0.10')
                                print('maq: "saldo = ' + saldo_to_string(saldo) + '"')
                            else:
                                print('maq: "Saldo insuficiente. Custo da chamada = 0e10c."')
                        
                        else:
                            print('maq: "Esse número não é permitido neste telefone. Queira discar novo número!"')

                    elif num[:2] == "00":
                        if saldo >= 1.5:
                            saldo -= Decimal('1.5')
                            print('maq: "saldo = ' + saldo_to_string(saldo) + '"')
                        else:
                            print('maq: "Saldo insuficiente. Custo da chamada = 1e50c."')
                                
                    else:
                        print('maq: "Esse número não é permitido neste telefone. Queira discar novo número!"')
                
                else:
                    print('maq: "Não introduziu um número de telefone. Queira discar um número!"')
                    
            else:
                print('maq: "O auscultador do telefone não foi levantado. Queira levantar o auscultador do mesmo!"')
            
        elif re.match(r"(?i)\s*ABORTAR\b", line):
            if on:
                imprime_troco(saldo)
            on = False
            estado = False
        
        else:
            print('maq: "Comando não suportado. Queira introduzir um novo comando!"')


cabine_telefonica()
