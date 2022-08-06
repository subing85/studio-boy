::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@echo off

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
"%PYTHON-EXE%" -c "print ('\n')"
echo    Studio-Pipe Project Management in-house Tool.
echo    Simplify the project management and workflow for the animation and vfx teams.
echo    Main highlight are,
echo        1. Studio-Pipe can help to manage and coordinates work from different locations.
echo        2. Open-Source free tool.
echo    Copyright (c) 2021, https://www.subins-toolkits.com All rights reserved.
echo    Author: Subin. Gopi (subing85@gmail.com).
echo    Last modified: 2021:April:26:Monday-09:57:52:AM.
echo    Version: 0.0.1
echo    WARNING! All changes made in this file will be lost!.
echo    Description: this is batch script for management studio-pipe commands.
"%PYTHON-EXE%" -c "print ('\n')"

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
set LOGN-SRC="%LIBRARY-PATH%/library/login/__init__.py"
set APPS-SRC="%LIBRARY-PATH%/library/applications/__init__.py"
set PROJ-SRC="%LIBRARY-PATH%/library/project/__init__.py"
set STEP-SRC="%LIBRARY-PATH%/library/steps/__init__.py"
set TASK-SRC="%LIBRARY-PATH%/library/tasks/__init__.py"
set VERS-SRC="%LIBRARY-PATH%/library/versions/__init__.py"
set HELP-SRC="%LIBRARY-PATH%/library/help/__init__.py"
set TEST-DIR="%LIBRARY-PATH%/library/tests/__init__.py"
set COMD-DIR="%LIBRARY-PATH%/library/event/__init__.py"
set MTRM-DIR="%LIBRARY-PATH%/library/mtRemapping/__init__.py"
set NDRM-DIR="%LIBRARY-PATH%/library/ndRemapping/__init__.py"

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
set TEMP-USERNAME-ENVS=%tmp%/pipe-username-envs.bat
set TEMP-APPS-ENVS=%tmp%/pipe-app-envs.bat
set TEMP-PROJECT-ENVS=%tmp%/pipe-project-envs.bat

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

if %1==--set-username (
    echo "check-in with your user account, please wait!..."
    echo        source:%LOGN-SRC%
    "%PYTHON-EXE%" "%LOGN-SRC%" --set-username %2 --path %TEMP-USERNAME-ENVS%
    call %TEMP-USERNAME-ENVS%
    "%PYTHON-EXE%" "%LOGN-SRC%" --get-username
)

if %1==--get-username (
    echo "current check-in pipe user account, please wait!..."
    echo        source:%LOGN-SRC%
    "%PYTHON-EXE%" "%LOGN-SRC%" --get-username
)

if %1==--get-all-users (
    echo "finding all users from ftrack, please wait!..."
    echo        source:%LOGN-SRC%
    "%PYTHON-EXE%" "%LOGN-SRC%" --get-all-users
)

if %1==--login-history (
    echo "list out your login history, please wait!..."
    echo        source:%LOGN-SRC%
    "%PYTHON-EXE%" "%LOGN-SRC%" --login-history
)

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if %1==--create-project (
    echo "create the new project, please wait!..."
    echo        source:%PROJ-SRC%
    "%PYTHON-EXE%" "%PROJ-SRC%" --create-project %2 --template %4 %5 %6 --path %TEMP-PROJECT-ENVS%
)

if %1==--delete-project (
    echo "delete the existing project, please wait!..."
    echo        source:%PROJ-SRC%
    "%PYTHON-EXE%" "%PROJ-SRC%" --delete-project %2
)

if %1==--get-all-projects (
    echo "finding available projects in ftrack, please wait!..."
    echo        source:%PROJ-SRC%
    "%PYTHON-EXE%" "%PROJ-SRC%" --get-all-projects
)

if %1==--set-project (
    echo "check-in the project, please wait!..."
    echo        source:%PROJ-SRC%
    "%PYTHON-EXE%" "%PROJ-SRC%" --set-project %2 --path %TEMP-PROJECT-ENVS%
    call %TEMP-PROJECT-ENVS%
    "%PYTHON-EXE%" "%PROJ-SRC%" --get-project
)

if %1==--get-project (
    echo "finding current check-in pipe project, please wait!..."
    echo        source:%PROJ-SRC%
    "%PYTHON-EXE%" "%PROJ-SRC%" --get-project
)

if %1==--get-project-templates (
    echo "finding available project schema (template) in ftrack, please wait!..."
    echo        source:%PROJ-SRC%
    "%PYTHON-EXE%" "%PROJ-SRC%" --get-project-templates
)

if %1==--get-project-template (
    echo "finding current check-in project schema (template), please wait!..."
    echo        source:%PROJ-SRC%
    "%PYTHON-EXE%" "%PROJ-SRC%" --get-project-template
)

if %1==--get-project-categories (
    echo "finding current check-in project categories please wait!..."
    echo        source:%PROJ-SRC%
    "%PYTHON-EXE%" "%PROJ-SRC%" --get-project-categories
)

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if %1==--get-apps (
    echo "finding available applications under the configure, please wait!..."
    echo        source:%APPS-SRC%
    "%PYTHON-EXE%" "%APPS-SRC%" --get-apps
)

if %1==--set-envs (
    echo "setting the environments to specific application, please wait!..."
    echo        source:%APPS-SRC%
    "%PYTHON-EXE%" "%APPS-SRC%" --set-envs %2
    call %TEMP-APPS-ENVS%
)

if %1==--get-app-envs (
    echo "setting the environments to specific application, please wait!..."
    echo        source:%APPS-SRC%
    "%PYTHON-EXE%" "%APPS-SRC%" --get-app-envs
)


if %1==launch (
    echo "launch the studio-pipe configured application, please wait!..."
    echo        source:%APPS-SRC%
    "%PYTHON-EXE%" "%APPS-SRC%" --set-envs %2 --path %TEMP-APPS-ENVS%
    call %TEMP-APPS-ENVS%
    "%PYTHON-EXE%" "%APPS-SRC%" --launch %2
)

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if %1==--get-step-templates (
    echo "finding step templates from the current check-in project, please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --get-step-templates
)

if %1==--isAssetExists (
    echo "check-ing the asset is exists in the current check-in project, please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --isAssetExists %2
)

if %1==--create-asset (
    echo "create the new asset (register asset to ftrack), please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --create-asset %2 %3 %4 %5 %6 %7 %8
)

if %1==--delete-asset (
    echo "delete the asset from ftrack, please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --delete-asset %2
)

if %1==--get-assets (
    echo "finding available assets from the current check-in project, please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --get-assets %2
)

if %1==--get-asset-types (
    echo "finding asset types from the current check-in project, please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --get-asset-types
)

if %1==--isSequenceExists (
    echo "check-ing the sequence is exists in the current check-in project category, please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --isSequenceExists %2
)

if %1==--create-sequence (
    echo "create the new sequence (register sequence to ftrack), please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --create-sequence %2 %3 %4 %5 %6
)

if %1==--delete-sequence (
    echo "delete the sequence from ftrack, please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --delete-sequence %2
)

if %1==--get-sequences (
    echo "finding sequence details in the current check-in project category, please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --get-sequences %2
)

if %1==--isShotExists (
    echo "check-ing the sequence is exists in the current check-in project category, please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --isShotExists %2 %3 %4
)

if %1==--create-shot (
    echo "create the new shot (register shot to ftrack), please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --create-shot %2 %3 %4 %5 %6 %7 %8 %9 %*
)

if %1==--delete-shot (
    echo "delete the shot from ftrack, please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --delete-shot %2 %3 %4
)

if %1==--get-shots (
    echo "finding shot details in the current check-in project category, please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --get-shots %2 %3 %4
)

if %1==--get-status (
    echo "finding available entity status, please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --get-status
)

if %1==--get-tasks (
    echo "finding available tasks in the current check-in project specific template, please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --get-tasks %2
)

if %1==--get-step-tasks (
    echo "finding available tasks in the current check-in project specific step, please wait!..."
    echo        source:%STEP-SRC%
    "%PYTHON-EXE%" "%STEP-SRC%" --get-step-tasks %2
)

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if %1==--get-my-tasks (
    echo "finding user assigned tasks, please wait!..."
    echo        source:%TASK-SRC%
    "%PYTHON-EXE%" "%TASK-SRC%" --get-my-tasks
)

if %1==--get-task-dependency (
    echo "finding available dependency tasks of the specified  task, please wait!..."
    echo        source:%TASK-SRC%
    "%PYTHON-EXE%" "%TASK-SRC%" --get-task-dependency %2
)

if %1==--get-task-id (
    echo "finding task id from name of the task, please wait!..."
    echo        source:%TASK-SRC%
    "%PYTHON-EXE%" "%TASK-SRC%" --get-task-id %2
)

if %1==--start-my-task (
    echo "trigger the user task to start, please wait!..."
    echo        source:%TASK-SRC%
    "%PYTHON-EXE%" "%TASK-SRC%" --start-my-task %2
)

if %1==--submit-my-task (
    echo "trigger the user task to submit, please wait!..."
    echo        source:%TASK-SRC%
    "%PYTHON-EXE%" "%TASK-SRC%" --submit-my-task %2 %3 %4 %5 %6 %7 %8
)

if %1==--clear-submits (
    echo "delete the all submission from the specified task, please wait!..."
    echo        source:%TASK-SRC%
    "%PYTHON-EXE%" "%TASK-SRC%" --clear-submits %2
)

if %1==--decline-user-task (
    echo "trigger the user task to decline, please wait!..."
    echo        source:%TASK-SRC%
    "%PYTHON-EXE%" "%TASK-SRC%" --decline-user-task %2 %3 %4 %5 %6
)

if %1==--approved-user-task (
    echo "trigger the user task to approved, please wait!..."
    echo        source:%TASK-SRC%
    "%PYTHON-EXE%" "%TASK-SRC%" --approved-user-task %2 %3 %4 %5 %6
)

if %1==--publish-user-task (
    echo "trigger the user task to publish, please wait!..."
    echo        source:%TASK-SRC%
    "%PYTHON-EXE%" "%TASK-SRC%" --publish-user-task %2 %3 %4 %5 %6
)

if %1==--clear-publish (
    echo "delete the all publish of the specified task, please wait!..."
    echo        source:%TASK-SRC%
    "%PYTHON-EXE%" "%TASK-SRC%" --clear-publish %2
)

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if %1==--download-task (
    echo "download and deploy the task version level, please wait!..."
    echo        source:%VERS-SRC%
    "%PYTHON-EXE%" "%VERS-SRC%" --download-task %2 %3 True %4 %5
)

if %1==--download-step (
    echo "download and deploy the step level, please wait!..."
    echo        source:%VERS-SRC%
    "%PYTHON-EXE%" "%VERS-SRC%" --download-step %2 %3 True %4 %5
)

if %1==--download-category (
    echo "download and deploy the category level, please wait!..."
    echo        source:%VERS-SRC%
    "%PYTHON-EXE%" "%VERS-SRC%" --download-category %2 %3 True %4 %6
)

if %1==--download-all (
    echo "download and deploy all tasks in the current check-in project, please wait!..."
    echo        source:%TASK-SRC%
    "%PYTHON-EXE%" "%VERS-SRC%" --download-all %2 True %4 %5
)

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if %1==help (
    echo "help studio-pipe command , please wait!..."
    echo        source:%HELP-SRC%
    "%PYTHON-EXE%" "%HELP-SRC%" --helps
)

if %1==unittest (
    echo "unittest for pipe  code, please wait!..."
    echo        source:%TEST-DIR%
    "%PYTHON-EXE%" "%TEST-DIR%" --unittest %2 %3
)

if %1==black-check (
    echo "black formatter check - pipe source code, please wait!..."
    echo        source:%TEST-DIR%
    "%PYTHON-EXE%" -m black --check %2
)

if %1==black-fix (
    echo "black formatter fix - pipe source code, please wait!..."
    echo        source:%TEST-DIR%
    if "%~2"=="" (
        "%PYTHON-EXE%" -m black -l 70 %PIPELINE-PATH%
    ) else (
        "%PYTHON-EXE%" -m black -l 70 %2
    )    
)

if %1==unused-check (
    echo "unused imports and variables check - pipe source code, please wait!..."
    echo        source:%TEST-DIR%
    if "%~2"=="" (
        "%PYTHON-EXE%" "%TEST-DIR%" --unused "packages" --check
    ) else (
        "%PYTHON-EXE%" "%TEST-DIR%" --unused %2 --check
    )
)

if %1==unused-fix (
    echo "unused imports and variables fix -pipe source code, please wait!..."
    echo        source:%TEST-DIR%
    if "%~2"=="" (
        "%PYTHON-EXE%" "%TEST-DIR%" --unused "packages" --fix
    ) else (
        "%PYTHON-EXE%" "%TEST-DIR%" --unused %2 --fix
    )
)

if %1==clean (
    echo "unused imports and variables fix -pipe source code, please wait!..."
    echo        source:%TEST-DIR%
    "%PYTHON-EXE%" "%TEST-DIR%" --clean
)

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

if %1==event (
    echo "pipe event, please wait!..."
    echo        source:%TEST-DIR%
    "%PYTHON-EXE%" "%COMD-DIR%" --event %2
)

if %1==event-all (
    echo "pipe event, please wait!..."
    echo        source:%TEST-DIR%
    "%PYTHON-EXE%" "%COMD-DIR%" --event-all
)

if %1==event-name (
    echo "pipe event, please wait!..."
    echo        source:%TEST-DIR%
    "%PYTHON-EXE%" "%COMD-DIR%" --event-name %2
)

if %1==python (
    echo "pipe event, please wait!..."
    echo        source:%TEST-DIR%
    "%PYTHON-EXE%" %2 %3 %4 %5 %6
)

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if %1==MtRemapping (
    echo "pipe  MtRemapping, please wait!..."
    echo        source:%MTRM-DIR%
    
    if %2==example (
        "%PYTHON-EXE%" "%MTRM-DIR%" --example
    
    ) else (
        "%PYTHON-EXE%" "%MTRM-DIR%" -s %3 -f %5
    )
)

if %1==NdRemapping (
    echo "pipe  NdRemapping, please wait!..."
    echo        source:%NODERM-DIR%
    
    if %2==example (
        "%PYTHON-EXE%" "%NDRM-DIR%" --example
    
    ) else (
        "%PYTHON-EXE%" "%NDRM-DIR%" -s %3 -c %5
    )
)

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
