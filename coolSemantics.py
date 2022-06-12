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


