import os
import stat
import shutil

CURRENT_PATH = os.path.dirname(__file__)

print(CURRENT_PATH)

if __name__ == "__main__":
    directory = os.path.dirname(CURRENT_PATH)
    for dir, folder, files in os.walk(directory):
        for file in files:
            current_file = os.path.join(dir, file)
            if file.endswith("Thumbs.db"):
                print("removed %s" % current_file)
                os.chmod(current_file, stat.S_IWRITE)
                os.remove(current_file)
            if not file.endswith(".pyc"):
                continue
            print("removed %s" % current_file)
            os.chmod(current_file, stat.S_IWRITE)
            os.remove(current_file)
        if dir.endswith("__pycache__"):
            os.chmod(dir, stat.S_IWRITE)
            shutil.rmtree(dir)
            print("removed %s" % dir)
    print("done!...")
