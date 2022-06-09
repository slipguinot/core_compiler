from asyncio.windows_events import NULL
import coolLexAnalyzer as lex
from anytree import AnyNode, RenderTree

def read_tokens(path: str):
    f = open(path)
    tokens = f.readlines()

    lista = []
    list_tokens = []

    for token in tokens:
        lista = token.replace('\n', '').split(',')
        list_tokens.append((lista[0], lista[1], lista[2], lista[3]))

    return list_tokens


class Parser:
    def __init__(self):
        self.pos = 0

    def forward(self, steps=1):
        self.pos += steps

    def backward(self, steps=1):
        self.pos -= steps

    def lookAheadUntilClosing(self, tokens, lookingFor):
        rollback = self.pos
        while(self.pos < len(tokens)):
            if(tokens[self.pos][1] == lookingFor or (tokens[self.pos][1] == ' CHAVES_D' and tokens[self.pos + 1][1] == ' P_VIRGULA')):
                self.pos = rollback
                return True
            else:
                self.forward()

        self.pos = rollback
        return False

    def parseID(self, tokens):
        if tokens[self.pos][1] == ' TYPE_IDENTIFIER':
            return AnyNode(id={'type': 'TYPE', 'value': tokens[self.pos][0]})

        if tokens[self.pos][1] == ' OBJECT_IDENTIFIER':
            return AnyNode(id={'type': 'ID', 'value': tokens[self.pos][0]})
        
        if tokens[self.pos][1] == ' SELF_TYPE':
            return AnyNode(id={'type': 'SELF_TYPE', 'value': tokens[self.pos][0]})
        if tokens[self.pos][1] == ' SELF':
            return AnyNode(id={'type': 'SELF', 'value': tokens[self.pos][0]})
       
    def parseInherits(self, tokens):
        self.forward()
        inherits = AnyNode(id="INHERITS", linha=tokens[self.pos][2], coluna=tokens[self.pos][3], children=[
                self.parseID(tokens)
            ])
        return inherits

    def lookAheadUntilPosition(self, tokens, lookingFor):
        rollback = self.pos
        limite = -1
        while(self.pos < len(tokens)):
            if(tokens[self.pos][1] == lookingFor or tokens[self.pos + 1][1] == ' P_VIRGULA'):
                limite = self.pos
                self.pos = rollback
                return limite
            else:
                self.forward()

        self.pos = rollback
        return limite

    def parseFormals(self, tokens, root):
        if(tokens[self.pos][1] != ' OBJECT_IDENTIFIER' or tokens[self.pos + 1][1] != ' DOIS_PONTOS' or tokens[self.pos + 2][1] != ' TYPE_IDENTIFIER'):
            node = AnyNode(id = "Feature mal formada, o padrão é: ID : Tipo;", linha = tokens[self.pos][2], coluna = tokens[self.pos][3], parent = root)
            return f"Erro, Feature mal formada, o padrão é: [ID : Tipo;] Rever linha {node.linha} e coluna {node.coluna}."
        objectIdentifier = AnyNode(id= 'OBJECT_IDENTIFIER', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], children = [self.parseID(tokens)], parent = root)
        self.forward()
        doisPontos = AnyNode(id={'type': 'DOIS_PONTOS', 'value': tokens[self.pos][0]}, parent = root)
        self.forward()
        typeIdentifier = AnyNode(id= 'TYPE_IDENTIFIER', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], children = [self.parseID(tokens)], parent = root)
        self.forward()
        if(tokens[self.pos][1] == ' VIRGULA'):
            virg = AnyNode(id={'type': 'VIRGULA', 'value': tokens[self.pos][0]}, parent = root)
            self.forward()
        elif(tokens[self.pos][1] == ' PARENTESES_D'):
            par = AnyNode(id={'type': 'PARENTESES_D', 'value': tokens[self.pos][0]}, parent = root)            
        return "ok"

    def parseExpr(self, tokens, root):
        if(tokens[self.pos][1] == ' OBJECT_IDENTIFIER'):
            #chamada de metodo
            if(tokens[self.pos + 1][1] == ' OBJECT_IDENTIFIER'):
                objectIdentifier = AnyNode(id= 'OBJECT_IDENTIFIER', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], children = [self.parseID(tokens)], parent = root)
                self.forward()
                objectIdentifier2 = AnyNode(id= 'OBJECT_IDENTIFIER', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], children = [self.parseID(tokens)], parent = root)
                self.forward()
                parentesesE = AnyNode(id={'type': 'PARENTESES_E', 'value': tokens[self.pos][0]}, parent = root)
                self.forward()            
                self.parseExpr(tokens,root)
                self.forward()
                parentesesD = AnyNode(id={'type': 'PARENTESES_D', 'value': tokens[self.pos][0]}, parent = root)
                self.forward()
                return "ok"
            #ID(algo)
            elif(tokens[self.pos + 1][1] == ' PARENTESES_E'):
                objectIdentifier = AnyNode(id= 'OBJECT_IDENTIFIER', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], children = [self.parseID(tokens)], parent = root)
                self.forward()
                parentesesE = AnyNode(id={'type': 'PARENTESES_E', 'value': tokens[self.pos][0]}, parent = root)
                self.forward()
                self.parseExpr(tokens, root)
                self.forward()
                parentesesD = AnyNode(id={'type': 'PARENTESES_D', 'value': tokens[self.pos][0]}, parent = root)
                self.forward()
                return "ok"
            #atribuicao normal
            elif(tokens[self.pos + 1][1] == ' ATRIBUICAO'):
                objectIdentifier = AnyNode(id= 'OBJECT_IDENTIFIER', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], children = [self.parseID(tokens)], parent = root)
                self.forward()
                atribuicao = AnyNode(id={'type': 'ATRIBUICAO', 'value': tokens[self.pos][0]}, parent = root)
                self.forward()
                self.parseExpr(tokens, root)
                self.forward()
                pontoVirg = AnyNode(id={'type': 'P_VIRGULA', 'value': tokens[self.pos][0]}, parent = root)
                self.forward()
                return "ok"
            #só ID mesmo
            elif(tokens[self.pos + 1][1] == ' P_VIRGULA'): 
                objectIdentifier = AnyNode(id= 'OBJECT_IDENTIFIER', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], children = [self.parseID(tokens)], parent = root)
                self.forward()
                pontoVirg = AnyNode(id={'type': 'P_VIRGULA', 'value': tokens[self.pos][0]}, parent = root)
                self.forward()
                return "ok"
            else:
                objectIdentifier = AnyNode(id= 'OBJECT_IDENTIFIER', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], children = [self.parseID(tokens)], parent = root)
                self.forward()
                self.parseExpr(tokens, root)
                self.forward()
            return "ok"
        elif(tokens[self.pos][1] == ' IF'):
            ifstart = AnyNode(id= 'IF', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], parent = root)
            self.forward()
            self.parseExpr(tokens, root)
            thenStart = AnyNode(id= 'THEN', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], parent = root)
            self.parseExpr(tokens, root)
            self.forward()
            elseStart = AnyNode(id= 'ELSE', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], parent = root)
            self.parseExpr(tokens, root)
            self.forward()
            fiStart = AnyNode(id= 'FI', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], parent = root)
            self.forward()
            return "ok"
        elif(tokens[self.pos][1] == ' WHILE'):
            whileStart = AnyNode(id= 'WHILE', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], parent = root)
            self.forward()
            self.parseExpr(tokens, root)
            loopStart = AnyNode(id= 'LOOP', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], parent = root)
            self.parseExpr(tokens, root)
            self.forward()
            pool = AnyNode(id= 'POOL', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], parent = root)
            self.forward()
            return "ok"
            
        elif(tokens[self.pos][1] == ' CHAVES_E'):
            chavesE = AnyNode(id={'type': 'CHAVES_E', 'value': tokens[self.pos][0]}, parent = root)
            self.forward()
            self.parseExpr(tokens, root)
            self.forward()
            chavesD = AnyNode(id={'type': 'CHAVES_D', 'value': tokens[self.pos][0]}, parent = root)
            self.forward()
            return "ok"
        elif(tokens[self.pos][1] == ' PARENTESES_E'):
            parentesesE = AnyNode(id={'type': 'PARENTESES_E', 'value': tokens[self.pos][0]}, parent = root)
            self.forward()
            self.parseExpr(tokens, root)
            self.forward()
            parentesesD = AnyNode(id={'type': 'PARENTESES_D', 'value': tokens[self.pos][0]}, parent = root)
            self.forward()
            return "ok"
        elif(tokens[self.pos][1] == ' LET'):
            return "expr começa com LET"
        elif(tokens[self.pos][1] == ' CASE'):
            return "expr começa com CASE"
        elif(tokens[self.pos][1] == ' NEW'):
            parentesesE = AnyNode(id={'type': 'NEW', 'value': tokens[self.pos][0]}, parent = root)
            self.forward()
            typeIdentifier = AnyNode(id= 'TYPE_IDENTIFIER', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], children = [self.parseID(tokens)], parent = root)
            self.forward()
        elif(tokens[self.pos][1] == ' ISVOID'):
            isvoid = AnyNode(id={'type': 'ISVOID', 'value': tokens[self.pos][0]}, parent = root)
            self.forward()
            self.parseExpr(tokens, root)
            self.forward()
        elif(tokens[self.pos][1] == ' NOT'):
            isnot = AnyNode(id={'type': 'NOT', 'value': tokens[self.pos][0]}, parent = root)
            self.forward()
            self.parseExpr(tokens, root)
            self.forward()
        elif(tokens[self.pos][1] == ' INTEIRO'):
            string = AnyNode(id={'type': 'INTEGER', 'value': tokens[self.pos][0]}, parent = root)
            self.forward()
            if(tokens[self.pos][1] != ' P_VIRGULA'):
                self.parseExpr(tokens, root)
            return "ok"
        elif(tokens[self.pos][1] == ' STRING'):
            string = AnyNode(id={'type': 'STRING', 'value': tokens[self.pos][0]}, parent = root)
            return "ok"
        elif(tokens[self.pos][1] == ' TRUE'):
            string = AnyNode(id={'type': 'TRUE', 'value': tokens[self.pos][0]}, parent = root)
            return "ok"
        elif(tokens[self.pos][1] == ' FALSE'):
            string = AnyNode(id={'type': 'FALSE', 'value': tokens[self.pos][0]}, parent = root)
            return "ok"
        #tirando isso sobra as operações binárias, são os casos de recursão a esquerda
        elif(tokens[self.pos][1] == ' MAIS'):
            string = AnyNode(id={'type': 'SOMA', 'value': tokens[self.pos][0]}, parent = root)
            self.forward()
            self.parseExpr(tokens, root)
            return "ok"
        elif(tokens[self.pos][1] == ' HIFEN'):
            string = AnyNode(id={'type': 'SUBTRACAO', 'value': tokens[self.pos][0]}, parent = root)
            self.forward()
            self.parseExpr(tokens, root)
            return "ok"
        elif(tokens[self.pos][1] == ' BARRA'):
            string = AnyNode(id={'type': 'DIVISAO', 'value': tokens[self.pos][0]}, parent = root)
            self.forward()
            self.parseExpr(tokens, root)
            return "ok"
        elif(tokens[self.pos][1] == ' ASTERISCO'):
            string = AnyNode(id={'type': 'MULTIPLICACAO', 'value': tokens[self.pos][0]}, parent = root)
            self.forward()
            self.parseExpr(tokens, root)
            return "ok"
        elif(tokens[self.pos][1] == ' IGUAL'):
            string = AnyNode(id={'type': 'IGUALDADE', 'value': tokens[self.pos][0]}, parent = root)
            self.forward()
            self.parseExpr(tokens, root)
            return "ok"
        return "ok"

    def parseFeatureMethod(self, tokens, methodParent):        
        methodName = AnyNode(id= 'OBJECT_IDENTIFIER', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], children = [self.parseID(tokens)], parent = methodParent)
        self.forward()
        parentesesE = AnyNode(id={'type': 'PARENTESES_E', 'value': tokens[self.pos][0]}, parent = methodParent)
        self.forward()
        if(tokens[self.pos][1] == ' PARENTESES_D'):
            par = AnyNode(id={'type': 'PARENTESES_D', 'value': tokens[self.pos][0]}, parent = methodParent)
        else:
            while(tokens[self.pos][1] != ' PARENTESES_D'):
                retorno = self.parseFormals(tokens, methodParent)
                if(retorno != "ok"):
                    break
        self.forward()
        if(tokens[self.pos][1] != ' DOIS_PONTOS'):
            node = AnyNode(id = "Faltando dois pontos(:).", linha = tokens[self.pos][2], coluna = tokens[self.pos][3], parent = root)
            return f"Erro, faltando dois pontos(:) linha {node.linha} e coluna {node.coluna}."
        doisPontos = AnyNode(id={'type': 'DOIS_PONTOS', 'value': tokens[self.pos][0]}, parent = methodParent)
        self.forward()
        if(tokens[self.pos][1] != ' TYPE_IDENTIFIER'):
            node = AnyNode(id = "Faltando TYPE_IDENTIFIER.", linha = tokens[self.pos][2], coluna = tokens[self.pos][3], parent = root)
            return f"Erro, faltando TYPE_IDENTIFIER na linha {node.linha} e coluna {node.coluna}."
        typeIdentifier = AnyNode(id= 'TYPE_IDENTIFIER', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], children = [self.parseID(tokens)], parent = methodParent)
        self.forward()
        if(tokens[self.pos][1] != ' CHAVES_E'):
            node = AnyNode(id = "Faltando CHAVES_E.", linha = tokens[self.pos][2], coluna = tokens[self.pos][3], parent = root)
            return f"Erro, faltando CHAVES_E na linha {node.linha} e coluna {node.coluna}."
        chaves = AnyNode(id={'type': 'CHAVES_E', 'value': tokens[self.pos][0]}, parent = methodParent)
        self.forward()
        while(self.lookAheadUntilClosing(tokens, " CHAVES_D") != False):
            expressionParent = AnyNode(id = 'EXPRESSION', parent = methodParent)
            self.parseExpr(tokens, expressionParent)
            if(tokens[self.pos][1] == ' CHAVES_D' and tokens[self.pos+1][1] == ' P_VIRGULA'):
                chaves = AnyNode(id={'type': 'CHAVES_D', 'value': tokens[self.pos][0]}, parent = methodParent)
                self.forward()
                pVirg = AnyNode(id={'type': 'P_VIRGULA', 'value': tokens[self.pos][0]}, parent = methodParent)
                self.forward()
                break

        return methodParent

    def parseFeature(self, tokens, root):
        self.forward()
        if(tokens[self.pos][1] != ' OBJECT_IDENTIFIER'):
            node = AnyNode(id = "Erro, não foi encontrado tipo identificador da feature.", linha = tokens[self.pos][2], coluna = tokens[self.pos][3], parent = root)
            return f"Erro, não foi encontrado tipo identificador da feature na linha {node.linha} e coluna {node.coluna}."
        elif(tokens[self.pos + 1][1] != ' PARENTESES_E' and tokens[self.pos + 1][1] != ' DOIS_PONTOS'):
            node = AnyNode(id = "Erro, não foi encontrado parenteses ou dois pontos.", linha = tokens[self.pos][2], coluna = tokens[self.pos][3], parent = root)
            return f"Erro, não foi encontrado parenteses ou dois pontos na linha {node.linha} e coluna {node.coluna}."
        
        if(tokens[self.pos + 1][1] != ' DOIS_PONTOS'):
            methodParent = AnyNode(id = 'METHOD')
            retorno = self.parseFeatureMethod(tokens, methodParent)
            featureParent = AnyNode(id = 'FEATURE', children = [methodParent], parent = root)
            if(retorno != "ok"):
                return "erro"
            chaves = AnyNode(id={'type': 'CHAVES_D', 'value': tokens[self.pos][0]}, parent = methodParent)
            self.forward()
            pVirg = AnyNode(id={'type': 'P_VIRGULA', 'value': tokens[self.pos][0]}, parent = methodParent)
            self.forward()
        else:
            objectIdentifier = AnyNode(id= 'OBJECT_IDENTIFIER', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], children = [self.parseID(tokens)])
            self.forward()
            doisPontos = AnyNode(id={'type': 'DOIS_PONTOS', 'value': tokens[self.pos][0]})
            self.forward()
            if(tokens[self.pos][1] != ' TYPE_IDENTIFIER' and tokens[self.pos + 1][1] != ' P_VIRGULA'):
                node = AnyNode(id = "Erro, não foi encontrado tipo identificador da feature e/ou ponto virgula.", linha = tokens[self.pos][2], coluna = tokens[self.pos][3], parent = root)
                return f"Erro, não foi encontrado tipo identificador da feature e/ou ponto virgula na linha {node.linha} e coluna {node.coluna}."

            typeIdentifier = AnyNode(id= 'TYPE_IDENTIFIER', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], children = [self.parseID(tokens)])
            self.forward()
            if(tokens[self.pos][1] != ' P_VIRGULA'):
                node = AnyNode(id = "Erro, faltou ;.", linha = tokens[self.pos][2], coluna = tokens[self.pos][3], parent = root)
                return f"Erro, faltou ; na linha {node.linha} e coluna {node.coluna}."
            pontoVirg = AnyNode(id={'type': 'PONTO_VIRGULA', 'value': tokens[self.pos][0]})
            featureParent = AnyNode(id = 'FEATURE', children = [objectIdentifier, doisPontos, typeIdentifier, pontoVirg], parent = root)
        return "ok"

    def parseClass(self, tokens, root):
        self.forward()
        if(tokens[self.pos][1] != ' TYPE_IDENTIFIER'):
            node = AnyNode(id = "Erro, não foi encontrado tipo identificador de classe.", linha = tokens[self.pos][2], coluna = tokens[self.pos][3], parent = root)
            return f"Erro, não foi encontrado tipo identificador de classe na linha {node.linha} e coluna {node.coluna}."
        elif(tokens[self.pos + 1][1] != ' INHERITS' and tokens[self.pos + 1][1] != ' CHAVES_E'):
            node = AnyNode(id = "Erro, não foi encontrado INHERITS ou abertura de bloco de código.", linha = tokens[self.pos][2], coluna = tokens[self.pos][3], parent = root)
            return f"Erro, não foi encontrado INHERITS ou abertura de bloco de código na linha {node.linha} e coluna {node.coluna}."
       
        typeIdentifier = AnyNode(id= 'TYPE_IDENTIFIER', linha=tokens[self.pos][2], coluna=tokens[self.pos][3], children = [self.parseID(tokens)])
        self.forward()
        if(tokens[self.pos][1] == ' INHERITS'):
            if(tokens[self.pos + 1][1] != ' TYPE_IDENTIFIER' and tokens[self.pos + 2][1] != ' CHAVES_E'):           
                node = AnyNode(id = "Erro, não foi encontrado tipo de herança ou abertura de bloco de código.", linha = tokens[self.pos][2], coluna = tokens[self.pos][3], parent = root)
                return f"Erro, não foi encontrado tipo de herança ou abertura de bloco de código na linha {node.linha} e {node.coluna}."
            inherits = self.parseInherits(tokens)
            self.forward()
            chavesE = AnyNode(id={'type': 'CHAVES_ESQUERDA', 'value': tokens[self.pos][0]})
            classParent = AnyNode(id = 'CLASS', children = [typeIdentifier, inherits, chavesE], parent = root)
        else:
            if(tokens[self.pos + 1][1] != ' CHAVES_E'):
                node = AnyNode(id = "Erro, não foi encontrado INHERITS ou abertura de bloco de código.", linha = tokens[self.pos][2], coluna = tokens[self.pos][3], parent = root)
                return f"Erro, não foi encontrado INHERITS ou abertura de bloco de código na linha {node.linha} e coluna {node.coluna}."
            chavesE = AnyNode(id={'type': 'CHAVES_ESQUERDA', 'value': tokens[self.pos][0]})
            classParent = AnyNode(id = 'CLASS', children = [typeIdentifier, chavesE], parent = root)
        
        while(self.lookAheadUntilClosing(tokens, " DOIS_PONTOS") != False):
            retorno = self.parseFeature(tokens, classParent)
            if(retorno != "ok"):
                break
        return("ok")

    def parseProgram(self, tokens, root):
       if tokens[self.pos][1] == ' CLASS':
            return self.parseClass(tokens, root)



hi = [('class ', ' CLASS', '1', '0'), ('CellularAutomaton', ' TYPE_IDENTIFIER', '1', '6'), ('inherits ', ' INHERITS', '1', '24'), ('IO', ' TYPE_IDENTIFIER', '1', '33'), ('{', ' CHAVES_E', '1', '36'), ('population_map', ' OBJECT_IDENTIFIER', '2', '1'), (':', ' DOIS_PONTOS', '2', '16'), ('String', ' TYPE_IDENTIFIER', '2', '18'), (';', ' P_VIRGULA', '2', '24'), ('init', ' OBJECT_IDENTIFIER', '4', '1'), ('(', ' PARENTESES_E', '4', '5'), ('map', ' OBJECT_IDENTIFIER', '4', '6'), (':', ' DOIS_PONTOS', '4', '10'), ('String', ' TYPE_IDENTIFIER', '4', '12'),  (',', ' VIRGULA', '4', '6') ,('map', ' OBJECT_IDENTIFIER', '4', '6'), (':', ' DOIS_PONTOS', '4', '10'), ('String', ' TYPE_IDENTIFIER', '4', '12'), (')', ' PARENTESES_D', '4', '18'), (':', ' DOIS_PONTOS', '4', '20'), ('SELF_TYPE', ' SELF_TYPE', '4', '22'), ('{', ' CHAVES_E', '4', '32'), ('{', ' CHAVES_E', '5', '2')]

p = Parser()

root = AnyNode(id="PROGRAM")
teste = read_tokens("result.txt")
print(teste)

result = p.parseProgram(teste, root)


for pre, _, node in RenderTree(root):
    print("%s%s" % (pre, node.id))

print(result)