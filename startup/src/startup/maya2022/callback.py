import os
import stat
import getpass

try:
    from maya import cmds
    from maya import OpenMaya
except Exception as error:
    pass


def callback_before_new(*args):
    print("\n#info Callback Before New Scene")
    remove_virus_from_scene()
    remove_virus_from_os()


def callback_after_new(*args):
    print("\n#info Callback After New Scene")
    remove_virus_from_scene()
    remove_virus_from_os()


def callback_before_open(*args):
    print("\n#info Callback Before Open Scene")
    remove_virus_from_scene()
    remove_virus_from_os()


def callback_after_open(*args):
    print("\n#info Callback After Open Scene")
    remove_virus_from_scene()
    remove_virus_from_os()


def callback_before_save(*args):
    print("\n#info Callback Before Save Scene")
    remove_virus_from_scene()
    remove_virus_from_os()


def callback_after_save(*args):
    print("\n#info Callback After Save Scene")
    remove_virus_from_scene()
    remove_virus_from_os()


def callback_before_import(*args):
    print("\n#info Callback Before Import Scene")
    remove_virus_from_scene()
    remove_virus_from_os()


def callback_after_import(*args):
    print("\n#info Callback After Import Scene")
    remove_virus_from_scene()
    remove_virus_from_os()


def callback_before_reference(*args):
    print("\n#info Callback Before Reference Scene")
    remove_virus_from_scene()
    remove_virus_from_os()


def callback_after_reference(*args):
    print("\n#info Callback After Reference Scene")
    remove_virus_from_scene()
    remove_virus_from_os()


def remove_virus_from_scene():
    scripts = cmds.ls(type="script")
    viruses = ["breed_gene", "vaccine_gene"]
    for each in scripts:
        for virus in viruses:
            if virus not in each:
                continue
            cmds.delete(each)
            print("#info removed script node", each)


def remove_virus_from_os(maya_path=True):
    if maya_path:
        script_dirnames = [
            cmds.internalVar(userAppDir=True) + "scripts",
            cmds.internalVar(userScriptDir=True),
        ]
    else:
        maya_dirname = os.path.expanduser("~/maya")
        script_dirnames = [
            os.path.join(maya_dirname, "2018", "scripts"),
            os.path.join(maya_dirname, "scripts"),
        ]

    viruses = ["vaccine", "breed"]
    for script_dirname in script_dirnames:
        for each in os.listdir(script_dirname):
            for virus in viruses:
                if virus not in each:
                    continue
                virus_path = os.path.join(script_dirname, each)
                try:
                    os.chmod(virus_path, stat.S_IWRITE)
                    os.remove(virus_path)
                    print("#info removed", virus_path)
                except Exception as error:
                    print(str(error))


if __name__ == "__main__":
    print(
        "\n#Studio Pipe Startup Script\n#info Callback Maya-2018 launch"
    )
    remove_virus_from_scene()
    remove_virus_from_os(maya_path=False)

    OpenMaya.MSceneMessage.addCallback(
        OpenMaya.MSceneMessage.kBeforeNew, callback_before_new
    )
    OpenMaya.MSceneMessage.addCallback(
        OpenMaya.MSceneMessage.kAfterNew, callback_after_new
    )

    OpenMaya.MSceneMessage.addCallback(
        OpenMaya.MSceneMessage.kBeforeOpen, callback_before_open
    )
    OpenMaya.MSceneMessage.addCallback(
        OpenMaya.MSceneMessage.kAfterOpen, callback_after_open
    )

    OpenMaya.MSceneMessage.addCallback(
        OpenMaya.MSceneMessage.kBeforeSave, callback_before_save
    )
    OpenMaya.MSceneMessage.addCallback(
        OpenMaya.MSceneMessage.kAfterSave, callback_after_save
    )

    OpenMaya.MSceneMessage.addCallback(
        OpenMaya.MSceneMessage.kBeforeImport, callback_before_import
    )

    OpenMaya.MSceneMessage.addCallback(
        OpenMaya.MSceneMessage.kAfterImport, callback_after_import
    )

    OpenMaya.MSceneMessage.addCallback(
        OpenMaya.MSceneMessage.kBeforeReference,
        callback_before_reference,
    )

    OpenMaya.MSceneMessage.addCallback(
        OpenMaya.MSceneMessage.kAfterReference,
        callback_after_reference,
    )
