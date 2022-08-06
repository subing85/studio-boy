from maya import cmds


def execute():
    valid_anims = ["animCurveTL", "animCurveTA", "animCurveTU"]
    anim_curves = cmds.ls(type="animCurve")
    invalid_nodes = []
    for anim_curve in anim_curves:
        node_type = cmds.nodeType(anim_curve)
        if node_type not in valid_anims:
            continue
        nodes = cmds.listConnections(anim_curve, s=False, d=True)
        nodes = nodes or [None]
        invalid_nodes.append([nodes[0].encode(), anim_curve.encode()])
    if invalid_nodes:
        return (
            False,
            "found animtion curves in your scene",
            invalid_nodes,
        )
    return (
        True,
        "not found animtion curves in your scene",
        invalid_nodes,
    )
