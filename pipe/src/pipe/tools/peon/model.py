from apis import studio


def doIt(create, **kwargs):
    step = studio.Steps()

    category = kwargs.get("category")
    valid, message, entity = False, None, None
    if category == "assets":
        if create:
            valid, message, entity = step.createNewAsset(
                kwargs.get("name"),
                kwargs.get("type"),
                kwargs.get("template"),
                description=kwargs.get("description"),
                thumbnail=None,
            )
        else:
            valid, message, entity = step.updateExistsAsset(
                kwargs.get("step"),
                kwargs.get("type"),
                kwargs.get("template"),
                name=kwargs.get("name"),
                description=kwargs.get("description"),
                thumbnail=None,
            )
    if category == "sequence":
        if create:
            valid, message, entity = step.createNewSequence(
                kwargs.get("name"),
                timeunit=kwargs.get("fps"),
                range=[kwargs.get("fstart"), kwargs.get("fend")],
                description=kwargs.get("description"),
                thumbnail=None,
                metadata={
                    "sceneAssembly": str(
                        {"assets": kwargs.get("assembly")}
                    )
                },
            )
        else:
            valid, message, entity = step.updateExistsSequence(
                kwargs.get("step"),
                name=kwargs.get("name"),
                timeunit=kwargs.get("fps"),
                range=[kwargs.get("fstart"), kwargs.get("fend")],
                description=kwargs.get("description"),
                thumbnail=None,
                metadata={
                    "sceneAssembly": str(
                        {"assets": kwargs.get("assembly")}
                    )
                },
            )
    if category == "shots":
        if create:
            if kwargs.get("sequence"):
                parent = kwargs["sequence"]
            else:
                parentitem = kwargs.get("widgetitem").parent()
                parent = parentitem.entity
            if not parent:
                message = (
                    "shot <%s> parent not yet created"
                    % kwargs.get("name")
                )
                valid, entity = False, None
            else:
                valid, message, entity = step.createNewShot(
                    kwargs.get("name"),
                    parent["name"],
                    kwargs.get("template"),
                    range=[kwargs.get("fstart"), kwargs.get("fend")],
                    thumbnail=None,
                    description=kwargs.get("description"),
                    metadata={
                        "sceneAssembly": str(
                            {"assets": kwargs.get("assembly")}
                        )
                    },
                )
        else:
            valid, message, entity = step.updateExistsShot(
                kwargs.get("step"),
                kwargs.get("template"),
                name=kwargs.get("name"),
                range=[kwargs.get("fstart"), kwargs.get("fend")],
                description=kwargs.get("description"),
                thumbnail=None,
                metadata={
                    "sceneAssembly": str(
                        {"assets": kwargs.get("assembly")}
                    )
                },
            )
    return valid, message, entity


if __name__ == "__main__":
    pass
