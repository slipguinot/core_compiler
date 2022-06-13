#salve bora sofrer

##Regras de tipo do cool:
#As another example, if En has type
#X, then the expression { E1; . . . ; En; } has type X.
class registro:
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

class method:
    def __init__(self, name, parametros, retorno):
        self.name = name
        self.parametros = parametros
        self.retorno = retorno

class Attr:
    def __init__(self, name, type):
        self.name = name
        self.type = type

outString = method("out_string", ["String"], "SELF_TYPE")
outInt = method("out_int", ["Int"], "SELF_TYPE")
inString = method("in_string", [""], "String")
inInt = method("in_int", ["", "Int"], "Int")


regIO = registro("IO", [outString, outInt, inString, inInt])


abort = method("abort", [""], "Object")
typeName = method("type_name", [""], "String")
copyMethod = method("copy", [""], "SELF_TYPE")

ObjectClass = registro("Object", [abort, typeName, copyMethod])

length = method("length", [""], "Int")
concats = method("concat", ["String"], "String")
substr = method("substr", ["Int", "Int"], "String")

StringClass = registro("String", [length, concats, substr])

intClass = registro("Int", [])

boolClass = registro("Bool", [])

symbolTable = [regIO, ObjectClass, StringClass, intClass, boolClass]

def lookForClass(searchingFor):
    for ref in symbolTable:
        if(ref.name == searchingFor):
            return True
    return False


def addNewClass(newClass):
    newEntry = registro(newClass, [])
    symbolTable.append(newEntry)

def addNewMethodToClass(classe, methodName):
    newEntry = method(methodName, [], "")
    for ref in symbolTable:
        if(ref.name == classe):
            ref.methods.append(newEntry)
            return True
    return False

def addArgToMethod(classe, methodName, argument):
    for ref in symbolTable:
        if(ref.name == classe):
            for metodo in ref.methods:
                if(metodo.name == methodName):
                    metodo.parametros.append(argument)

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