MAIN = None


def getTriggerContext(trigger):
    contexts = getContext()
    if not contexts:
        return
    contexts = list(
        filter(lambda k: k["trigger"] == trigger, contexts)
    )
    if not contexts:
        return
    return contexts[0]


def getAllWidgets():
    contexts = getContext()
    if not contexts:
        return
    widgets = []
    for each in contexts:
        if not each.get("visibility"):
            continue
        if isinstance(each["visibility"], list):
            widgets.extend(each["visibility"])
        if isinstance(each["visibility"], str):
            widgets.append(each["visibility"])
    return widgets


def getContext():
    if not MAIN:
        return
    contexts = [
        {
            "trigger": "Start",
            "visibility": [MAIN.label_tag, MAIN.button_start],
            "clear": [MAIN.treewidget, MAIN.textedit_comments],
            "values": {MAIN.combobox_semanticversion: 0},
            "disable": [MAIN.treewidget],
        },
        {
            "trigger": "Submit",
            "visibility": [
                MAIN.label_tag,
                MAIN.button_status,
                MAIN.label_versions,
                MAIN.combobox_versions,
                MAIN.label_semanticversion,
                MAIN.combobox_semanticversion,
                MAIN.label_nextversion,
                MAIN.lineedit_nextversion,
                MAIN.label_comments,
                MAIN.textedit_comments,
                MAIN.button_submit,
                MAIN.button_deploy,
            ],
            "clear": [MAIN.treewidget, MAIN.textedit_comments],
            "values": {MAIN.combobox_semanticversion: 0},
            "enable": [MAIN.treewidget],
        },
        {
            "trigger": "Approved",
            "visibility": [
                MAIN.label_tag,
                MAIN.button_status,
                MAIN.label_versions,
                MAIN.combobox_versions,
                MAIN.label_semanticversion,
                MAIN.combobox_semanticversion,
                MAIN.label_nextversion,
                MAIN.lineedit_nextversion,
                MAIN.label_comments,
                MAIN.textedit_comments,
                MAIN.button_decline,
                MAIN.button_approved,
                MAIN.button_deploy,
            ],
            "clear": [MAIN.treewidget, MAIN.textedit_comments],
            "values": {MAIN.combobox_semanticversion: 0},
            "disable": [MAIN.treewidget],
        },
        {
            "trigger": "Publish",
            "visibility": [
                MAIN.label_tag,
                MAIN.button_status,
                MAIN.label_versions,
                MAIN.combobox_versions,
                MAIN.label_semanticversion,
                MAIN.combobox_semanticversion,
                MAIN.label_nextversion,
                MAIN.lineedit_nextversion,
                MAIN.label_comments,
                MAIN.textedit_comments,
                MAIN.button_decline,
                MAIN.button_publish,
                MAIN.button_deploy,
            ],
            "clear": [MAIN.treewidget, MAIN.textedit_comments],
            "values": {MAIN.combobox_semanticversion: 0},
            "disable": [MAIN.treewidget],
        },
        {
            "trigger": "Completed",
            "visibility": [
                MAIN.label_tag,
                MAIN.button_status,
                MAIN.label_versions,
                MAIN.combobox_versions,
                MAIN.label_semanticversion,
                MAIN.combobox_semanticversion,
                MAIN.label_nextversion,
                MAIN.lineedit_nextversion,
                MAIN.label_comments,
                MAIN.textedit_comments,
                MAIN.button_decline,
                MAIN.button_publish,
                MAIN.button_deploy,
            ],
            "clear": [MAIN.treewidget, MAIN.textedit_comments],
            "values": {MAIN.combobox_semanticversion: 0},
            "enable": [MAIN.treewidget],
        },
        {
            "trigger": "Status",
            "visibility": [MAIN.label_tag, MAIN.button_status],
        },
    ]
    return contexts
