import sys

def read_stdin():
    text = ""
    for line in sys.stdin:
        text += line
    return text

def parse(text):
    numbers = []
    state_on = True
    last_3_chars = ""
    
    i = 0
    for line in text:
        for char in line:
            if state_on is True:
                if char.isnumeric():
                    if i == len(numbers):
                        numbers.append("")
                    if i < len(numbers):
                        numbers[i] += char 
                else:
                    if char == '=':
                        numbers.append('=')
                        i += 1
                    if i < len(numbers) and numbers[i] != "":
                        i += 1
                        
            if len(last_3_chars) < 3:
                last_3_chars += char
            else:
                last_3_chars = last_3_chars[1:3] + char
            
            if last_3_chars.lower() == "off":
                state_on = False
            elif last_3_chars.lower() == "on" or last_3_chars[1:3].lower() == "on":
                state_on = True
                
    return numbers

def imprime_resultado(numbers):
    soma = 0
    str_soma = ""
    first_n = True
    n_igual = 0
    
    for n in numbers:
        if n != '=':
            soma += int(n)
            if first_n is True:
                str_soma += n
            else:
                str_soma += " + " + n
            first_n = False 
        else:
            n_igual += 1
            str_soma = "[" + str(n_igual) + "º =] " + str_soma + " = " + str(soma) + "\n"
            print(str_soma, end='')

            str_soma = str(soma)
            first_n = False

def main():
    print("Input:")
    text = read_stdin()
    numbers = parse(text)
    if len(text) == 0 or text[-1].strip() == '':
        print("\nOutput:")
    else:
        print("\n\nOutput:")
    imprime_resultado(numbers)
    
main()
