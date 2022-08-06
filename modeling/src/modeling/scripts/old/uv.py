import os
import json

from maya import cmds
from maya import OpenMaya


def imports(path):
    context = read(path)
    print("total geometry size %s" % len(context))
    for each in context:
        valid, message = set(each)
    return True


def exports(path, task=None):
    nodes = cmds.ls(type="mesh")
    uvs = []
    for node in nodes:
        context = get(node)
        uvs.append(context)
    write(uvs, task, path)
    return uvs


def write(context, task, path):
    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    context = {"type": "uv", "context": context, "task": task}
    with open(path, "w") as file:
        file.write(json.dumps(context, indent=2))
        return True


def read(path):
    data = None
    with (open(path, "r")) as file:
        data = json.load(file)
    if not data:
        return None
    if data.get("type") != "uv":
        raise ValueError("invalid uv data")
        return
    context = data.get("context")
    return context


def get(node):
    dagpath = getDagpath(node)
    mfn_mesh = OpenMaya.MFnMesh(dagpath)
    set_names = []
    mfn_mesh.getUVSetNames(set_names)
    context = []
    for index, set_name in enumerate(set_names):
        u_array = OpenMaya.MFloatArray()
        v_array = OpenMaya.MFloatArray()
        mfn_mesh.getUVs(u_array, v_array, set_name)
        uv_counts = OpenMaya.MIntArray()
        uv_ids = OpenMaya.MIntArray()
        mfn_mesh.getAssignedUVs(uv_counts, uv_ids, set_name)
        current_set_data = {
            "set_name": set_name.encode(),
            "u_array": list(u_array),
            "v_array": list(v_array),
            "uv_counts": list(uv_counts),
            "uv_ids": list(uv_ids),
            "order": index,
        }
        context.append(current_set_data)
    num_polygons, polygon_vertices = getFacesVertices(mfn_mesh)
    context = {
        "uv_sets": context,
        "long_name": dagpath.fullPathName().encode(),
        "short_name": dagpath.fullPathName().split("|")[-1],
        "shape_node": mfn_mesh.name().encode(),
        "num_polygons": num_polygons,
        "polygon_vertices": polygon_vertices,
    }
    return context


def set(node_context):
    node = node_context["shape_node"]
    uv_sets = node_context["uv_sets"]

    if not cmds.objExists(node):
        message = "not found geometry %s" % node
        OpenMaya.MGlobal.displayWarning(message)
        return False, message
    dagpath = getDagpath(node)
    mfn_mesh = OpenMaya.MFnMesh(dagpath)

    validate = validateGeometry(
        mfn_mesh,
        node_context["num_polygons"],
        node_context["polygon_vertices"],
    )

    if not validate:
        message = "invalid geometry topology <%s>" % node
        OpenMaya.MGlobal.displayWarning(message)
        return False, message

    clearUVs(mfn_mesh)

    set_names = []
    mfn_mesh.getUVSetNames(set_names)

    print("\n\tUV update <%s>" % node)
    for index, uv_set in enumerate(uv_sets):
        set_name = uv_set["set_name"]
        u_array = createFloatArray(uv_set["u_array"])
        v_array = createFloatArray(uv_set["v_array"])
        uv_counts = createIntArray(uv_set["uv_counts"])
        uv_ids = createIntArray(uv_set["uv_ids"])

        if index == 0:
            set_name = set_names[0]
        else:
            set_name = mfn_mesh.createUVSetWithName(set_name)
        # mfn_mesh.setCurrentUVSetName(set_name)
        mfn_mesh.setUVs(u_array, v_array, set_name)
        mfn_mesh.assignUVs(uv_counts, uv_ids, set_name)
        print("updated uv set name: ".rjust(25) + set_name)

    return True, None


def clear_selection():
    OpenMaya.MGlobal.clearSelectionList()


def getDagpath(node):
    mselection = OpenMaya.MSelectionList()
    mselection.add(node)
    mdag_path = OpenMaya.MDagPath()
    mselection.getDagPath(0, mdag_path)
    return mdag_path


def getFacesVertices(mfn_mesh):
    num_polygons = mfn_mesh.numPolygons()
    polygon_vertices = []
    for index in range(num_polygons):
        mint_array = OpenMaya.MIntArray()
        mfn_mesh.getPolygonVertices(index, mint_array)
        polygon_vertices.append(list(mint_array))
    return num_polygons, polygon_vertices


def validateGeometry(mfn_mesh, num_polygons, polygon_vertices):
    mesh_num_polygons, mesh_polygon_vertices = getFacesVertices(
        mfn_mesh
    )
    if num_polygons != mesh_num_polygons:
        print("geometry".rjust(35) + mfn_mesh.name())
        print(
            "scene mesh num polygons:".rjust(35) + mesh_num_polygons
        )
        print("model mesh num polygons:".rjust(35) + num_polygons)
        return False
    if polygon_vertices != mesh_polygon_vertices:
        print("geometry".rjust(35) + mfn_mesh.name())
        print(
            "scene mesh polygon vertices:".rjust(35)
            + mesh_polygon_vertices
        )
        print(
            "model mesh polygon vertices:".rjust(35)
            + polygon_vertices
        )
        return False
    return True


def createFloatArray(python_list):
    mfloat_array = OpenMaya.MFloatArray()
    mscript_util = OpenMaya.MScriptUtil()
    mscript_util.createFloatArrayFromList(python_list, mfloat_array)
    return mfloat_array


def createIntArray(python_list):
    mint_array = OpenMaya.MIntArray()
    mscript_util = OpenMaya.MScriptUtil()
    mscript_util.createIntArrayFromList(python_list, mint_array)
    return mint_array


def clearUVs(mfn_mesh):
    set_names = []
    mfn_mesh.getUVSetNames(set_names)
    delete_uvsets(mfn_mesh, set_names[1:])
    mfn_mesh.clearUVs()
    mfn_mesh.updateSurface()


def delete_uvsets(mfn_mesh, set_names):
    for set_name in set_names:
        try:
            mfn_mesh.deleteUVSet(set_name)
        except Exception as error:
            print("\nDeleteError %s" % error)
