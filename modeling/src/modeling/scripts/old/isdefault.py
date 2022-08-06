from maya import mel
from maya import cmds


def execute():
    geometry = mel.eval('listTransforms "-type mesh"')
    nurbscurve = mel.eval('listTransforms "-type nurbsCurve"')
    nodes = set(geometry + nurbscurve)
    invalid_nodes = []
    for node in nodes:
        attributes = cmds.listAttr(node, k=True, u=True, sn=True)
        for att in attributes:
            default = cmds.attributeQuery(
                att, node=node, listDefault=True
            )
            attribute = "%s.%s" % (node, att)
            value = cmds.getAttr("%s.%s" % (node, att))
            if isinstance(value, int) or isinstance(value, float):
                value = round(value, 5)
            if default[0] == value:
                continue
            invalid_nodes.append([attribute.encode(), float(value)])
    if invalid_nodes:
        return False, "not default values ", invalid_nodes
    return (
        True,
        "all transform object attributes are default values",
        invalid_nodes,
    )
