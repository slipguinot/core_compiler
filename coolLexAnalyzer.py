#leitura do arquivo com o codigo
import re
file = open('reference.txt', 'r')
linha = file.readline()
leitor = []

while linha != "":
    leitor.append(linha)
    linha = file.readline()
    if linha == "":
        leitor.append(' ')
        fullCode = ''.join(leitor)
        leitor = []
file.close()
#print(fullCode)

tokens = [
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
    'MAIOR_IGUAL',
    'FIMLINHA',
    'ASPAS_DUPLAS',
    'WHITESPACE',
    'QUEISSO?' #algo inesperado
]

lexemes = [
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
    r'==',
    r'!=',
    r'\+',
    r'/',
    r'<',
    r'<=',
    r'>',
    r'>=',
    r'\n',
    r'"',
    r'[ \t\f\r\v]+', #WHITESPACE
    r'.', #algo que não foi esperado
]


tokenLexema = []

for i in range(0, len(lexemes) - 1):
    tokenLexema.append((tokens[i], lexemes[i]))

tokenPattern = '|'.join('(?P<%s>%s)' % x for x in tokenLexema)

comecoLinha = 0

token = []
lexeme = []
row = []
column = []
numeroLinha = 1
for m in re.finditer(tokenPattern, fullCode):
    token_type = m.lastgroup
    token_lexeme = m.group(token_type)
    if token_type == 'IDENTIFICADOR':
        if token_lexeme[0].isupper():
            token_type = 'TYPE_IDENTIFIER'
        else:
            token_type = 'OBJECT_IDENTIFIER'
    elif token_type == 'FIMLINHA':
        comecoLinha = m.end()
        numeroLinha += 1
    elif token_type == 'WHITESPACE':
        continue
    elif token_type == 'QUEISSO':
        raise RuntimeError('%r erro desconhecido em %d' % (token_lexeme, numeroLinha))
    else:
            col = m.start() - comecoLinha
            column.append(col)
            token.append(token_type)
            lexeme.append(token_lexeme)
            row.append(numeroLinha)
            print('Token = {0}, Lexema = \'{1}\', Linha = {2}, Coluna = {3}'.format(token_type, token_lexeme, numeroLinha, col))
           