from lookdev.scripts.scene import LookdevScene
from lookdev.scripts.scene import LookdevShader


class GroomScene(LookdevScene):

    eventEnable = True
    eventName = "groomShaderScene"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()


class GroomShader(LookdevShader):

    eventEnable = True
    eventName = "groomShaderScene"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()
    
    
