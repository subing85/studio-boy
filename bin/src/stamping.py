import os
import logging
import optparse
import tempfile

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

LOGGER = logging.getLogger("__main__")

from pprint import pprint


def execute():
    """
    :description
        studio-pipe event commands.
        to query and execute the studio-pipe events

    :examples
        \u2022 pipe event setWorkspace
            to execute the event based on the event name.
                :param <str>

        \u2022 pipe event-all
            get all available stuido-pipe events.
                :param None

        \u2022 pipe event-name
            get all specific event based on name.
                :param <str>
    """

    parser = optparse.OptionParser(
        usage="usage: %prog [options] studio-pipe image stamping commands.",
        version="0.0.1",
    )

    option_list = [
        optparse.make_option(
            "-W",
            "--width",
            dest="width",
            default=1024,
            type="int",
            help="width of the final image",
        ),
        optparse.make_option(
            "-H",
            "--height",
            dest="height",
            default=1024,
            type="int",
            help="height of the final image",
        ),
        optparse.make_option(
            "-D",
            "--directory",
            dest="source",
            action="store",
            type="string",
            help="file path of the foreground image",
        ),
        optparse.make_option(
            "-O",
            "--output",
            dest="output",
            action="store",
            type="string",
            default=tempfile.mktemp(
                ".jpg", "Studio-Pipe_", tempfile.gettempdir()
            ),
            help="file path of the output image",
        ),
        optparse.make_option(
            "-F",
            "--foreground",
            dest="foreground",
            action="store",
            type="string",
            help="file path of the foreground image",
        ),
        optparse.make_option(
            "-B",
            "--background",
            dest="background",
            action="store",
            type="string",
            help="file path of the background image",
        ),
        optparse.make_option(
            "-P",
            "--project",
            dest="project",
            action="store",
            type="string",
            help="file path of the project logo image",
        ),
        optparse.make_option(
            "-L",
            "--logo",
            dest="logo",
            action="store",
            type="string",
            help="file path of the studio logo image",
        ),
        optparse.make_option(
            "--projectSize",
            dest="projectSize",
            action="store",
            type="string",
            default="medium",
            help="project logo image size (small, medium, large)",
        ),
        optparse.make_option(
            "--logoSize",
            dest="logoSize",
            action="store",
            type="string",
            default="medium",
            help="project logo image size (small, medium, large)",
        ),
        optparse.make_option(
            "--projectPositions",
            dest="projectPositions",
            action="store",
            type="string",
            default="['right', 'bottom']",
            help="""
                project logo image position 
                    (
                        'left, top', 'left, center''left, bottom',
                        'right, top', 'right, center''right, bottom',
                        'middle, top', 'middle, center''middle, bottom'
                    )
                """,
        ),
        optparse.make_option(
            "--logoPositions",
            dest="logoPositions",
            action="store",
            type="string",
            default="['left', 'bottom']",
            help="""
                studio logo image position 
                    (
                        'left, top', 'left, center''left, bottom',
                        'right, top', 'right, center''right, bottom',
                        'middle, top', 'middle, center''middle, bottom'
                    )
                """,
        ),
        optparse.make_option(
            "-M",
            "--watermark",
            dest="watermark",
            action="store",
            type="string",
            help="""
                list dictionary watermark context
                    [
                        {
                            "font": "arialbd.ttf",
                            "encoding": "unic",
                            "size": "medium",
                            "positions": ["left", "top"],
                            "spacing": 8,
                            "align": "left",
                            "color": "black",
                            "stroke_width": 0,
                            "marks": [
                                {"Email": "subing85@gmail.com111111111111111"},
                                {"Username": "subingopi"},
                                {"User Role": "Administrator"}
                            ],
                        }
                    ]
                """,
        ),
    ]

    parser.add_options(option_list)
    (options, args) = parser.parse_args()

    print(options)

    """ 
    E:\venture\source_code\studio-pipe\devkit\pipeline\bin\src\stamping.py -W 1024 -H 1024 -F "C:/Users/sid/Desktop/icons/playblast_0000001001.tif" -B "C:/Users/sid/Desktop/icons/background.tiff" -P "C:/Users/sid/Desktop/icons/show.png" -L "C:/Users/sid/Desktop/icons/subins_toolkit_logo.png" --projectSize "medium" --logoSize "medium" --projectPositions "['left', 'bottom']" --logoPositions "['right', 'bottom']" -M "ssssssss"

    E:\venture\source_code\studio-pipe\devkit\pipeline\bin\src\stamping.py
        -W 1024 
        -H 1024 
        -F "C:/Users/sid/Desktop/icons/playblast_0000001001.tif" 
        -B "C:/Users/sid/Desktop/icons/background.tiff" 
        -P "C:/Users/sid/Desktop/icons/show.png" 
        -L "C:/Users/sid/Desktop/icons/subins_toolkit_logo.png" 
        --projectSize "medium" 
        --logoSize "medium" 
        --projectPositions "['left', 'bottom']" 
        --logoPositions "['right', 'bottom']" 
        -M "ssssssss"
    """

    if not options.foreground:
        logging.warning(
            "TypeError: stamping missing 1 required positional argument: '-F or --foreground'"
        )
        return

    if not options.background:
        logging.warning(
            "TypeError: stamping missing 1 required positional argument: '-B or --background'"
        )
        return

    if not options.project:
        logging.warning(
            "TypeError: stamping missing 1 required positional argument: '-P or --project'"
        )
        return

    if not options.logo:
        logging.warning(
            "TypeError: stamping missing 1 required positional argument: '-L or --logo'"
        )
        return

    if not options.output:
        logging.warning(
            "TypeError: stamping missing 1 required positional argument: '-O or --output'"
        )
        return

    options.foreground = pathResolver(options.foreground)
    if not options.foreground:
        return

    options.background = pathResolver(options.background)
    if not options.background:
        return

    options.project = pathResolver(options.project)
    if not options.project:
        return

    options.logo = pathResolver(options.logo)
    if not options.logo:
        return

    options.output = pathResolver(options.output, exists=False)
    if not options.output:
        return

    composite(**options.__dict__)

    """
    
    {'width': 1024, 
     'height': 1024, 
     'source': None, 
     'foreground': None, 
     'background': None, 
     'project': None, 
     'logo': None, 
     'projectSize': None, 
     'logoSize': None, 
     'projectPositions': None, 
     'logoPositions': None, 
     'watermark': None
     }
    """


def pathResolver(path, exists=True):
    expand_path = os.path.expandvars(path)
    if not os.path.isabs(expand_path):
        logging.warning("invalid path %s" % path)
        return None
    resolved_path = os.path.abspath(expand_path).replace("\\", "/")
    if not exists:
        return resolved_path
    if not os.path.exists(resolved_path):
        logging.warning("could not find the path %s" % resolved_path)
        return None
    return resolved_path


def composite(**kwargs):

    pprint(kwargs)
    width, height = kwargs.get("resolution", [1024, 1024])

    foreground = kwargs.get("foreground")
    background = kwargs.get("background")
    project = kwargs.get("project")
    logo = kwargs.get("logo")

    output = kwargs.get("output")

    project_size = kwargs.get("project_size", "medium")
    logo_size = kwargs.get("logo_size", "medium")

    project_positions = kwargs.get(
        "project_positions", ["left", "bottom"]
    )
    logo_positions = kwargs.get("logo_positions", ["right", "bottom"])

    optimize = kwargs.get("optimize", True)
    quality = kwargs.get("quality", 100)
    compression = kwargs.get("compression", "jpeg")

    watermarks = kwargs.get("watermarks")

    iforeground = resizeImage(foreground, width, height)
    ibackground = resizeImage(background, width, height)

    icomp = Image.alpha_composite(ibackground, iforeground)

    lwidth, lheight = getLogoSize(project_size, width, height)
    iproject = resizeImage(project, lwidth, lheight)

    x, y = getPositions(
        width, height, project_positions, iproject.size
    )

    icomp.paste(iproject, (int(x), int(y)))

    lwidth, lheight = getLogoSize(logo_size, width, height)
    ilogo = resizeImage(logo, lwidth, lheight)

    x, y = getPositions(width, height, logo_positions, ilogo.size)

    icomp.paste(ilogo, (int(x), int(y)))

    if watermarks:
        icomp = watermarks(icomp, width, height, watermarks)
    icomp.save(
        output,
        optimize=optimize,
        quality=quality,
        compression=compression,
    )
    print(output)


def resizeImage(filepath, width, height):
    image = Image.open(filepath).convert("RGBA")
    image = image.resize([width, height], Image.ANTIALIAS)
    return image


def watermarks(image, width, height, context):
    idraw = ImageDraw.Draw(image)
    for item in context:
        watermark(idraw, width, height, **item)
    return image


def watermark(idraw, width, height, **kwargs):
    font = kwargs.get("font", "arialbd.ttf")
    align = kwargs.get("align", "left")
    size = kwargs.get("size", "medium")
    encoding = kwargs.get("encoding", "unic")
    color = kwargs.get("color", "white")
    positions = kwargs.get("positions", ["left", "top"])
    spacing = kwargs.get("spacing", "white")

    lines = textLines(kwargs["marks"])
    fontindex = getFontSize(size, width, height)

    ifont = ImageFont.truetype(
        font, size=fontindex, encoding=encoding
    )
    text_resolution = ifont.getsize_multiline(lines)

    x, y = getPositions(width, height, positions, text_resolution)

    idraw.text(
        (x, y),
        lines,
        font=ifont,
        fill=color,
        spacing=spacing,
        align=align,
        stroke_width=0,
        direction=None,
        language=None,
    )


def textLines(input):
    output = []
    for each in input:
        for k, v in each.items():
            output.append("%s: %s" % (k, v))
    output = "\n".join(output)
    return output


def getFontSize(size, iwidth, iheight):
    context = {"small": 1.46, "medium": 1.95, "large": 3.91}
    percentage = context[size]
    index = int((percentage * iwidth) / 100)
    return index


def getLogoSize(size, iwidth, iheight):
    context = {"small": 5, "medium": 10, "large": 20}
    percentage = context[size]
    w_index = int((percentage * iwidth) / 100)
    h_index = int((percentage * iheight) / 100)
    return w_index, h_index


def getPositions(iwidth, iheight, positions, resoultion):
    x_offset = (1.95 * iwidth) / 100
    y_offset = (1.95 * iheight) / 100

    x, y = x_offset, y_offset

    if positions[0] == "left":
        x = x_offset

    if positions[0] == "right":
        x = (iwidth - resoultion[0]) - x_offset

    if positions[0] == "middle":
        x = (iwidth / 2) - (resoultion[0] / 2)

    if positions[1] == "top":
        y = y_offset

    if positions[1] == "center":
        y = (iheight / 2) - (resoultion[1] / 2)

    if positions[1] == "bottom":
        y = (iheight - resoultion[1]) - x_offset

    return x, y


def convertToJpg(image, outputpath=None, resolution=[512, 512]):
    outputpath = outputpath or tempfile.mktemp(
        ".jpg", "JPEG", tempfile.gettempdir()
    )
    image = Image.open(image).convert("RGB")
    if resolution:
        image = image.resize(
            [resolution[0], resolution[1]], Image.ANTIALIAS
        )
    image.save(
        outputpath, optimize=True, quality=100, compression="jpeg"
    )
    return outputpath


if __name__ == "__main__":
    execute()
