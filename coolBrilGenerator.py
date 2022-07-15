from anytree import AnyNode, RenderTree, findall, find

def expressionCodeGenerator(expression):
    resultado = ""
    if(len(expression.children) == 1):
        resultado = "\t" + resultado + expression.children[0].value
    qtdExpressoes = len(expression.children)
    for expressao in expression.children:
        if(expressao.id == "OBJECT_IDENTIFIER"):
            resultado = resultado + "\t"
            varName = expressao.children[0].id['value']
            temAtribuicao = findall(expressao, lambda node: node.id == "ATRIBUICAO")
            if(len(temAtribuicao) > 0):
                for atribuicao in temAtribuicao:
                    objetos = findall(atribuicao, lambda node: node.id == "OBJECT_IDENTIFIER")
                    if(len(objetos) > 0):
                        for objeto in objetos:
                            var2Name = objeto.children[0].id['value']
                            resultado = resultado + "store " + varName + " " + var2Name + ";\n"
        elif(expressao.id == "CHAMADA_METODO"):
            resultado = resultado + "\t"            
            qtdFilhos = len(expressao.children) - 1
            for membro in expressao.children:
                if(membro.id != {'type': 'PARENTESES_E', 'value': '('} and membro.id != {'type': 'VIRGULA', 'value': ','} and membro.id != {'type': 'PARENTESES_D', 'value': ')'}):
                    if(qtdFilhos == len(expressao.children) - 1):
                        nomeMetodo = expressao.children[0].children[0].id['value']
                        resultado = resultado + "call " + f"@{nomeMetodo}"
                        qtdFilhos -= 1
                    else:
                        resultado = resultado + f" {membro.children[0].id['value']}"
            resultado = resultado + ";\n"
        elif(expressao.id == "IF"):
            comparacao = find(expressao, lambda node: node.id == "COMPARACAO")
            if(comparacao.value == "="):
                resultado = resultado + f"\t aux: eq {expressao.children[0].value} {expressao.children[2].value};\n"
            elif(comparacao.value == "<="):
                resultado = resultado + f"\t aux: le {expressao.children[0].value} {expressao.children[2].value};\n"
            elif(comparacao.value == "<"):
                resultado = resultado + f"\t aux: lt {expressao.children[0].value} {expressao.children[2].value};\n"          
            resultado = resultado + "\t br aux THEN ELSE;\n"

        elif(expressao.id == "THEN"):
            resultado = resultado + "\t THEN: " + expressao.children[0].value + ";\n"
            resultado = resultado + "\t jmp NEXT;\n"

        elif(expressao.id == "ELSE"):
            resultado = resultado + "\t ELSE: " + expressao.children[0].value + ";\n"
            resultado = resultado + "\t NEXT: "

    resultado = resultado + "\n"
    return resultado

def BrilCodeGenerator(root):
    saida = open("saida.bril", "a")
    classes = findall(root, lambda node: node.id == "CLASS")
    if(len(classes) > 0):
        for classe in classes:
            nomeClasse = find(classe, lambda node: node.id == "CLASS_NAME").children[0].id['value']
            metodos = findall(root, lambda node: node.id == "METHOD")
            for metodo in metodos:
                nomeMetodo = find(metodo, lambda node: node.id == "METHOD_NAME").children[0].id['value']
                saida.write(f"@{nomeMetodo}_{nomeClasse}(")
                tipoRetorno = find(metodo, lambda node: node.id == "TIPO_RETORNO").children[0].id['value']
               
                parametros = findall(metodo, lambda node: node.id == "PARAMETRO")
                if(tipoRetorno != "Int" and tipoRetorno != "Bool"):
                    saida.write("this: ptr<int>")
                    tipoRetorno = "ptr<int>"
                    if(len(parametros) > 0):
                        saida.write(", ")
                if(len(parametros) > 0):
                    virgulas = len(parametros) - 1
                    for parametro in parametros:
                        parametroNome = find(parametro, lambda node: node.id == "NOME_PARAMETRO").children[0].id['value']
                        parametroTipo = find(parametro, lambda node: node.id == "TIPO_PARAMETRO").children[0].id['value']
                        saida.write(f"{parametroNome}: {parametroTipo}")
                        if(virgulas > 0):
                            saida.write(", ")                        
                            virgulas -= 1
                saida.write(f") : {tipoRetorno}\n")
                expressoes = findall(metodo, lambda node: node.id == "EXPRESSION")                
                saida.write("{\n")
                qtdExpressoes = len(expressoes)
                
                if(qtdExpressoes > 0):
                    for expressao in expressoes:
                        saida.write(expressionCodeGenerator(expressao))
                saida.write("}\n\n")
    
    saida.close()
    return "transpilado"