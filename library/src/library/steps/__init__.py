# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:02:Sunday-04:08:34:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe project step commands.

import optparse

from apis import studio
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


def execute():
    """
    :description
        studio-pipe project step commands.
        to create and query the assets, sequence and shots.
        make sure to login with your user name and check-in with respective project.

    :examples
        \u2022 pipe --get-step-templates
            get the current check-in project available step templates schema.
                :param None

        \u2022 pipe --isAssetExists
            check the asset is exists in the current check-in project.
                :param <str>  asset name

        \u2022 pipe --create-asset "ball" --type "Character" --template "Character" --icon "Z:/icons/ball.png"
            create the new asset in the current check-in project.
                :param <str> asset name
                :param --type <str> --type asset type name (such as Character, Prop, etc)
                :param --template <str> step template name
                :param --icon <str>, icon path (optional)

        \u2022 pipe --delete-asset all
            delete all registered assets from current check-in project.
                :param <str> "all"

        \u2022 pipe --delete-asset "ball"
            delete asset based on the name of the asset.
                :param <str> asset name

        \u2022 pipe --get-assets "all"
            get the current check-in project all assets.
                :param <str> "all"

        \u2022 pipe --get-assets "Character"
            get the current check-in project assets based on the asset type.
                :param <str> asset type

        \u2022 pipe --get-asset-types
            get the current check-in project asset types such as character, prop, etc.
                :param None

        \u2022 pipe --isSequenceExists "101"
            check the sequence is exists in the current check-in project.
                :param <str>  sequence name

        \u2022 pipe --create-sequence "102" --icon "Z:/icons/sequence.png" --description "tests sequence"
            create the new sequence in the current check-in project.
                :param <str> sequence name
                :param --icon <str>, icon path (optional)
                :param --description <str> description (optional)

        \u2022 pipe --delete-sequence "all"
            delete the all registered sequence from current check-in project.
                :param <str> "all"

        \u2022 pipe --delete-sequence "101"
            delete sequence based on the name of the sequence.
                :param <str> sequence name

        \u2022 pipe --get-sequence "all"
            get the current check-in project all sequence.
                :param <str> "all"

        \u2022 pipe --get-sequence "101"
            get the current check-in project sequence based on the name.
                :param <str> sequence name


        \u2022 pipe --isShotExists "1001" --parent "101"
            check the shot is exists in the current check-in project.
                :param <str> shot name
                :param --parent <str> sequence name

        \u2022 pipe --create-shot "101-tests" --parent "101" --template "3D" --range "1001, 1025" --icon "Z:/icons/sequence.png" --description "tests shot"
            create the new shot in the current check-in project.
                :param <str> shot name
                :param --parent <str> sequence name
                :param --template <str> template name
                :param --range <str> shot frame range (optional)
                :param --icon <str>, icon path (optional)
                :param --description <str> description (optional)

        \u2022 pipe --delete-shot "101-tests" --parent "101"
            delete the shot from current check-in project.
                :param <str> sequence name

        \u2022 pipe --delete-shot "all" --parent "101"
            get the current check-in project all shot from specific sequence.
                :param <str> sequence name

        \u2022 pipe --get-shots "101" --parent "101"
            get the current check-in project all shot or shot based on the name.
                :param <str> shot name
                :param --parent <str> sequence name

        \u2022 pipe --get-shots "all" --parent "101"
            get the current check-in project all shot under the specific sequence.
                :param <str> "all"
                :param --parent <str> sequence name

        \u2022 pipe --get-shots "all" --parent "all"
            get the current check-in project all shot under the all sequence.
                :param <str> "all"
                :param --parent <str> "all"

        \u2022 pipe --get-status
            get the available ftrack status entity values.
                :param None

        \u2022 pipe --get-tasks "Character"
            get the tasks from the current check-in project specific template.
                :param <str> "template name"  or "all"

        \u2022 pipe --get-step-tasks "jocker"
            to get the current project step tasks
                :param <str> "step name"
    """

    parser = optparse.OptionParser(
        usage="usage: %prog [options] studio-pipe user login commands.",
        version="0.0.1",
    )

    option_list = [
        optparse.make_option(
            "--get-step-templates",
            dest="getStepTemplates",
            action="store_true",
            default=False,
            help="get the current check-in project available step templates schema.",
        ),
        optparse.make_option(
            "--isAssetExists",
            dest="isAssetExists",
            default=None,
            action="store",
            help="check the asset is exists in the project.",
        ),
        optparse.make_option(
            "--create-asset",
            dest="createAsset",
            default=None,
            action="store",
            help="create the new asset in the current check-in project.",
        ),
        optparse.make_option(
            "--delete-asset",
            dest="deleteAsset",
            default=None,
            action="store",
            help="delete asset based on the name of the asset or all",
        ),
        optparse.make_option(
            "--get-assets",
            dest="getAssets",
            default=None,
            action="store",
            help="get the current check-in project assets based on the asset type.",
        ),
        optparse.make_option(
            "--get-asset-types",
            dest="getAssetTypes",
            action="store_true",
            default=False,
            help="get the current check-in project asset types such as character, prop, etc.",
        ),
        optparse.make_option(
            "--isSequenceExists",
            dest="isSequenceExists",
            default=None,
            action="store",
            help="check the sequence is exists in the current check-in project.",
        ),
        optparse.make_option(
            "--create-sequence",
            dest="createSequence",
            default=None,
            action="store",
            help="create the new sequence in the current check-in project.",
        ),
        optparse.make_option(
            "--delete-sequence",
            dest="deleteSequence",
            default=None,
            action="store",
            help="delete the sequence from current check-in project.",
        ),
        optparse.make_option(
            "--get-sequences",
            dest="getSequences",
            default=None,
            action="store",
            help="get the current check-in project all sequences or sequence based on the name.",
        ),
        optparse.make_option(
            "--isShotExists",
            dest="isShotExists",
            default=None,
            action="store",
            help="check the shot is exists in the current check-in project.",
        ),
        optparse.make_option(
            "--create-shot",
            dest="createShot",
            default=None,
            action="store",
            help="create the new shot in the current check-in project.",
        ),
        optparse.make_option(
            "--delete-shot",
            dest="deleteShot",
            default=None,
            action="store",
            help="delete the shot from current check-in project.",
        ),
        optparse.make_option(
            "--get-shots",
            dest="getShots",
            default=None,
            action="store",
            help="get the current check-in project all shot or shot based on the name.",
        ),
        optparse.make_option(
            "--get-status",
            dest="getStatus",
            action="store_true",
            default=False,
            help="get the available ftrack status entity values.",
        ),
        optparse.make_option(
            "--get-tasks",
            dest="getTasks",
            action="store",
            help="get the tasks from the current check-in project specific templates.",
        ),
        optparse.make_option(
            "--get-step-tasks",
            dest="getStepTasks",
            action="store",
            help="get the step tasks from current project.",
        ),
        optparse.make_option(
            "--template",
            dest="template",
            action="store",
            help="input parameter of the template.",
        ),
        optparse.make_option(
            "--type",
            dest="type",
            action="store",
            help="input parameter of the type.",
        ),
        optparse.make_option(
            "--icon",
            dest="thumbnail",
            action="store",
            help="input parameter of the thumbnail.",
        ),
        optparse.make_option(
            "--description",
            dest="description",
            action="store",
            help="input parameter of the description.",
        ),
        optparse.make_option(
            "--parent",
            dest="parent",
            action="store",
            help="input parameter of the parent.",
        ),
        optparse.make_option(
            "--range",
            dest="range",
            action="store",
            help="input parameter of the range.",
        ),
    ]

    parser.add_options(option_list)
    (options, args) = parser.parse_args()

    login = studio.Login()
    stats = studio.Status()
    steps = studio.Steps()

    if not login.isValidLogin():
        print("\n")
        LOGGER.warning(
            'login and try, use this event pipe --set-username "_ _ _"'
        )
        print("\n")
        return

    if not stats.isInProject():
        print("\n")
        LOGGER.warning(
            'not check-in the project, use this event pipe --set-project "_ _ _"'
        )
        print("\n")
        return

    if options.getStepTemplates:
        steps.getStepTemplates()
        return

    if options.isAssetExists:
        steps.isAssetExists(options.isAssetExists)
        return

    if options.createAsset:
        steps.createNewAsset(
            options.createAsset,
            options.type,
            options.template,
            thumbnail=options.thumbnail,
        )
        return

    if options.deleteAsset:
        name = options.deleteAsset
        if options.deleteAsset == "all":
            name = None
        steps.deleteAsset(name)
        return

    if options.getAssets:
        typed = options.getAssets
        if options.getAssets == "all":
            typed = None
        steps.getAssets(typed)
        return

    if options.getAssetTypes:
        steps.getAssetTypes()
        return

    if options.isSequenceExists:
        steps.isSequenceExists(options.isSequenceExists)
        return

    if options.createSequence:
        steps.createNewSequence(
            options.createSequence,
            thumbnail=options.thumbnail,
            description=options.description,
        )
        return

    if options.deleteSequence:
        name = options.deleteSequence
        if options.deleteSequence == "all":
            name = None
        steps.deleteSequence(name)
        return

    if options.getSequences:
        name = options.getSequences
        if options.getSequences == "all":
            name = None
        steps.getSequences(name)
        return

    if options.isShotExists:
        steps.isShotExists(options.isShotExists, options.parent)
        return

    if options.createShot:
        range = None
        if options.range:
            range = options.range.split(", ")
            range = int(range[0]), int(range[1])
        steps.createNewShot(
            options.createShot,
            options.parent,
            options.template,
            range=range,
            thumbnail=options.thumbnail,
            description=options.description,
        )
        return

    if options.deleteShot:
        name = options.deleteShot
        if options.deleteShot == "all":
            name = None
        steps.deleteShot(options.parent, name)
        return

    if options.getShots:
        parent = options.parent
        name = options.getShots
        if options.parent == "all":
            parent = None
        if options.getShots == "all":
            name = None
        steps.getShots(parent, name)
        return

    if options.getStatus:
        stats.getTaskStatus()
        return

    if options.getTasks:
        template = options.getTasks
        if options.getTasks == "all":
            template = None
        steps.getTasks(template)
        return

    if options.getStepTasks:
        steps.getStepTasks(options.getStepTasks)
        return


if __name__ == "__main__":
    execute()
