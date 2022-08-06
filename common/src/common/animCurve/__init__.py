class SearchAnimCurve(object):
    @classmethod
    def doIt(cls):
        from maya import cmds

        valid_anims = ["animCurveTL", "animCurveTA", "animCurveTU"]
        anim_curves = cmds.ls(type="animCurve")
        animation = []
        for anim_curve in anim_curves:
            node_type = cmds.nodeType(anim_curve)
            if node_type not in valid_anims:
                continue
            nodes = cmds.listConnections(anim_curve, s=False, d=True)
            nodes = nodes or [None]
            animation.append([nodes[0], anim_curve])
        return animation
