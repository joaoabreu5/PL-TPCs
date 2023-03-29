import ply.lex as lex
import sys

tokens = ['ID', 'INT', 'INT_TYPE', 'MAIS', 'MENOS', 'VEZES', 'DIVIDIR', 'IGUAL', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
          'PONTO_VIRG', 'VIRG', 'DOIS_PONTOS', 'PAREN_ESQ', 'PAREN_DIR', 'PAREN_RET_ESQ', 'PAREN_RET_DIR', 'CHAVETA_ESQ', 'CHAVETA_DIR',
          'PROGRAM', 'FUNCTION', 'PRINT', 'IN', 'IF', 'ELSE', 'FOR', 'WHILE', 'NEWLINE', 'COMENTARIO', 'BLOCO_COMENTARIO']

t_MAIS = r'\+'
t_MENOS = r'-'
t_VEZES = r'\*'
t_DIVIDIR = r'/'
t_IGUAL = r'='
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_PONTO_VIRG = r';'
t_VIRG = r','
t_DOIS_PONTOS = r'\.\.'
t_PAREN_ESQ = r'\('
t_PAREN_DIR = r'\)'
t_PAREN_RET_ESQ = r'\['
t_PAREN_RET_DIR = r'\]'
t_CHAVETA_ESQ = r'\{'
t_CHAVETA_DIR = r'\}'
t_COMENTARIO = r'//.*'
t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_]\w*'
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_INT_TYPE(t):
    r'int\b'
    return t

def t_PROGRAM(t):
    r'program\b'
    return t

def t_FUNCTION(t):
    r'function\b'
    return t

def t_PRINT(t):
    r'print\b'
    return t

def t_IN(t):
    r'in\b'
    return t

def t_IF(t):
    r'if\b'
    return t

def t_ELSE(t):
    r'else\b'
    return t

def t_FOR(t):
    r'for\b'
    return t

def t_WHILE(t):
    r'while\b'
    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1

def t_BLOCO_COMENTARIO(t):
    r'/\*(.|\n)*\*/'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_error(t):
    print(f"Carácter inválido: '{t.value[0]}', linha {t.lexer.lineno};")
    t.lexer.skip(1)
    
def read_file(path):
    text = ""
    file = open(path, "r")
    for line in file:
        text += line
    file.close()
    return text    

def parse_code(code):
    lexer = lex.lex()
    lexer.input(code)

    while True:
        tok = lexer.token()
        if not tok: 
            break
        print(tok)
        
def main():
    if len(sys.argv) >= 2:
        file_path = sys.argv[1]
    else:
        file_path = input("Introduza o caminho do ficheiro a ler: ")
        
    text = read_file(file_path)
    print('----------------------------------------------------------------------')
    parse_code(text)
    
main()
