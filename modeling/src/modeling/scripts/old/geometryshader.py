from maya import cmds


def execute():
    default_shaders = cmds.ls(defaultNodes=True, materials=True)
    geometries = cmds.ls(type="mesh")
    invalid_nodes = []
    for geometry in geometries:
        shding_engines = cmds.listConnections(
            geometry, type="shadingEngine"
        )
        if not shding_engines:
            invalid_nodes.append(
                [geometry.encode(), "not assign any shaders"]
            )
            continue
        dependency_nodes = cmds.listConnections(shding_engines)
        shaders = list(set(cmds.ls(dependency_nodes, materials=True)))
        for shader in shaders:
            if shader in default_shaders:
                continue
            invalid_nodes.append([geometry.encode(), shader.encode()])
    if invalid_nodes:
        return (
            False,
            "geometries are not assign to default lambert1 shader",
            invalid_nodes,
        )
    return (
        True,
        "all geometries are assign to default lambert1 shader",
        invalid_nodes,
    )
