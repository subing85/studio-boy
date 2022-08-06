import os
import json
import tempfile

from pipe import utils


from pipe import resources

from pipe.core import logger

LOGGER = logger.getLogger(__name__)
CURRENT_PATH = os.path.dirname(__file__)


def setPathResolver(path, folders=[]):
    return utils.setPathResolver(path, folders=folders)


def getIcon(name):
    iconpath = os.path.join(getIconPath(), name)
    if not os.path.isfile(iconpath):
        iconpath = os.path.join(getIconPath(), "unknown.png")
    iconpath = setPathResolver(iconpath)
    return iconpath


def getIconPath():
    return setPathResolver(os.path.join(CURRENT_PATH, "icons"))


def getImagePath():
    return setPathResolver(os.path.join(CURRENT_PATH, "images"))


def getBackgroundImage(step):
    path = setPathResolver(
        getImagePath(), folders=[step, "background.tif"]
    )
    return path


def getProjectImage(project, format="jpg"):
    image = getUrlImageToImage(
        project["thumbnail_url"]["url"], format=format
    )
    return image


def getStudioImage():
    image = getIcon("subins_toolkit_logo.png")
    return image


def getUrlImageToImage(url, format="jpg"):
    from pipe.utils import qwidgets

    qimage = qwidgets.encodeIcon(url)
    image = setPathResolver(
        tempfile.mktemp(".%s" % format, "JPEG", tempfile.gettempdir())
    )
    qimage.save(image)
    return image


def getInputPath():
    return os.path.join(CURRENT_PATH, "inputs")


def getConfigData(typed, name):
    data = getInputData(typed, enable=False)
    if not data:
        return
    bake_data = list(
        filter(lambda k: k["name"].lower() == name.lower(), data)
    )

    if not bake_data:
        LOGGER.warning(
            "could not found <%s> in the bake input resource" % name
        )
        return
    items = list(
        filter(lambda k: k["enable"] == True, bake_data[0]["items"])
    )
    items = sorted(items, key=lambda k: (k["order"]))
    bake_data[0]["items"] = items
    return bake_data[0]


def getInputData(name, enable=False):
    path = os.path.join(getInputPath(), "%s.json" % name)
    data = getData(path)
    if not data.get("enable"):
        return None
    if not enable:
        return data["data"]
    enabled_data = list(
        filter(lambda k: k["enable"] == True, data["data"])
    )
    return enabled_data


def getData(path):
    if not os.path.isfile(path):
        raise IOError("not found path <%s>" % path)
    with open(path, "r") as file:
        data = json.load(file)
        return data


def getDateTime(context=None):
    return resources.getDateTime(context=context)


def searchContext(input, key, value=None):
    if value:
        contexts = list(
            filter(
                lambda k: k.get(key) == value and k.get("enable"),
                input,
            )
        )
    else:
        contexts = list(
            filter(
                lambda k: k.get(key) and k.get("enable"),
                input,
            )
        )
    return contexts
