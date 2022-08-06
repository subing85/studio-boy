import os
import json

from pipe import utils
from pipe import resources

from pipe.core import logger
from pipe.core import ftrack
from pipe.core import inputs

LOGGER = logger.getLogger(__name__)

from pprint import pprint


class Connect(ftrack.Connect):

    entity = "CustomAttributeConfiguration"
    typeEntity = "CustomAttributeType"
    objectTypeEntity = "ObjectType"

    def __init__(self, entity=entity, **kwargs):
        super(Connect, self).__init__(entity, **kwargs)

        self.attributes_input = inputs.Connect("attributes")

    def searchAttributes(self):
        contexts = self.search(filter=self.entity)
        return contexts

    def searchAttribute(self, label, **kwargs):
        key = kwargs.get("key") or label
        object_typeid = kwargs.get("object_typeid") or None
        filter = "%s where label='%s' and key='%s'" % (
            self.entity,
            label,
            key,
        )
        if object_typeid:
            filter += " and object_type_id='%s'" % object_typeid
        contexts = self.search(filter=filter)
        return contexts.first()

    def hasAttribute(self, label, **kwargs):
        context = self.searchAttribute(label, **kwargs)
        if context:
            return True
        return False

    def searchObjectTypes(self):
        contexts = self.search(filter=self.objectTypeEntity)
        return contexts

    def searchObjectTypeByName(self, name):
        filter = '%s where name = "%s"' % (
            self.objectTypeEntity,
            name,
        )
        contexts = self.search(filter=filter)
        return contexts.first()

    def searchAttributeTypes(self):
        contexts = self.search(filter=self.typeEntity)
        return contexts

    def searchAttributeTypeByName(self, name):
        filter = '%s where name = "%s"' % (self.typeEntity, name)
        contexts = self.search(filter=filter)
        return contexts.first()

    def createAttribute(self, **kwargs):
        replace = kwargs.get("replace") or False
        if "replace" in kwargs:
            kwargs.pop("replace")

        print("\n")
        LOGGER.info(
            "%s - %s"
            % (kwargs["object_type"]["name"], kwargs["label"])
        )

        context = self.searchAttribute(
            kwargs["label"],
            key=kwargs["key"],
            object_typeid=kwargs["object_type"]["id"],
        )

        if replace and context:
            self.remove(context)
            # self.session.delete(context)
            LOGGER.warning(
                "removed, already exists <%s> custom attribute in the <%s>"
                % (kwargs["key"], kwargs["object_type"]["name"])
            )

        if not context:
            # Create a custom attribute configuration.
            context = self.session.create(
                "CustomAttributeConfiguration", kwargs
            )
            message = "created new custom attribute"
        else:
            context = self.updateParameters(context)
            message = "updated exists custom attribute"

        LOGGER.info(
            "%s <%s> in the <%s>"
            % (message, kwargs["key"], kwargs["object_type"]["name"])
        )

        # Persist it to the ftrack instance.
        self.session.commit()
        return context

    def updateParameters(self, context):
        result = dict()
        for each in self.editableParameters:
            if not context.get(each):
                continue
            result[each] = context[each]
        return result

    @property
    def editableParameters(self):
        parameters = [
            "write_security_roles",
            "read_security_roles",
            "config",
            "default",
            "group",
            "key",
            "label",
            "object_type",
        ]
        return parameters

    def createProjectAttributes(self):
        for each in self.attributes_input.get():
            each.pop("order"), each.pop("enable")
            attributretype = self.searchAttributeTypeByName(
                each.get("type")
            )
            if not attributretype:
                LOGGER.warning(
                    "invalid attribute type <%s>" % each["type"]
                )
                continue
            each["type"] = attributretype

            object_type = self.searchObjectTypeByName(
                each.get("object_type")
            )
            if not object_type:
                LOGGER.warning(
                    "invalid attribute object type <%s>"
                    % each["object_type"]
                )
                continue
            each["object_type"] = object_type

            if each.get("project_id"):
                each["project_id"] = os.getenv(each["project_id"])

            read_security_roles = self.searchSecurityRoleByNames(
                each.get("read_security_roles")
            )

            if read_security_roles:
                each["read_security_roles"] = read_security_roles
            write_security_roles = self.searchSecurityRoleByNames(
                each.get("write_security_roles")
            )

            if write_security_roles:
                each["write_security_roles"] = write_security_roles

            if each.get("config"):
                each["config"] = json.dumps(each["config"])
            self.createAttribute(**each)

        print("\n")
        LOGGER.info("created studio-pipe custom attributes")


if __name__ == "__main__":
    os.environ["PROJECT-ID"] = "ad54bf94-ba83-41d3-899d-9ed3dc1ab699"
    os.environ["PROJECT-PATH"] = "Z:/projects/RAR"
    os.environ["PIPE-VERSION"] = "0.0.1"

    con = Connect()
    con.authorization()

    con.createProjectAttributes()

# =================================================================
# inputs = {
#     "label": "taskTemplate",
#     "key": "taskTemplate",
#     "default": "subin",
#     "type": "text",
#     "entity_type": "task",
#     "object_type": "Asset Build",
#     "is_hierarchical": False,
#     "project_id": "57cfc315-c96d-4031-89f6-110ad66c0cbd",
#     'config': {'markdown': False}
#     }
#
# object_type = con.searchObjectTypeByName("Asset Build")
# type = con.searchAttributeTypeByName("text")
#
# inputs["object_type"] = object_type
# inputs["type"] = type
#
# pprint (inputs)
#
# con.session.create(
#         "CustomAttributeConfiguration",
#         inputs
#     )
#     # Persist it to the ftrack instance.
# con.session.commit()
#
# =================================================================

# =================================================================
# contexts = con.searchAttributes()
#
# for context in contexts:
#     if context["label"] == "Frame end":
#         con.verbose(context)
#         # con.session.delete(context)
#         # con.verbose(context)
#         #con.verbose(context["type"])
# =================================================================

# =================================================================
# if contexts:
#     con.verbose(contexts)
# =================================================================

# =================================================================
# for context in contexts:
#     if context["label"] == "enable":
#         con.verbose(context)
# =================================================================


# =====================================================================
#                            sort : 4
#                            core : True
#                        group_id : None
#                           group : None
#                             key : handles
#                         type_id : 92009b00-381c-11e0-acff-0019bb49847a
#                         default : 0.0
#                            type : <CustomAttributeType(92009b00-381c-11e0-acff-0019bb49847a)>
#                     object_type : <ObjectType(bad911de-3bd6-47b9-8b46-3476e237cb36)>
#                           label : Frame handles
#             read_security_roles : <ftrack_api.collection.Collection object at 0x000001DAD55FE548>
#                     entity_type : task
#                          values : <ftrack_api.collection.Collection object at 0x000001DAD57630C8>
#                  object_type_id : bad911de-3bd6-47b9-8b46-3476e237cb36
#            write_security_roles : <ftrack_api.collection.Collection object at 0x000001DAD4FEF148>
#                 is_hierarchical : False
#                      project_id : None
#                          config : {"isdecimal": true}
#                              id : 432bdfa6-4087-11e2-8250-0019bb4983d8
#
#
#
#
#                     form_config : {"xtype" : "numberfield"}
#                            core : True
#                              id : 92009b00-381c-11e0-acff-0019bb49847a
#                            name : number
# custom_attribute_configurations : <ftrack_api.collection.Collection object at 0x000001DAD5615A08>
# =====================================================================


# =====================================================================
#                 sort : 0
#                 core : False
#             group_id : None
#                group : None
#                  key : enable
#              type_id : ad1034d8-15e2-11e1-b21a-0019bb4983d8
#              default : True
#                 type : <CustomAttributeType(ad1034d8-15e2-11e1-b21a-0019bb4983d8)>
#          object_type : <ObjectType(4be63b64-5010-42fb-bf1f-428af9d638f0)>
#                label : enable
#  read_security_roles : <ftrack_api.collection.Collection object at 0x0000018339EB4348>
#          entity_type : task
#               values : <ftrack_api.collection.Collection object at 0x0000018339ED7488>
#       object_type_id : 4be63b64-5010-42fb-bf1f-428af9d638f0
# write_security_roles : <ftrack_api.collection.Collection object at 0x000001833A093A08>
#      is_hierarchical : False
#           project_id : None
#               config :
#                   id : 426c60e2-9648-11ec-8c5a-cafb5f2d2887
# =====================================================================


# con.createProjectCustomAttributes()

# context = con.searchCustomAttributeByLabel("sceneAssembly")
# contexts = con.searchCustomAttributes()

# for context in contexts:

#    print(context["label"])
# con.verbose(context)

# print (context["read_security_roles"])
# print (context["write_security_roles"])

# each = con.searchSecurityRoles()

# for e in each:
#    print (e)


# =====================================================================
#     for each in context["write_security_roles"]:
#         for a in each["user_security_roles"]:
#             con.verbose(a)
#
#     each = con.searchSecurityRoleByName(name="API")
#     for a in each["user_security_roles"]:
#         con.verbose(a)
# =====================================================================

# =================================================================
# write_roles = [each for each in con.searchWriteSecurityRoles()]
#
# read_roles = [each for each in con.searchReadSecurityRoles()]
#
#
# securityRoles = con.searchSecurityRoles()
#
# typed = con.searchCustomAttributeTypeByName("boolean")
# object_type = con.searchObjectTypeByName("Asset Build")
#
#
# abc = {
#         "core": False,
#         "label": "enable",
#         "key": "enable12",
#         "default": True,
#         "type": typed,
#         "entity_type": "task",
#         "object_type": object_type,
#         # "object_type_id": object_type["id"],
#
#         "is_hierarchical": False,
#         "project_id": "57cfc315-c96d-4031-89f6-110ad66c0cbd",
#         "read_security_roles": read_roles,
#         "write_security_roles": write_roles
#
#     }
#
# con.session.create(
#     "CustomAttributeConfiguration",
#     abc
# )
# # Persist it to the ftrack instance.
# con.session.commit()
#
# print ("done!...")
# =================================================================

# context = con.update("AssetBuild", "849f0e3c-316c-4f2a-9630-b6f59033a0e7")
# print (context.entity_type)


# =================================================================
# con.createCustomAttribute(
#     "task", "boolean", "ptest", True
#     )
# =================================================================

# =================================================================
# context = con.searchCustomAttributeTypes()
# for each in context:
#     print (each["name"])
#     # con.verbose(each)
# =================================================================

# =================================================================
# context = con.searchCustomAttributes()
#
# for each in context:
#     if each["label"] == "subin":
#         con.verbose(each)
#         con.verbose (each["object_type"])
#         # print (each["default"])
#
#         print (each["object_type"].entity_type)
#
#
# context = con.searchObjectTypes()
# for each in context:
#     # if each["label"] == "subin":
#     print (each["name"])
# =================================================================


# =====================================================================
# text
# enumerator
# date
# dynamic enumerator
# number
# notificationtype
# boolean
# expression
# =====================================================================

# =====================================================================
#                 sort : 0
#                 core : False
#             group_id : None
#                group : None
#                  key : enable
#              type_id : ad1034d8-15e2-11e1-b21a-0019bb4983d8
#              default : True
#                 type : <CustomAttributeType(ad1034d8-15e2-11e1-b21a-0019bb4983d8)>
#          object_type : <ObjectType(4be63b64-5010-42fb-bf1f-428af9d638f0)>
#                label : enable
#  read_security_roles : <ftrack_api.collection.Collection object at 0x000001F294FD4248>
#          entity_type : task
#               values : <ftrack_api.collection.Collection object at 0x000001F29512EF08>
#       object_type_id : 4be63b64-5010-42fb-bf1f-428af9d638f0
# write_security_roles : <ftrack_api.collection.Collection object at 0x000001F294FD4BC8>
#      is_hierarchical : False
#           project_id : None
#               config :
#                   id : dd4bae26-924a-11ec-b9bd-6e863b29c9f5
# =====================================================================


# print (each["label"], each["type"])
