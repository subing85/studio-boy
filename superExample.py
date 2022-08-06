import os


def doIt(directory, name, format):

    for index, each in enumerate(os.listdir(directory)):
        filepath = os.path.join(directory, each)
        if os.path.splitext(filepath)[-1] != format:
            continue
        padding = str(index + 1).zfill(4)
        # newFilepath =
        filename = "%s-%s%s" % (name, padding, format)
        newfilepath = os.path.join(directory, filename)
        print(filename)
        abc = os.renames(filepath, newfilepath)


if __name__ == "__main__":
    directory = r"C:\Users\sid\Downloads\a"
    name = "LauraSaenz"
    format = ".mp4"
    doIt(directory, name, format)
