import os
import cv2
import tempfile

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class Connect(object):
    def __init__(self, **kwargs):
        super(Connect, self).__init__(**kwargs)

    def createMove(self, imageSequence, output, **kwargs):
        fps = kwargs.get("fps", 24)
        resolution = kwargs.get("resolution", None)

        frame = cv2.imread(imageSequence[0])
        if not resolution:
            height, width, layers = frame.shape
            resolution = (height, width)
        if not os.path.isdir(os.path.dirname(output)):
            os.makedirs(os.path.dirname(output))
        out = cv2.VideoWriter(
            output, cv2.VideoWriter_fourcc(*"DIVX"), fps, resolution
        )
        for image in imageSequence:
            out.write(cv2.imread(image))
        cv2.destroyAllWindows()
        out.release()
        return output

    def createImage(self, output, **kwargs):
        image = self.composite(output, **kwargs)
        return image

    def composite(self, output, **kwargs):

        mode = kwargs.get("mode", "RGB")
        format = kwargs.get("format", "JPEG")

        width, height = kwargs.get("resolution", [1024, 1024])

        foreground = kwargs.get("foreground")
        background = kwargs.get("background")
        project = kwargs.get("project")
        studio = kwargs.get("studio")

        project_size = kwargs.get("project_size", "medium")
        studio_size = kwargs.get("studio_size", "medium")

        project_positions = kwargs.get(
            "project_positions", ["left", "bottom"]
        )
        studio_positions = kwargs.get(
            "studio_positions", ["right", "bottom"]
        )

        optimize = kwargs.get("optimize", True)
        quality = kwargs.get("quality", 100)
        compression = kwargs.get("compression", "jpeg")

        watermarks = kwargs.get("watermarks")

        iforeground = self.resizeImage(
            foreground, width, height, "RGBA"
        )
        ibackground = self.resizeImage(
            background, width, height, "RGBA"
        )

        icomp = Image.alpha_composite(ibackground, iforeground)
        icomp = icomp.convert(mode)

        lwidth, lheight = self.getLogoSize(
            project_size, width, height
        )
        iproject = self.resizeImage(
            project, lwidth, lheight, "RGBA", aspectRatio=True
        )

        x, y = self.getPositions(
            width, height, project_positions, iproject.size
        )

        icomp.paste(iproject, (int(x), int(y)), iproject)

        lwidth, lheight = self.getLogoSize(studio_size, width, height)
        istudio = self.resizeImage(
            studio, lwidth, lheight, "RGBA", aspectRatio=True
        )

        x, y = self.getPositions(
            width, height, studio_positions, istudio.size
        )

        icomp.paste(istudio, (int(x), int(y)), istudio)

        if watermarks:
            icomp = self.watermarks(icomp, width, height, watermarks)

        context = {
            "mode": mode,
            "format": format,
            "optimize": optimize,
            "quality": quality,
            "compression": compression,
        }

        if not os.path.isdir(os.path.dirname(output)):
            os.makedirs(os.path.dirname(output))

        icomp.save(output, **context)
        # icomp.save(output, mode=mode, format=format, optimize=optimize, quality=quality, compression=compression)
        return output

    def resizeImage(self, filepath, width, height, mode, **kwargs):
        aspectRatio = kwargs.get("aspectRatio", False)
        image = Image.open(filepath).convert(mode)
        if (
            aspectRatio
        ):  # get the aspect ratio value based on source image height
            percentage = (image.width * width) / 100
            width = int((percentage / image.height) * 100)
            height = int((percentage / image.width) * 100)
        image = image.resize(
            [width, height], resample=Image.Resampling.NEAREST
        )
        return image

    def saveResizeImage(self, filepath, **kwargs):
        width = kwargs.get("width", 1024)
        height = kwargs.get("height", 1024)
        mode = kwargs.get("mode", "RGBA")
        aspectRatio = kwargs.get("aspectRatio", False)
        format = kwargs.get("format", "JPEG")
        optimize = kwargs.get("optimize", True)
        quality = kwargs.get("quality", 100)
        compression = kwargs.get("compression", "jpeg")
        outputPath = kwargs.get("outputPath", filepath)

        image = self.resizeImage(
            filepath, width, height, mode, aspectRatio=aspectRatio
        )

        context = {
            "mode": mode,
            "format": format,
            "optimize": optimize,
            "quality": quality,
            "compression": compression,
        }
        image.save(outputPath, **context)
        return outputPath

    def watermarks(self, image, width, height, context):
        idraw = ImageDraw.Draw(image)
        for item in context:
            self.watermark(idraw, width, height, **item)
        return image

    def watermark(self, idraw, width, height, **kwargs):
        font = kwargs.get("font", "arialbd.ttf")
        align = kwargs.get("align", "left")
        size = kwargs.get("size", "medium")
        encoding = kwargs.get("encoding", "unic")
        color = kwargs.get("color", "white")
        positions = kwargs.get("positions", ["left", "top"])
        spacing = kwargs.get("spacing", "white")

        lines = self.textLines(kwargs["marks"])
        fontindex = self.getFontSize(size, width, height)

        ifont = ImageFont.truetype(
            font, size=fontindex, encoding=encoding
        )
        text_resolution = ifont.getsize_multiline(lines)

        x, y = self.getPositions(
            width, height, positions, text_resolution
        )

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

    def textLines(self, input):
        output = []
        for each in input:
            for k, v in each.items():
                output.append("%s: %s" % (k, v))
        output = "\n".join(output)
        return output

    def getFontSize(self, size, iwidth, iheight):
        context = {"small": 1.46, "medium": 1.95, "large": 3.91}
        percentage = context[size]
        index = int((percentage * iwidth) / 100)
        return index

    def getLogoSize(self, size, iwidth, iheight):
        context = {"small": 5, "medium": 10, "large": 20}
        percentage = context[size]
        width = int((percentage * iwidth) / 100)
        height = int((percentage * iheight) / 100)
        return width, height

    def getPositions(self, iwidth, iheight, positions, resoultion):
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

    def convertToJpg(
        self, image, outputpath=None, resolution=[512, 512]
    ):
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

    def example(self):
        watermarks = [
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
                    {"Email": "subing85@gmail.com"},
                    {"Username": "subingopi"},
                    {"User Role": "Administrator"},
                ],
            },
            {
                "font": "arialbd.ttf",
                "encoding": "unic",
                "size": "medium",
                "positions": ["right", "top"],
                "spacing": 8,
                "align": "right",
                "color": "black",
                "stroke_width": 0,
                "marks": [
                    {"project": "RAR"},
                    {"name": "batman"},
                    {"step": "modeling"},
                    {"type": "character"},
                    {
                        "released-at": "2022:January:25:Tuesday-07:53:11:PM"
                    },
                    {"released-by": "tony.williams@example.com"},
                    {"kind": "submit"},
                    {"status": "Approved"},
                    {"version": "0.0.2"},
                ],
            },
            {
                "font": "arialbd.ttf",
                "encoding": "unic",
                "size": "medium",
                "positions": ["middle", "bottom"],
                "spacing": 8,
                "align": "left",
                "color": "black",
                "stroke_width": 0,
                "marks": [
                    {"frame": 1001},
                ],
            },
        ]

        context = {
            "resolution": [1024, 1024],
            "foreground": "E:/venture/source_code/studio-pipe/devkit/pipeline/common/src/common/resources/icons/playblast_0000001001.tif",
            "background": "E:/venture/source_code/studio-pipe/devkit/pipeline/common/src/common/resources/icons/background.tiff",
            "project": "E:/venture/source_code/studio-pipe/devkit/pipeline/common/src/common/resources/icons/show.png",
            "studio": "E:/venture/source_code/studio-pipe/devkit/pipeline/common/src/common/resources/icons/subins_toolkit_logo.png",
            "project_size": "medium",
            "studio_size": "medium",
            "project_positions": ["left", "bottom"],
            "studio_positions": ["right", "bottom"],
            "watermarks": watermarks,
        }

        # con = Connect()
        # output = "E:/venture/source_code/studio-pipe/devkit/pipeline/common/src/common/resources/icons/out.tif"
        # con.composite(output, **context)


if __name__ == "__main__":
    pass

# ===================================================================================================
#     con = Connect()
#
#     filepath = "C:/Users/sid/AppData/Local/Temp/raja-Lookdev-_mrr7vsh/sourceimages/belt.png"
#     image = con.resizeImage(filepath, 512, 512, "RGB", aspectRatio=True)
#
#     context = {
#         "mode": "RGB",
#         "format": "JPEG",
#         "optimize": True,
#         "quality": 100,
#         "compression": "jpeg",
#     }
#     filepath = "C:/Users/sid/AppData/Local/Temp/raja-Lookdev-_mrr7vsh/sourceimages/belt1.png"
#     abc = image.save(filepath, **context)
#     for a in dir(image):
#         print (a)
# ===================================================================================================
