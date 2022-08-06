from maya import mel
from maya import cmds


def execute():
    geometry = mel.eval('listTransforms "-type mesh"')
    nodes = set(geometry)
    invalid_nodes = []
    attributes = [
        "tx",
        "ty",
        "tz",
        "rx",
        "ry",
        "rz",
        "sx",
        "sy",
        "sz",
    ]
    for node in nodes:
        for each in attributes:
            attribute = "%s.%s" % (node, each)
            lock = cmds.getAttr(attribute, lock=True)
            if lock:
                continue
            invalid_nodes.append([node.encode(), attribute.encode()])
    if invalid_nodes:
        return (
            False,
            "geometry transformation attributes are not locked",
            invalid_nodes,
        )
    return (
        True,
        "all geometry transformation attributes are locked",
        invalid_nodes,
    )
