class SearchDefultTransforms(object):
    @classmethod
    def doIt(cls):
        from maya import mel
        from maya import cmds

        geometry = mel.eval('listTransforms "-type mesh"')
        nurbscurve = mel.eval('listTransforms "-type nurbsCurve"')
        nodes = set(geometry + nurbscurve)
        invalidAttributes = []
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
                invalidAttributes.append(
                    [attribute, float(value), default[0]]
                )
        return invalidAttributes


class SearchUnLockedTransformAttributes(object):
    @classmethod
    def doIt(cls):
        from maya import mel
        from maya import cmds

        nodes = set(mel.eval('listTransforms "-type mesh"'))
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
        invalidAttributes = []
        for node in nodes:
            for each in attributes:
                attribute = "%s.%s" % (node, each)
                lock = cmds.getAttr(attribute, lock=True)
                if lock:
                    continue
                invalidAttributes.append([node, each])
        return invalidAttributes
