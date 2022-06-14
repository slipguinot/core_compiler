#salve bora sofrer

##Regras de tipo do cool:
#As another example, if En has type
#X, then the expression { E1; . . . ; En; } has type X.

from anytree import AnyNode, RenderTree, findall, find

class registro:
    def __init__(self, name, methods, inheritance, attr):
        self.name = name
        self.methods = methods
        self.inheritance = inheritance
        self.attr = attr

    def print(self):
        print(f"Classe: {self.name}")
        for metodo in self.methods:
            metodo.print()

class method:
    def __init__(self, name, parametros, retorno):
        self.name = name
        self.parametros = parametros
        self.retorno = retorno

    def print(self):
        print(f"Metodo: {self.name}\nParametros:")
        for parametro in self.parametros:
            print(f"{parametro}, ")
        print(f"Retorno: {self.retorno}")

class Attr:
    def __init__(self, name, type):
        self.name = name
        self.type = type
    def print(self):
        print(f"{self.name}:{self.type}")

outString = method("out_string", [{'value' : "String", 'name' : 'algo'}], "SELF_TYPE")
outInt = method("out_int", [{'value' : "Int", 'name' : 'algo'}], "SELF_TYPE")
inString = method("in_string", [""], "String")
inInt = method("in_int", ["", {'value' : "Int", 'name' : 'algo'}], "Int")


regIO = registro("IO", [outString, outInt, inString, inInt], "", [])


abort = method("abort", [""], "Object")
typeName = method("type_name", [""], "String")
copyMethod = method("copy", [""], "SELF_TYPE")

ObjectClass = registro("Object", [abort, typeName, copyMethod], "", [])

length = method("length", [""], "Int")
concats = method("concat", ["String"], "String")
substr = method("substr", ["Int", "Int"], "String")

StringClass = registro("String", [length, concats, substr], "", [])

intClass = registro("Int", [], "", [])

boolClass = registro("Bool", [], "", [])

symbolTable = [regIO, ObjectClass, StringClass, intClass, boolClass]

def lookForClass(searchingFor):
    for ref in symbolTable:
        if(ref.name == searchingFor):
            return True
    return False

def getInheritance(nomeClasse):
    for classe in symbolTable:
        if(classe.name == nomeClasse):
            return classe.inheritance

def addNewClass(newClass):
    newEntry = registro(newClass, [], "", [])
    symbolTable.append(newEntry)

def addInheritance(classe, heranca):
    for reg in symbolTable:
        if(reg.name == classe):
            reg.inheritance = heranca

def addNewMethodToClass(classe, methodName, tipoRetorno):
    newEntry = method(methodName, [], tipoRetorno)
    for ref in symbolTable:
        if(ref.name == classe):
            ref.methods.append(newEntry)
            return True
    return False

def checkIfArgExists(nomeClasse, methodName, argument):
    ascendente = getInheritance(nomeClasse)
    for classe in symbolTable:
        if(classe.name == nomeClasse or classe.name == ascendente):
            for atributo in classe.attr:
                if(atributo['name'] == argument['name']):
                    raise Exception(f"O nome {atributo['name']} já está sendo utilizado.")
            for metodo in classe.methods:
                if(metodo.name == methodName):
                    for parametro in metodo.parametros:
                        if(parametro['name'] == argument['name']):
                            raise Exception(f"O nome {argument['name']} já está sendo utilizado.")
    return False

def addArgToMethod(classe, methodName, argument):
    if(checkIfArgExists(classe, methodName, argument) == False):
        for ref in symbolTable:
            if(ref.name == classe):
                for metodo in ref.methods:
                    if(metodo.name == methodName):
                        metodo.parametros.append(argument)

def addAttrToClass(classe, attr):
    if(checkIfAttrExists(classe, attr) == False):
        for ref in symbolTable:
            if(ref.name == classe):
                ref.attr.append(attr)

def checkIfAttrExists(nomeClasse, attr):
    for ref in symbolTable:
        if(ref.name == nomeClasse):
            for atributo in ref.attr:
                if(atributo == attr):
                    raise Exception(f"Existe um atributo {attr} com o mesmo nome, favor verificar.")
    return False


def addRetornoToMethod(classe, methodName, retorno):
        for ref in symbolTable:
            if(ref.name == classe):
                for metodo in ref.methods:
                    if(metodo.name == methodName):
                        metodo.retorno = retorno


def checkIfMethodExists(nomeClasse, method):
    for classe in symbolTable:
        if(classe.name == nomeClasse):
            for metodo in classe.methods:
                if(metodo.name == method):
                    return True
    return False

def checkIfMethodExistsEverywhere(nomeClasse, method):
    ascendentes = []
    ascendente = getInheritance(nomeClasse)
    while(True):
        if(ascendente == ''):
            break
        else:
            ascendentes.append(ascendente)
            ascendente = getInheritance(ascendente)

    for classe in symbolTable:
        if(classe.name == nomeClasse or classe.name in ascendentes):
            for metodo in classe.methods:
                if(metodo.name == method):
                    return True
    return False

def getReturnType(method):
    for classe in symbolTable:
        for metodo in classe.methods:
            if(metodo.name == method):
                return metodo.retorno

def lookForInherit(searchingFor):
    if(searchingFor != "String" and searchingFor != "Bool" and searchingFor != "String"):
        for ref in symbolTable:
            if(ref.name == searchingFor):
                return True
    return False


def getClassName(ancestors):
    for ancestrais in ancestors:
        if(ancestrais.id == "CLASS"):
            for filho in ancestrais.children:
                if(filho.id == "TYPE_IDENTIFIER"):
                    return filho.children[0].id['value']



def addMethod(classe, method):
    nomeMetodo = find(method, lambda node: node.id == "METHOD_NAME").children[0].id['value']
    tipoRetorno = find(method, lambda node: node.id == "TIPO_RETORNO").children[0].id['value']
    if(checkIfMethodExists(classe, nomeMetodo) == True):
        raise Exception(f"Metodo {nomeMetodo} já existe e não pode ser redeclarado.")
    addNewMethodToClass(classe, nomeMetodo, tipoRetorno)
    parametros = findall(method, lambda node: node.id == "PARAMETRO")
    if(len(parametros) > 0):
        for parametro in parametros:
            addArgToMethod(classe, nomeMetodo, {'name' : parametro.children[0].children[0].id['value'], 'value' : parametro.children[2].children[0].id['value']})
    
    return "ok"

def addAtrToClass(classRoot, nomeClasse):
    atributos = findall(classRoot, lambda node: node.id == "NOME_ATRIBUTO")
    if(len(atributos) > 0):
        for atributo in atributos:
            attrType = find(atributo.ancestors[2], lambda node: node.id == "TIPO_ATRIBUTO").children[0].id['value']
            addAttrToClass(nomeClasse, { 'name' : atributo.children[0].id['value'], 'tipo' : attrType })



def getReturnTypeFromMethod(nomeClasse, methodName):
    for ref in symbolTable:
        if(ref.name == nomeClasse):
            for metodo in ref.methods:
                if(metodo.name == methodName):
                    return metodo.retorno

    return ""


def checkExpressionType(nomeClasse, expressao):
    nodes = findall(expressao, lambda node: node.id != 'COMPARACAO' and node.id != 'IF' and node.id != 'WHILE')
    tipoAtual = ""
    if(len(nodes) > 0):
        for node in nodes:
            if(tipoAtual == ""):
                tipoAtual = node.id
            else:
                if(tipoAtual != node.id):
                    raise Exception(f"Tipos diferentes")
    return True

def getArgType(nomeClasse, nomeMetodo, nome):

    for ref in symbolTable:
        if(ref.name == nomeClasse):
            if(nomeMetodo != ""):
                for metodo in ref.methods:
                    if(metodo.name == nomeMetodo):
                        for atr in metodo.parametros:
                            if(atr['name'] == nome):
                                return atr['value']
            for atb in ref.attr:
                if(atb['name'] == nome):
                    return atb['tipo']

    return ""

def checkNodeType(nomeClasse, nomeMetodo, node, tipoAtual):
    if(node.id == "OBJECT_IDENTIFIER"):
        varName = node.children[0].id['value']
        tipo = getArgType(nomeClasse, nomeMetodo, varName)
        return tipo
    elif(node.id == "INTEGER"):
        return "Int"
    elif(node.id == "STRING"):
        return "String"
    elif(node.id == "CHAMADA_METODO"):
        return getReturnTypeFromMethod(nomeClasse, node.children[0].children[0].id['value'])
    return tipoAtual

def checkExpression(nomeClasse, nomeMetodo, expressao):   

    ifsWhiles = findall(expressao, lambda node: node.id == "IF" or node.id == "WHILE")
    if(len(ifsWhiles) > 0):
        for interesse in ifsWhiles:
            retorno = ""
            methodCalls = findall(interesse, lambda node: node.id == "CHAMADA_METODO")
            if(len(methodCalls) > 0):            
                for chamada in methodCalls:
                    retorno = getReturnTypeFromMethod(nomeClasse, chamada.children[0].children[0].id['value'])
            comparacoes = findall(interesse, lambda node: node.id == "COMPARACAO")
            if(len(comparacoes) > 0):
                if(checkExpressionType(nomeClasse, comparacoes[0].ancestors[len(comparacoes[0].ancestors) - 1]) == True):
                    retorno = 'Bool'
            if(retorno != 'Bool'):
                raise Exception(f"Erro no tipo de expressão no IF/While")
    atrb = findall(expressao, lambda node: node.id == "ATRIBUICAO")
    if(len(atrb) > 0):
        tipo = ""
        tipoDesejado = ""
        for atribuicao in atrb:
            tipoChamador = atribuicao.ancestors[len(atribuicao.ancestors) - 1]
            if(tipoChamador.id == "OBJECT_IDENTIFIER"):
                tipoDesejado = getArgType(nomeClasse, nomeMetodo, tipoChamador.children[0].id['value'])
            for node in atribuicao.children:
                if(tipoDesejado == ""):
                    tipoDesejado = checkNodeType(nomeClasse, nomeMetodo, node, tipoDesejado)
                else:
                    tipo = checkNodeType(nomeClasse, nomeMetodo, node, tipoDesejado)
                    if(tipo != tipoDesejado):
                        raise Exception(f"Expressao invalida")
            print("ok")



    # methodCall = find(expressao, lambda node: node.id == "CHAMADA_METODO")
    # if(methodCall != None):
    #    retorno = getReturnTypeFromMethod(nomeClasse, methodCall.children[0].children[0].id['value'])
    # node = find(expressao, lambda node: node.id == "IF")
    # if(node != None):
    #     comparacao = find(node, lambda node: node.id == "COMPARACAO") 
    #     methodCall = find(node, lambda node: node.id == "CHAMADA_METODO")
    #     if(comparacao == None and retorno != "Bool"):
    #         raise Exception(f"A expressão do IF não é booleana.")     
    #     return "Ok"

    return "ok"


def semanticAnalyzer(root):
    classes = findall(root, lambda node: node.id == "CLASS")
    if(len(classes) > 0):
        for classe in classes:
            nomeClasse = find(classe, lambda node: node.id == "CLASS_NAME").children[0].id['value']
            addAtrToClass(classe, nomeClasse)
            metodos = findall(classe, lambda node: node.id == "METHOD")
            for metodo in metodos:
                addMethod(nomeClasse, metodo)
            chamadasMetodo =  findall(classe, lambda node: node.id == "CHAMADA_METODO")
            for metodo in chamadasMetodo:
                if(checkIfMethodExistsEverywhere(nomeClasse, metodo.children[0].children[0].id['value']) == False):
                    raise Exception(f"Metodo {metodo.children[0].children[0].id['value']} não existe.")
            for metodo in metodos:
                expressoes = findall(metodo, lambda node: node.id == "EXPRESSION")
                for expressao in expressoes:
                    checkExpression(nomeClasse, metodo.children[0].children[0].id['value'], expressao)
    return "e lá vamos nós"