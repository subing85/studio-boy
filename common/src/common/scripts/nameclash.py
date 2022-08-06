class Validate(object):

    eventEnable = True
    eventName = "sceneNameclash"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        valid, message, nodes = cls.travelScene()
        cls.output["valid"] = valid
        cls.output["message"] = message
        cls.output["nodes"] = nodes

    @classmethod
    def travelScene(cls):
        from maya import cmds

        dag_nodes = cmds.ls(dag=True, l=True)
        invalid_nodes = []
        for dag_node in dag_nodes:
            name = dag_node.split("|")[-1]
            nodes = cmds.ls(name)
            if len(nodes) == 1:
                continue
            if nodes in invalid_nodes:
                continue
            nodes = [each for each in nodes]
            invalid_nodes.append(nodes)
        if invalid_nodes:
            return False, "find name-clash", invalid_nodes
        return True, "could not find name-clash", invalid_nodes
