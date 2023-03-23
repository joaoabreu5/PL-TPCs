import re
import sys
from decimal import Decimal

def saldo_to_string(saldo):
    cent = int((saldo - int(saldo)) * 100)
    eur = int(saldo)
    return str(eur) + 'e' + str(cent) + 'c'
    
def soma_moedas(lista_moedas):
    valor = Decimal('0')
    moedas_invalidas = []
    
    for moeda in lista_moedas:
        if moeda == "1c":
            valor += Decimal('0.01')
                      
        elif moeda == "2c":
            valor += Decimal('0.02')
            
        elif moeda == "5c":
            valor += Decimal('0.05')
            
        elif moeda == "10c":
            valor += Decimal('0.10')
            
        elif moeda == "20c":
            valor += Decimal('0.20')
            
        elif moeda == "50c":
            valor += Decimal('0.50')
            
        elif moeda == "1e":
            valor += Decimal('1')
            
        elif moeda == "2e":
            valor += Decimal('2')
            
        else:
            moedas_invalidas.append(moeda)

    return (valor, moedas_invalidas)

def cabine_telefonica():
    estado = True
    on = False
    saldo = Decimal('0')
    
    while estado:
        line = sys.stdin.readline()
        if re.match(r"(?i)LEVANTAR", line):
            on = True
            print('maq: "Introduza moedas."')
            
        elif re.match(r"(?i)POUSAR", line):
            if on:
                on = False
                estado = False
                print('maq: "troco = ' + saldo_to_string(saldo) + '; Volte sempre!"')
            else:
                print('maq: "O auscultador do telefone não foi levantado. Queira levantar o auscultador do mesmo!"')
            
        elif re.match(r"(?i)MOEDA *=", line):
            if on:
                fall_moedas = re.findall(r"\b[0-9]+[ce]\b", line)
                soma, moedas_invalidas = soma_moedas(fall_moedas)
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
                
        elif re.match(r"(?i)T *= *[0-9]+", line):
            if on:
                num = re.search(r"[0-9]+", line)
                num = num.group()
                
                if len(num) == 9:
                    if num[:3] == "601" or num[:3] == "604":
                        print('maq: "Esse número não é permitido neste telefone. Queira discar novo número!"')
                    
                    elif num[0] == "2":
                        if saldo >= 0.25:
                            saldo -= Decimal('0.25')
                            print('maq: "saldo = ' + saldo_to_string(saldo) + '"')
                        else:
                            print('maq: "Saldo insuficiente."')
                        
                    elif num[:3] == "800":
                        print('maq: "saldo = ' + saldo_to_string(saldo) + '"')
                    
                    elif num[:3] == "808":
                        if saldo >= 0.10:
                            saldo -= Decimal('0.10')
                            print('maq: "saldo = ' + saldo_to_string(saldo) + '"')
                        else:
                            print('maq: "Saldo insuficiente."')

                elif num[:2] == "00":
                    if saldo >= 1.5:
                        saldo -= Decimal('1.5')
                        print('maq: "saldo = ' + saldo_to_string(saldo) + '"')
                    else:
                        print('maq: "Saldo insuficiente."')
                            
                else:
                    print('maq: "Esse número não é permitido neste telefone. Queira discar novo número!"')
                    
            else:
                print('maq: "O auscultador do telefone não foi levantado. Queira levantar o auscultador do mesmo!"')
            
        elif re.match(r"(?i)ABORTAR", line):
            if on:
                print('maq: "troco = ' + saldo_to_string(saldo) + '; Volte sempre!"')
            on = False
            estado = False
        
        else:
            print('maq: "Comando não suportado. Queira introduzir um novo comando!"')

          
cabine_telefonica()
