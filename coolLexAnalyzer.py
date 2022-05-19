import re

#função de leitura de arquivo
def read_file(filename: str):
    
    with open(filename, 'r') as f:
        prog = f.read()
        prog = prog.replace('\t', '').replace('    ', ' ')
        return prog


#função para salvar o arquivo resultante
def save_file(path: str, content):
    
    text_file = open(path, "w")
    
    for tupla in content:
        #print('(' + tupla + ')')
        text_file.write(tupla + '\n')
        text_file.flush()
    
    text_file.close()
    print('O arquivo foi salvo.')


code = read_file('program.txt')

#função para deletar comentários do código na linguagem COOL
def delete_comments(code: str):
    i=0
    size = len(code) - 1
    new_code = []

    while (i+1)<size:
        string = ''
        if (code[i] + code[i+1]) == "(*":
            string = code[i] + code[i+1]
            i+=2

                
            while (code[i] + code[i+1]) != "*)":
                string += code[i]

                i+=1
        
            i+=2

            string += "*)"            
            new_code.append(string)

        else:
            i+=1

    for i in new_code:
        code=code.replace(i, '')

    return code


fullCode = delete_comments(code)


tokens = [
    'STRING',
    'SELF',
    'SELF_TYPE',
    'TRUE',
    'FALSE',
    'CLASS',
    'ELSE',
    'FI',
    'IF',
    'IN',
    'INHERITS',
    'ISVOID',
    'LET',
    'LOOP',
    'POOL',
    'THEN',
    'WHILE',
    'CASE',
    'ESAC',
    'NEW',
    'OF',
    'INTEIRO',
    'IDENTIFICADOR',
    'NOT',
    'CHAVES_E',
    'CHAVES_D',
    'PARENTESES_E',
    'PARENTESES_D',
    'ASTERISCO',
    'HIFEN',
    'VIRGULA',
    'P_VIRGULA',
    'ATRIBUICAO',
    'IGUAL',
    'DIFERENTE',
    'MAIS',
    'BARRA',
    'MENOR',
    'MENOR_IGUAL',
    'MAIOR',
    'ATRIBUICAO_CASE',
    'WHITESPACE',
    'NOVALINHA',
    'ASPAS',
    'DOIS_PONTOS',
    'QUEISSO?' #algo inesperado
]

lexemes = [
    r'\"(.*?)\"',
    r'self', #self
    r'SELF_TYPE', #selftype
    r't(?i)rue(\s)', #TRUE
    r'f(?i)alse(\s)', #FALSE
    r'(?i)class(\s)', #BREAK
    r'(?i)else(\s)', #CASE
    r'(?i)fi(\s)', #CLASS
    r'(?i)if(\s)', #CATCH
    r'(?i)in(\s)', #CONST
    r'(?i)inherits(\s)',#continue
    r'(?i)isvoid(\s)',
    r'(?i)let(\s)',
    r'(?i)loop(\s)',
    r'(?i)pool(\s)',
    r'(?i)then(\s)',
    r'(?i)while(\s)',
    r'(?i)case(\s)',
    r'(?i)esac(\s)',
    r'(?i)new(\s)',
    r'(?i)of(\s)',
    r'\d(\d)*', #INTEIRO
    r'[a-zA-Z]\w*', #IDENTIFICADOR
    r'(?i)not(\s)',    
    r'\{',
    r'\}',
    r'\(',
    r'\)',
    r'\*',
    r'\-',
    r',',
    r';',
    r'<-',
    r'=',
    r'!=',
    r'\+',
    r'/',
    r'<',
    r'<=',
    r'>',
    r'=>',
    r'[ \t\f\r\v]+', #WHITESPACE
    r'\n',
    r'"',
    r':',
    r'.', #algo que não foi esperado
]


tokenLexema = []


for i in range(0, len(lexemes)-1):
    tokenLexema.append((tokens[i], lexemes[i]))

tokenPattern = '|'.join('(?P<%s>%s)' % x for x in tokenLexema)

lin_start = 0

token = []
lexeme = []
row = []
column = []
lin_num = 1

list_tok = []
for m in re.finditer(tokenPattern, fullCode):
    token_type = m.lastgroup
    token_lexeme = m.group(token_type)
    if token_type == 'IDENTIFICADOR':
        if token_lexeme[0].isupper():
            token_type = 'TYPE_IDENTIFIER'
        else:
            token_type = 'OBJECT_IDENTIFIER'
    if token_type == 'WHITESPACE':
        continue
    elif token_type == 'NOVALINHA':
        lin_start = m.end()
        lin_num += 1

    elif token_type == 'QUEISSO':
        raise RuntimeError('%r unexpected on line %d' % (token_lexeme, lin_num))
    
    else:
        col = m.start() - lin_start
        column.append(col)
        token.append(token_type)
        lexeme.append(token_lexeme)
        row.append(lin_num)
        #print('({0}, {1})'.format(token_type, token_lexeme))
        list_tok.append(token_lexeme.replace('\n', '') + ', ' + token_type + ',' + str(lin_num) + ',' + str(col))
           
save_file('result.txt', list_tok)