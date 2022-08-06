from maya import mel
from maya import cmds


def execute():
    geometry = mel.eval('listTransforms "-type mesh"')
    nurbscurve = mel.eval('listTransforms "-type nurbsCurve"')
    nodes = set(geometry + nurbscurve)
    invalid_nodes = []
    for node in nodes:
        histories = cmds.listHistory(node, pdo=True, gl=True)
        if not histories:
            continue
        histories = [each.encode() for each in histories]
        invalid_nodes.append([node.encode(), histories])
    if invalid_nodes:
        return False, "found history", invalid_nodes
    return True, "not found any history ", invalid_nodes
