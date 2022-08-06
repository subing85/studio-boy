from maya import cmds


def execute():
    dag_nodes = cmds.ls(dag=True, l=True)
    invalid_nodes = []
    for dag_node in dag_nodes:
        name = dag_node.split("|")[-1]
        nodes = cmds.ls(name)
        if len(nodes) == 1:
            continue
        if nodes in invalid_nodes:
            continue
        nodes = [each.encode() for each in nodes]
        invalid_nodes.append(nodes)
    if invalid_nodes:
        return False, "found name-clash", invalid_nodes
    return True, "not found name-clash", invalid_nodes
