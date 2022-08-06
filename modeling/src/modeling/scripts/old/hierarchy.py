from maya import mel
from maya import cmds


def execute():
    hierarchy = [
        "|world",
        "|world|control",
        "|world|control|transform",
        "|world|control|controls",
        "|world|geometry",
        "|world|geometry|hires",
        "|world|geometry|lores",
    ]
    invalid_nodes = []
    lost_nodes = []
    for each in hierarchy:
        if cmds.objExists(each):
            continue
        lost_nodes.append(each)
    if lost_nodes:
        invalid_nodes = [["missing", lost_nodes]]
    default = ["persp", "top", "front", "side", hierarchy[0]]
    top_level_nodes = cmds.ls(assemblies=True)
    unwant_nodes = []
    for node in top_level_nodes:
        if node in default:
            continue
        unwant_nodes.append(node.encode())
    if unwant_nodes:
        invalid_nodes.append(["unwanted", unwant_nodes])
    if invalid_nodes:
        return False, "found wrong hierarchy", invalid_nodes
    return True, "hierarchy is prefect", invalid_nodes


def create():
    pass
