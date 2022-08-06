import importlib
from pipe.core import media

importlib.reload(media)


context = {
    "background": "Z:/devkit/pipeline/common/src/common/resources/images/modeling/background.tif",
    "foreground": "C:/Users/sid/AppData/Local/Temp/modelingodeqsrib/raja.jpg",
    # 'project': 'C:/Users/sid/AppData/Local/Temp/JPEGz6so8xxa.jpg',
    "project": "Z:/devkit/pipeline/example/JPEG_H.jpg",
    "project_positions": ["left", "bottom"],
    "project_size": "medium",
    "resolution": [1024, 1024],
    "studio": "Z:/devkit/pipeline/common/src/common/resources/icons/subins_toolkit_logo.png",
    "studio_positions": ["right", "bottom"],
    "studio_size": "medium",
    "watermarks": [
        {
            "align": "left",
            "color": "black",
            "enable": True,
            "encoding": "unic",
            "font": "arialbd.ttf",
            "marks": [
                {"subing85@gmail.com": "email"},
                {"subin gopi": "name"},
                {"Administrator": "type"},
                {"2022:04:15-12:50:PM": "date"},
            ],
            "positions": ["left", "top"],
            "size": "medium",
            "spacing": 8,
            "stroke_width": 0,
        },
        {
            "align": "right",
            "color": "black",
            "enable": True,
            "encoding": "unic",
            "font": "arialbd.ttf",
            "marks": [
                {"id": "dbdf6a7b-7a08-48de-8791-04acdadbfd27"},
                {"name": "raja"},
                {"type": "Character"},
                {"step": "Modeling"},
                {"category": "assets"},
                {"project": "Raja and Rani"},
            ],
            "positions": ["right", "top"],
            "size": "medium",
            "spacing": 8,
            "stroke_width": 0,
        },
    ],
}


meda = media.Connect()
output = "Z:/devkit/pipeline/common/src/common/resources/abcd.jpg"
# context.update({"format": "JPEG", "mode": "RGB"})

meda.composite(output, **context)
