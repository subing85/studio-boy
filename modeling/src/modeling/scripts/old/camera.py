from maya import cmds


def create(start, end):
    current_camera = cmds.lookThru(q=True)
    mov_camera = cmds.camera()
    constraint = cmds.parentConstraint(
        current_camera, mov_camera[0], mo=False, w=True
    )
    cmds.delete(constraint)
    cmds.lookThru(mov_camera[1])
    camera_group = cmds.group(em=True)
    cmds.parent(mov_camera[0], camera_group)
    cmds.setAttr("%s.overscan" % mov_camera[1], 1)
    anim_curve = cmds.createNode("animCurveTA")
    cmds.connectAttr(
        "%s.output" % anim_curve, "%s.rotateY" % camera_group
    )
    cmds.keyTangent(anim_curve, e=True, wt=False)
    cmds.setAttr("%s.preInfinity" % anim_curve, 0)
    cmds.setAttr("%s.postInfinity" % anim_curve, 0)
    cmds.setKeyframe(anim_curve, time=start, value=0)
    cmds.setKeyframe(anim_curve, time=end, value=-360)
    cmds.keyTangent(
        anim_curve,
        e=1,
        t=(start, end),
        itt=("linear"),
        ott=("linear"),
    )
    return current_camera, [camera_group, mov_camera[0], anim_curve]


def delete_camera(current_camera, nodes):
    cmds.lookThru(current_camera)
    for node in nodes:
        if not cmds.objExists(node):
            continue
        cmds.delete(node)
