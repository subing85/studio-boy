from maya import cmds


def execute():
    default_shaders = cmds.ls(defaultNodes=True, materials=True)
    shaders = cmds.ls(materials=True)
    invalid_nodes = []
    for shader in shaders:
        if shader in default_shaders:
            continue
        invalid_nodes.append(["invalid shader", shader.encode()])
    if invalid_nodes:
        return False, "found invalid shader", invalid_nodes
    return True, "not found invalid shader", invalid_nodes
