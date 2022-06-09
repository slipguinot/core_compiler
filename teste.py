from anytree import AnyNode, RenderTree



n = AnyNode(id = "filho")
m = AnyNode(id = "irmao")
root = AnyNode(id = "Pai", children = [n, m])
for pre, _, node in RenderTree(root):
    print("%s%s" % (pre, node.id))
