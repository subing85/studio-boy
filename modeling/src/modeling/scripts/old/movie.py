import tempfile


def create_script(context):
    lines = [
        "import glob",
        "from apis.media import pitcher",
        "kwargs = %s" % str(context),
        "image = kwargs['images']",
        "pathname = '%s*.*' % image",
        "images = glob.glob(pathname)",
        "cframe = kwargs.get('fstart')",
        "outputs = []",
        "for image in images:",
        "\tkwargs['forground'] = image",
        "\tkwargs['cframe'] = cframe",
        "\toutput = pitcher.Connect.stamping(**kwargs)",
        "\toutputs.append(output)",
        "\tif cframe:",
        "\t\tcframe += 1",
        "print ('success, Studio Stamping')",
        "pitcher.Connect.create(",
        "\toutputs, kwargs['moviepath'], kwargs['fps'], kwargs.get('resolution'))",
        "print ('movie path', kwargs['moviepath'])",
        "print ('success, Studio Movie')",
    ]
    path = tempfile.mktemp(".py")
    with (open(path, "w")) as script:
        script.write("\n".join(lines))
        return path


def example():
    import glob
    from apis.media import pitcher

    kwargs = {
        "background": "G:/abc/abc-studio/pipeline/animation/0.0.1/animation/bake/images/background.tiff",
        "font": "arialbd.ttf",
        "fps": 24,
        "fstart": 1001,
        "images": u"B:/projects/MSH/scene/101/101/layout/work/tmp_spa3q/turnaround",
        "moviepath": u"B:/projects/MSH/scene/101/101/layout/work/turnaround.avi",
        "project": False,
        "project_logo": "c:/users/sid/appdata/local/temp/Project6l1mc7.jpg",
        "resolution": [1920, 1080],
        "size": 20,
        "studio_logo": "G:/abc/abc-studio/pipeline/pipe/0.0.1/pipe/resources/icons/abc-logo.png",
        "task_context": [
            {"name": u"101"},
            {"step": u"layout"},
            {"category": u"scene"},
            {"project": u"My Super Hero"},
        ],
        "user_context": [
            {u"davidmiller@abcstudios.com": "email"},
            {u"David Miller": "name"},
            {u"artist": "type"},
            {"2021:07:04-02:51:PM": "date"},
        ],
    }
    image = kwargs["images"]
    pathname = "%s*.*" % image
    images = glob.glob(pathname)
    cframe = kwargs.get("fstart")
    outputs = []
    for image in images:
        kwargs["forground"] = image
        kwargs["cframe"] = cframe
        output = pitcher.Connect.stamping(**kwargs)
        outputs.append(output)
        if cframe:
            cframe += 1
    print("success, Studio Stamping")
    pitcher.Connect.create(
        outputs,
        kwargs["moviepath"],
        kwargs["fps"],
        kwargs.get("resolution"),
    )
    print("movie path", kwargs["moviepath"])
    print("success, Studio Movie")
