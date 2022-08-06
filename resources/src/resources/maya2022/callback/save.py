class Common(object):
    @classmethod
    def doIt(cls):
        from maya import cmds
        from pipe.nodes import PipeNode
        nodetypes = [each["typeName"] for each in PipeNode.nodeTypes()]
        for each in cmds.ls(type=nodetypes):
            PipeNode.refresh(node=each)    


class After(object):
    @classmethod
    def doIt(cls):
        Common.doIt()


class Before(object):
    @classmethod
    def doIt(cls):
        Common.doIt()