from anytree import AnyNode, RenderTree



def teste(root):
    oi = AnyNode(id="FilhoNaFunc", parent = root)
    teste1(oi)

def teste1(root):
    AnyNode(id="FilhoDois", parent = root)

root = AnyNode(id="root")
teste(root)
kk = AnyNode(id="oi", parent=root)
teste1(kk)
"""for pre, _, node in RenderTree(root):
    print("%s%s" % (pre, node.id))


print("oi")"""