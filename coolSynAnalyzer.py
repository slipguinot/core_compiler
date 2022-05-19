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

    def parseID(self, tokens):
        self.forward()
        if tokens[self.pos][1] == ' TYPE_IDENTIFIER':
            return {'type': 'TYPE', 'value': tokens[self.pos][0]}

        if tokens[self.pos][1] == ' OBJECT_IDENTIFIER':
            return {'type': 'ID', 'value': tokens[self.pos][0]}
        
        if tokens[self.pos][1] == ' SELF_TYPE':
            return {'type': 'SELF_TYPE', 'value': tokens[self.pos][0]}
        if tokens[self.pos][1] == ' SELF':
            return {'type': 'SELF', 'value': tokens[self.pos][0]}

    def parseBool(self, tokens):
        self.forward()
        if tokens[self.pos][1] == ' TRUE':
            return {'type': 'BOOL_TRUE', 'value': tokens[self.pos][0]}

        if tokens[self.pos][1] == ' FALSE':
            return {'type': 'BOOL_FALSE', 'value': tokens[self.pos][0]}

    def parseCompare(self, tokens, root):  
        self.forward()
        if tokens[self.pos][1] == ' IGUAL':
            n = AnyNode(id="COMPARACAO_IGUAL", parent = root, children = [
                    AnyNode(id=self.parseExpr(tokens, n), linha = tokens[self.pos][2], coluna = tokens[self.pos][3]),
                    AnyNode(id=self.parseExpr(tokens, n), linha = tokens[self.pos][2], coluna = tokens[self.pos][3])
                ])

        elif tokens[self.pos][1] == ' DIFERENTE':
            n = AnyNode(id="COMPARACAO_DIFERENTE", parent = root, children = [
                    AnyNode(id=self.parseExpr(tokens, n), linha = tokens[self.pos][2], coluna = tokens[self.pos][3]),
                    AnyNode(id=self.parseExpr(tokens, n), linha = tokens[self.pos][2], coluna = tokens[self.pos][3])
                ])

        elif tokens[self.pos][1] == ' MENOR_IGUAL':
            n = AnyNode(id="COMPARACAO_MENORIGUAL", parent = root, children = [
                    AnyNode(id=self.parseExpr(tokens, n), linha = tokens[self.pos][2], coluna = tokens[self.pos][3]),
                    AnyNode(id=self.parseExpr(tokens, n), linha = tokens[self.pos][2], coluna = tokens[self.pos][3])
                ])

        elif tokens[self.pos][1] == ' MENOR':
            n = AnyNode(id="COMPARACAO_MENOR", parent = root, children = [
                    AnyNode(id=self.parseExpr(tokens, n), linha = tokens[self.pos][2], coluna = tokens[self.pos][3]),
                    AnyNode(id=self.parseExpr(tokens, n), linha = tokens[self.pos][2], coluna = tokens[self.pos][3])
                ])

    def parseExpr(self, tokens, root):  
        self.forward()
        if tokens[self.pos][1] == ' IF':
            n = AnyNode(id="COND_IF", parent = root, children = [
                    AnyNode(id=self.parseExpr(tokens, n), linha = tokens[self.pos][2], coluna = tokens[self.pos][3])
                ])

        elif tokens[self.pos][1] == ' THEN':
            n = AnyNode(id="COND_THEN", parent = root, children = [
                    AnyNode(id=self.parseExpr(tokens, n), linha = tokens[self.pos][2], coluna = tokens[self.pos][3]),
                ])

        elif tokens[self.pos][1] == ' OBJECT_IDENTIFIER':
            self.backward()
            n = AnyNode(id="ID_OBJ", parent = root, children = [
                    AnyNode(id=self.parseID(tokens), linha = tokens[self.pos][2], coluna = tokens[self.pos][3]),
                ])

        elif tokens[self.pos][1] == ' TYPE_IDENTIFIER':
            self.backward()
            n = AnyNode(id="ID_TYPE", parent = root, children = [
                    AnyNode(id=self.parseID(tokens), linha = tokens[self.pos][2], coluna = tokens[self.pos][3]),
                ])

        elif tokens[self.pos][1] == ' TRUE':
            n = AnyNode(id="BOOL_TRUE", parent = root, children = [
                    AnyNode(id=self.parseBool(tokens), linha = tokens[self.pos][2], coluna = tokens[self.pos][3]),
                ])

        elif tokens[self.pos][1] == ' FALSE':
            n = AnyNode(id="BOOL_FALSE", parent = root, children = [
                    AnyNode(id=self.parseBool(tokens), linha = tokens[self.pos][2], coluna = tokens[self.pos][3]),
                ])
        elif tokens[self.pos][1] == ' NEW':
            n = AnyNode(id="DECL_new", parent = root, children = [
                    AnyNode(id=self.parseID(tokens), linha = tokens[self.pos][2], coluna = tokens[self.pos][3]),
                ])



    def parseFormal(self, tokens, root):
        if(tokens[self.pos][1] == ' OBJECT_IDENTIFIER'):
            self.backward()
            n = AnyNode(id=self.parseID(tokens), parent=root,
                        linha=tokens[self.pos][2], coluna=tokens[self.pos][3])
            self.forward()
        if(tokens[self.pos][1] == ' DOIS_PONTOS'):
            p = AnyNode(id={'type': ':', 'value': tokens[self.pos][0]}, parent=root)
            m = AnyNode(id=self.parseID(tokens), parent=root,
                        linha=tokens[self.pos][2], coluna=tokens[self.pos][3])
            self.forward()
        if(tokens[self.pos][1] == ' P_VIRGULA'):
            q = AnyNode(id={'type': ';', 'value': tokens[self.pos][0]}, parent=root)
        if(tokens[self.pos][1] == ' VIRGULA'):
            q = AnyNode(id={'type': ',', 'value': tokens[self.pos][0]}, parent=root)
        
    
    def parseMethod(self, tokens, root):
        if(tokens[self.pos][1] == ' OBJECT_IDENTIFIER'):
            self.backward()
            n = AnyNode(id=self.parseID(tokens), parent=root,linha=tokens[self.pos][2], coluna=tokens[self.pos][3])
            self.forward()
        if(tokens[self.pos][1] == ' PARENTESES_E'):
            p = AnyNode(id={'type': '(', 'value': tokens[self.pos][0]}, parent=root)
            self.parseFeature(tokens, root)
        return


    def parseFeature(self, tokens, root):
        while(tokens[self.pos + 1][1] == ' OBJECT_IDENTIFIER' and tokens[self.pos + 2][1] == ' DOIS_PONTOS'):
            self.forward()
            self.parseFormal(tokens, root)
            self.parseFeature(tokens, root)
        while(tokens[self.pos + 1][1] == ' OBJECT_IDENTIFIER' and tokens[self.pos + 2][1] == ' PARENTESES_E'):
            n = AnyNode(id="METHOD", parent = root)
            self.forward()
            self.parseMethod(tokens, n)
            self.parseFeature(tokens, root)
        if(tokens[self.pos][1] == ' PARENTESES_D'):
            p = AnyNode(id={'type': ')', 'value': tokens[self.pos][0]}, parent=root)
            self.forward()
            AnyNode(id = {'type': ':', 'value': tokens[self.pos][0]}, parent=root)
            AnyNode(id = self.parseID(tokens), parent=root, linha=tokens[self.pos][2], coluna=tokens[self.pos][3])
            if(tokens[self.pos][1] == ' SELF_TYPE'):
                self.forward()
                AnyNode(id = {'type': '{', 'value': tokens[self.pos][0]}, parent=root)
                self.forward()
                AnyNode(id = {'type': '{', 'value': tokens[self.pos][0]}, parent=root)
                self.parseExpr(tokens, root)
            else:
                self.parseExpr(tokens, root)
        
                

    def parseInherits(self, tokens, root):
        self.forward()
        if tokens[self.pos][1] != ' INHERITS':
            self.backward()
            pass

        else:
            AnyNode(id="INHERITS", parent=root, children=[
                AnyNode(id=self.parseID(tokens),
                        linha=tokens[self.pos][2], coluna=tokens[self.pos][3])
            ])

    def parseClass(self, tokens, root):
        n = AnyNode(id='CLASS', parent=root, children=[
            AnyNode(id=self.parseID(tokens), linha=tokens[self.pos][2], coluna=tokens[self.pos][3])])
        self.parseInherits(tokens, n)
        self.forward()
        if(tokens[self.pos][1] == ' CHAVES_E'):
            m = AnyNode(id="FEATURE", parent=n)
            self.parseFeature(tokens, m)
        if(tokens[self.pos][1] == ' CHAVES_D'):
            self.forward()
        if(tokens[self.pos][1] == ' P_VIRGULA'):  # acabou a feature
            return "ok"
        # return {'type': 'class', 'value': [self.parseIDa(tokens), self.parseInherits(tokens),  {'type': 'delimitador', 'value': ['{', self.parseFeature(tokens), '}']}]}

    def parseProgram(self, tokens, root):
        if tokens[self.pos][1] == ' CLASS':
            return self.parseClass(tokens, root)


# trecho de teste

hi = [('class ', ' CLASS', '1', '0'), ('CellularAutomaton', ' TYPE_IDENTIFIER', '1', '6'), ('inherits ', ' INHERITS', '1', '24'), ('IO', ' TYPE_IDENTIFIER', '1', '33'), ('{', ' CHAVES_E', '1', '36'), ('population_map', ' OBJECT_IDENTIFIER', '2', '1'), (':', ' DOIS_PONTOS', '2', '16'), ('String', ' TYPE_IDENTIFIER', '2', '18'), (';', ' P_VIRGULA', '2', '24'), ('init', ' OBJECT_IDENTIFIER', '4', '1'), ('(', ' PARENTESES_E', '4', '5'), ('map', ' OBJECT_IDENTIFIER', '4', '6'), (':', ' DOIS_PONTOS', '4', '10'), ('String', ' TYPE_IDENTIFIER', '4', '12'),  (',', ' VIRGULA', '4', '6') ,('map', ' OBJECT_IDENTIFIER', '4', '6'), (':', ' DOIS_PONTOS', '4', '10'), ('String', ' TYPE_IDENTIFIER', '4', '12'), (')', ' PARENTESES_D', '4', '18'), (':', ' DOIS_PONTOS', '4', '20'), ('SELF_TYPE', ' SELF_TYPE', '4', '22'), ('{', ' CHAVES_E', '4', '32'), ('{', ' CHAVES_E', '5', '2')
]

p = Parser()

root = AnyNode(id="PROGRAM")

teste = read_tokens("result.txt")
#print(teste)

result = p.parseProgram(teste, root)

for pre, _, node in RenderTree(root):
    print("%s%s" % (pre, node.id))

print(result)




"""if tokens[self.pos][1] == ' OBJECT_IDENTIFIER' and tokens[self.pos + 1][1] == ' PARENTESES_E':
# while tokens[self.pos + 1] != ' PARENTESES_D':
#     formal += self.parseFormal(tokens)
return {'type': 'feature', 'value': [ self.parseID(tokens), '(', self.parseFormal(tokens), self.forward(), ')', self.forward(), ':',
self.parseID(tokens), self.forward(), '{', self.parseExpr(), self.forward(), '}'] }

elif tokens[self.pos][1] == ' OBJECT_IDENTIFIER' and tokens[self.pos + 1][1] == ' DOIS_PONTOS':
pass"""

""" def parseInteger(tokens, pos):
    return {'type' : 'integer', 'value': tokens[pos][0]}

def parseString(tokens, pos):
    return {'type' : 'string', 'value': tokens[pos][0]}

def parseBoolean(token, pos):
    if token[1] == ' TRUE':
        return {'type' : 'true', 'value': token[0]}

    if token[1] == ' FALSE':
        return {'type' : 'false', 'value': token[0]}

def parsePONTOS(tokens, pos):
    return {'value': tokens[pos][0]}

def parseOps(tokens, pos):
    if tokens[pos][1] == ' MULTIPLICA':
        if tokens[pos-1][1] == ' OBJECT_IDENTIFIER' and tokens[pos+1][1] != ' OBJECT_IDENTIFIER':
            return {'type': 'multiplicacao', 'value': [parseID(tokens, pos-1), tokens[pos][0], parseInteger(tokens, pos+1)]}

        elif tokens[pos-1][1] != ' OBJECT_IDENTIFIER' and tokens[pos+1][1] == ' OBJECT_IDENTIFIER':
            return {'type': 'multiplicacao', 'value': [parseInteger(tokens, pos-1), tokens[pos][0], parseID(tokens, pos+1)]}

        elif tokens[pos-1][1] == ' OBJECT_IDENTIFIER' and tokens[pos+1][1] == ' OBJECT_IDENTIFIER':
            return {'type': 'multiplicacao', 'value': [parseID(tokens, pos-1), tokens[pos][0], parseID(tokens, pos+1)]}

        else:
            return {'type': 'multiplicacao', 'value': [parseInteger(tokens, pos-1), tokens[pos][0], parseInteger(tokens, pos+1)]}

    elif tokens[pos][1] == ' MENOS':
        if tokens[pos-1][1] == ' OBJECT_IDENTIFIER' and tokens[pos+1][1] != ' OBJECT_IDENTIFIER':
            return {'type': 'subtracao', 'value': [parseID(tokens, pos-1), tokens[pos][0], parseInteger(tokens, pos+1)]}

        elif tokens[pos-1][1] != ' OBJECT_IDENTIFIER' and tokens[pos+1][1] == ' OBJECT_IDENTIFIER':
            return {'type': 'subtracao', 'value': [parseInteger(tokens, pos-1), tokens[pos][0], parseID(tokens, pos+1)]}

        elif tokens[pos-1][1] == ' OBJECT_IDENTIFIER' and tokens[pos+1][1] == ' OBJECT_IDENTIFIER':
            return {'type': 'subtracao', 'value': [parseID(tokens, pos-1), tokens[pos][0], parseID(tokens, pos+1)]}

        else:
            return {'type': 'subtracao', 'value': [parseInteger(tokens, pos-1), tokens[pos][0], parseInteger(tokens, pos+1)]}


    elif tokens[pos][1] == ' MAIS':
        if tokens[pos-1][1] == ' OBJECT_IDENTIFIER' and tokens[pos+1][1] != ' OBJECT_IDENTIFIER':
            return {'type': 'adicao', 'value': [parseID(tokens, pos-1), tokens[pos][0], parseInteger(tokens, pos+1)]}

        elif tokens[pos-1][1] != ' OBJECT_IDENTIFIER' and tokens[pos+1][1] == ' OBJECT_IDENTIFIER':
            return {'type': 'adicao', 'value': [parseInteger(tokens, pos-1), tokens[pos][0], parseID(tokens, pos+1)]}

        elif tokens[pos-1][1] == ' OBJECT_IDENTIFIER' and tokens[pos+1][1] == ' OBJECT_IDENTIFIER':
            return {'type': 'adicao', 'value': [parseID(tokens, pos-1), tokens[pos][0], parseID(tokens, pos+1)]}

        else:
            return {'type': 'adicao', 'value': [parseInteger(tokens, pos-1), tokens[pos][0], parseInteger(tokens, pos+1)]}
    
    elif tokens[pos][1] == ' DIVIDE':
        if tokens[pos-1][1] == ' OBJECT_IDENTIFIER' and tokens[pos+1][1] != ' OBJECT_IDENTIFIER':
            return {'type': 'divisao', 'value': [parseID(tokens, pos-1), tokens[pos][0], parseInteger(tokens, pos+1)]}

        elif tokens[pos-1][1] != ' OBJECT_IDENTIFIER' and tokens[pos+1][1] == ' OBJECT_IDENTIFIER':
            return {'type': 'divisao', 'value': [parseInteger(tokens, pos-1), tokens[pos][0], parseID(tokens, pos+1)]}

        elif tokens[pos-1][1] == ' OBJECT_IDENTIFIER' and tokens[pos+1][1] == ' OBJECT_IDENTIFIER':
            return {'type': 'divisao', 'value': [parseID(tokens, pos-1), tokens[pos][0], parseID(tokens, pos+1)]}

        else:
            return {'type': 'divisao', 'value': [parseInteger(tokens, pos-1), tokens[pos][0], parseInteger(tokens, pos+1)]}
    
def parseFormal(tokens, pos):
    if tokens[pos][1] == ' DOIS_PONTOS':
        return {'type': 'formal', 'value': [parseID(tokens, pos-1), parsePONTOS(tokens, pos), parseID(tokens, pos+1)]  }"""
