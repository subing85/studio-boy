import importlib

from common.scripts import scene
importlib.reload(scene)

from common.scripts.scene import LoadScene
from common.scripts.scene import BuildScene


class BuildScene(BuildScene):
    eventEnable = True
    eventName = "layoutBuildScene"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()
    
    
class LoadScene(LoadScene):
    eventEnable = True
    eventName = "layoutLoadScene"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()
