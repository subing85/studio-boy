import os

from apis import studio


os.environ["PIPE-USER-EMAIL"] = "subing85@gmail.com"
os.environ["PIPE-USER-ID"] = "bcdf57b0-acc6-11e1-a554-f23c91df1211"
os.environ["PIPE-USER-NAME"] = "subingopi"
os.environ["PIPE-USER-DISCIPLINE"] = "Administrator"

os.environ["PROJECT-NAME"] = "RAR"
os.environ["PROJECT-FULL-NAME"] = "Ranj and Rani"
os.environ["PROJECT-ID"] = "ad54bf94-ba83-41d3-899d-9ed3dc1ab699"
os.environ[
    "PROJECT-THUMBNAIL"
] = "b160a733-07be-4c7f-b2f0-84f179b8be97"
os.environ["PROJECT-PATH"] = "Z:/projects/RAR"


#===================================================================================================
# os.environ["MAYA_VERSION"] = "maya2022"
# os.environ["MAYA_PLUG_IN_PATH"] = "Z:/devkit/pipeline/resources/src/resources/maya2022/plug-ins"
# os.environ["MAYA_SCRIPT_PATH"] = "Z:/devkit/pipeline/resources/src/resources/maya2022/scripts"
# os.environ["MAYA_SHELF_PATH"] = "Z:/devkit/pipeline/resources/src/resources/maya2022/shelves"
# os.environ["PIPE-APPLICATION-NAME"] = "maya2022"
#===================================================================================================

appn = studio.Applications()
contexts = appn.get()
current_application = "maya2022"
appn.startLaunch(current_application, thread=True)
