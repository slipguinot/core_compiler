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
        self.pos +=steps

    def backward(self, steps=1):
        self.pos -= steps


    def parseID(self, tokens):
        self.forward()
        if tokens[self.pos][1] == ' TYPE_IDENTIFIER':
            return {'type': 'TYPE', 'value': tokens[self.pos][0]}

        if tokens[self.pos][1] == ' OBJECT_IDENTIFIER':
            return {'type': 'ID', 'value': tokens[self.pos][0]}

#funcao ainda nao desenvolvida
    def parseExpr(self, tokens):
        self.forward()


#funcao nao testada dentro da classe, fora ok
    def parseFormal(self, tokens):
        self.forward()
        return {'type': 'formal', 'value': [self.parseID(tokens), self.forward(), ':', self.parseID(tokens)] }

    def parseMethod(self, tokens, root):
        return
#funcao nao testada
    def parseFeature(self,tokens, root):
        self.forward()
        if(tokens[self.pos][1] == ' CHAVES_E'):
            print(tokens[self.pos][1])
        """if tokens[self.pos][1] == ' OBJECT_IDENTIFIER' and tokens[self.pos + 1][1] == ' PARENTESES_E':
            # while tokens[self.pos + 1] != ' PARENTESES_D':
            #     formal += self.parseFormal(tokens)
            return {'type': 'feature', 'value': [ self.parseID(tokens), '(', self.parseFormal(tokens), self.forward(), ')', self.forward(), ':',
            self.parseID(tokens), self.forward(), '{', self.parseExpr(), self.forward(), '}'] }

        elif tokens[self.pos][1] == ' OBJECT_IDENTIFIER' and tokens[self.pos + 1][1] == ' DOIS_PONTOS':
            pass"""

    def parseInherits(self,tokens, root):  
        self.forward()
        if tokens[self.pos][1] != ' INHERITS':
            self.backward()
            pass

        else:
            AnyNode(id="INHERITS", parent = root, children = [
                AnyNode(id=self.parseID(tokens), linha = tokens[self.pos][2], coluna = tokens[self.pos][3])
            ])

    def parseClass(self,tokens, root):
        n = AnyNode(id = 'CLASS', parent=root, children = [
                AnyNode(id = self.parseID(tokens), linha = tokens[self.pos][2], coluna = tokens[self.pos][3])])
        self.parseInherits(tokens, n)
        self.parseFeature(tokens, n)
        #return {'type': 'class', 'value': [self.parseID(tokens), self.parseInherits(tokens),  {'type': 'delimitador', 'value': ['{', self.parseFeature(tokens), '}']}]}

    def parseProgram(self,tokens, root):
        if tokens[self.pos][1] == ' CLASS':            
            return self.parseClass(tokens, root)



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


#trecho de teste

hi = [('class ', ' CLASS', '1', '0'), ('CellularAutomaton', ' TYPE_IDENTIFIER', '1', '6'), 
('inherits ', ' INHERITS', '1', '24'), ('IO', ' TYPE_IDENTIFIER', '1', '33'), 
('{', ' CHAVES_E', '1', '36'), ('population_map', ' OBJECT_IDENTIFIER', '2', '1'), 
(':', ' CHAVES_D', '2', '16')]

p = Parser()

root = AnyNode(id="PROGRAM")

result = p.parseProgram(hi, root)

for pre, _, node in RenderTree(root):
    print("%s%s" % (pre, node.id))

print(result)

