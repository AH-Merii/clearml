"""
models service

This service provides a management interface for models (results of training tasks) stored in the system.
"""
from typing import List, Optional, Union, Any
import six
from datetime import datetime
from dateutil.parser import parse as parse_datetime
from clearml.backend_api.session import (
    Request,
    Response,
    NonStrictDataModel,
    schema_property,
)


class MultiFieldPatternData(NonStrictDataModel):
    """
    :param pattern: Pattern string (regex)
    :type pattern: str
    :param fields: List of field names
    :type fields: Sequence[str]
    """

    _schema = {
        "properties": {
            "fields": {
                "description": "List of field names",
                "items": {"type": "string"},
                "type": ["array", "null"],
            },
            "pattern": {
                "description": "Pattern string (regex)",
                "type": ["string", "null"],
            },
        },
        "type": "object",
    }

    def __init__(self, pattern: Optional[str] = None, fields: Optional[List[str]] = None, **kwargs: Any) -> None:
        super(MultiFieldPatternData, self).__init__(**kwargs)
        self.pattern = pattern
        self.fields = fields

    @schema_property("pattern")
    def pattern(self) -> Optional[str]:
        return self._property_pattern

    @pattern.setter
    def pattern(self, value: Optional[str]) -> None:
        if value is None:
            self._property_pattern = None
            return
        self.assert_isinstance(value, "pattern", six.string_types)
        self._property_pattern = value

    @schema_property("fields")
    def fields(self) -> Optional[List[str]]:
        return self._property_fields

    @fields.setter
    def fields(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_fields = None
            return
        self.assert_isinstance(value, "fields", (list, tuple))
        self.assert_isinstance(value, "fields", six.string_types, is_array=True)
        self._property_fields = value


class MetadataItem(NonStrictDataModel):
    """
    :param key: The key uniquely identifying the metadata item inside the given
        entity
    :type key: str
    :param type: The type of the metadata item
    :type type: str
    :param value: The value stored in the metadata item
    :type value: str
    """

    _schema = {
        "properties": {
            "key": {
                "description": "The key uniquely identifying the metadata item inside the given entity",
                "type": ["string", "null"],
            },
            "type": {
                "description": "The type of the metadata item",
                "type": ["string", "null"],
            },
            "value": {
                "description": "The value stored in the metadata item",
                "type": ["string", "null"],
            },
        },
        "type": "object",
    }

    def __init__(
        self, key: Optional[str] = None, type: Optional[str] = None, value: Optional[str] = None, **kwargs: Any
    ) -> None:
        super(MetadataItem, self).__init__(**kwargs)
        self.key = key
        self.type = type
        self.value = value

    @schema_property("key")
    def key(self) -> Optional[str]:
        return self._property_key

    @key.setter
    def key(self, value: Optional[str]) -> None:
        if value is None:
            self._property_key = None
            return
        self.assert_isinstance(value, "key", six.string_types)
        self._property_key = value

    @schema_property("type")
    def type(self) -> Optional[str]:
        return self._property_type

    @type.setter
    def type(self, value: Optional[str]) -> None:
        if value is None:
            self._property_type = None
            return
        self.assert_isinstance(value, "type", six.string_types)
        self._property_type = value

    @schema_property("value")
    def value(self) -> Optional[str]:
        return self._property_value

    @value.setter
    def value(self, value: Optional[str]) -> None:
        if value is None:
            self._property_value = None
            return
        self.assert_isinstance(value, "value", six.string_types)
        self._property_value = value


class Model(NonStrictDataModel):
    """
    :param id: Model id
    :type id: str
    :param name: Model name
    :type name: str
    :param user: Associated user id
    :type user: str
    :param company: Company id
    :type company: str
    :param created: Model creation time
    :type created: datetime.datetime
    :param last_update: Model last update time
    :type last_update: datetime.datetime
    :param task: Task ID of task in which the model was created
    :type task: str
    :param parent: Parent model ID
    :type parent: str
    :param project: Associated project ID
    :type project: str
    :param comment: Model comment
    :type comment: str
    :param tags: User-defined tags
    :type tags: Sequence[str]
    :param system_tags: System tags. This field is reserved for system use, please
        don't use it.
    :type system_tags: Sequence[str]
    :param framework: Framework on which the model is based. Should be identical to
        the framework of the task which created the model
    :type framework: str
    :param design: Json object representing the model design. Should be identical
        to the network design of the task which created the model
    :type design: dict
    :param labels: Json object representing the ids of the labels in the model. The
        keys are the layers' names and the values are the ids.
    :type labels: dict
    :param uri: URI for the model, pointing to the destination storage.
    :type uri: str
    :param ready: Indication if the model is final and can be used by other tasks
    :type ready: bool
    :param ui_cache: UI cache for this model
    :type ui_cache: dict
    :param metadata: Model metadata
    :type metadata: dict
    :param stats: Model statistics
    :type stats: dict
    """

    _schema = {
        "properties": {
            "comment": {"description": "Model comment", "type": ["string", "null"]},
            "company": {"description": "Company id", "type": ["string", "null"]},
            "created": {
                "description": "Model creation time",
                "format": "date-time",
                "type": ["string", "null"],
            },
            "design": {
                "additionalProperties": True,
                "description": "Json object representing the model design. Should be identical to the network design of the task which created the model",
                "type": ["object", "null"],
            },
            "framework": {
                "description": "Framework on which the model is based. Should be identical to the framework of the task which created the model",
                "type": ["string", "null"],
            },
            "id": {"description": "Model id", "type": ["string", "null"]},
            "labels": {
                "additionalProperties": {"type": "integer"},
                "description": "Json object representing the ids of the labels in the model. The keys are the layers' names and the values are the ids.",
                "type": ["object", "null"],
            },
            "last_update": {
                "description": "Model last update time",
                "format": "date-time",
                "type": ["string", "null"],
            },
            "metadata": {
                "additionalProperties": {"$ref": "#/definitions/metadata_item"},
                "description": "Model metadata",
                "type": ["object", "null"],
            },
            "name": {"description": "Model name", "type": ["string", "null"]},
            "parent": {"description": "Parent model ID", "type": ["string", "null"]},
            "project": {
                "description": "Associated project ID",
                "type": ["string", "null"],
            },
            "ready": {
                "description": "Indication if the model is final and can be used by other tasks",
                "type": ["boolean", "null"],
            },
            "stats": {
                "description": "Model statistics",
                "properties": {
                    "labels_count": {
                        "description": "Number of the model labels",
                        "type": "integer",
                    }
                },
                "type": ["object", "null"],
            },
            "system_tags": {
                "description": "System tags. This field is reserved for system use, please don't use it.",
                "items": {"type": "string"},
                "type": ["array", "null"],
            },
            "tags": {
                "description": "User-defined tags",
                "items": {"type": "string"},
                "type": ["array", "null"],
            },
            "task": {
                "description": "Task ID of task in which the model was created",
                "type": ["string", "null"],
            },
            "ui_cache": {
                "additionalProperties": True,
                "description": "UI cache for this model",
                "type": ["object", "null"],
            },
            "uri": {
                "description": "URI for the model, pointing to the destination storage.",
                "type": ["string", "null"],
            },
            "user": {"description": "Associated user id", "type": ["string", "null"]},
        },
        "type": "object",
    }

    def __init__(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
        user: Optional[str] = None,
        company: Optional[str] = None,
        created: Optional[str] = None,
        last_update: Optional[str] = None,
        task: Optional[str] = None,
        parent: Optional[str] = None,
        project: Optional[str] = None,
        comment: Optional[str] = None,
        tags: Optional[List[str]] = None,
        system_tags: Optional[List[str]] = None,
        framework: Optional[str] = None,
        design: Optional[dict] = None,
        labels: Optional[dict] = None,
        uri: Optional[str] = None,
        ready: Optional[bool] = None,
        ui_cache: Optional[dict] = None,
        metadata: Optional[dict] = None,
        stats: Optional[dict] = None,
        **kwargs: Any
    ) -> None:
        super(Model, self).__init__(**kwargs)
        self.id = id
        self.name = name
        self.user = user
        self.company = company
        self.created = created
        self.last_update = last_update
        self.task = task
        self.parent = parent
        self.project = project
        self.comment = comment
        self.tags = tags
        self.system_tags = system_tags
        self.framework = framework
        self.design = design
        self.labels = labels
        self.uri = uri
        self.ready = ready
        self.ui_cache = ui_cache
        self.metadata = metadata
        self.stats = stats

    @schema_property("id")
    def id(self) -> Optional[str]:
        return self._property_id

    @id.setter
    def id(self, value: Optional[str]) -> None:
        if value is None:
            self._property_id = None
            return
        self.assert_isinstance(value, "id", six.string_types)
        self._property_id = value

    @schema_property("name")
    def name(self) -> Optional[str]:
        return self._property_name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        if value is None:
            self._property_name = None
            return
        self.assert_isinstance(value, "name", six.string_types)
        self._property_name = value

    @schema_property("user")
    def user(self) -> Optional[str]:
        return self._property_user

    @user.setter
    def user(self, value: Optional[str]) -> None:
        if value is None:
            self._property_user = None
            return
        self.assert_isinstance(value, "user", six.string_types)
        self._property_user = value

    @schema_property("company")
    def company(self) -> Optional[str]:
        return self._property_company

    @company.setter
    def company(self, value: Optional[str]) -> None:
        if value is None:
            self._property_company = None
            return
        self.assert_isinstance(value, "company", six.string_types)
        self._property_company = value

    @schema_property("created")
    def created(self) -> Optional[str]:
        return self._property_created

    @created.setter
    def created(self, value: Optional[str]) -> None:
        if value is None:
            self._property_created = None
            return
        self.assert_isinstance(value, "created", six.string_types + (datetime,))
        if not isinstance(value, datetime):
            value = parse_datetime(value)
        self._property_created = value

    @schema_property("last_update")
    def last_update(self) -> Optional[str]:
        return self._property_last_update

    @last_update.setter
    def last_update(self, value: Optional[str]) -> None:
        if value is None:
            self._property_last_update = None
            return
        self.assert_isinstance(value, "last_update", six.string_types + (datetime,))
        if not isinstance(value, datetime):
            value = parse_datetime(value)
        self._property_last_update = value

    @schema_property("task")
    def task(self) -> Optional[str]:
        return self._property_task

    @task.setter
    def task(self, value: Optional[str]) -> None:
        if value is None:
            self._property_task = None
            return
        self.assert_isinstance(value, "task", six.string_types)
        self._property_task = value

    @schema_property("parent")
    def parent(self) -> Optional[str]:
        return self._property_parent

    @parent.setter
    def parent(self, value: Optional[str]) -> None:
        if value is None:
            self._property_parent = None
            return
        self.assert_isinstance(value, "parent", six.string_types)
        self._property_parent = value

    @schema_property("project")
    def project(self) -> Optional[str]:
        return self._property_project

    @project.setter
    def project(self, value: Optional[str]) -> None:
        if value is None:
            self._property_project = None
            return
        self.assert_isinstance(value, "project", six.string_types)
        self._property_project = value

    @schema_property("comment")
    def comment(self) -> Optional[str]:
        return self._property_comment

    @comment.setter
    def comment(self, value: Optional[str]) -> None:
        if value is None:
            self._property_comment = None
            return
        self.assert_isinstance(value, "comment", six.string_types)
        self._property_comment = value

    @schema_property("tags")
    def tags(self) -> Optional[List[str]]:
        return self._property_tags

    @tags.setter
    def tags(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_tags = None
            return
        self.assert_isinstance(value, "tags", (list, tuple))
        self.assert_isinstance(value, "tags", six.string_types, is_array=True)
        self._property_tags = value

    @schema_property("system_tags")
    def system_tags(self) -> Optional[List[str]]:
        return self._property_system_tags

    @system_tags.setter
    def system_tags(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_system_tags = None
            return
        self.assert_isinstance(value, "system_tags", (list, tuple))
        self.assert_isinstance(value, "system_tags", six.string_types, is_array=True)
        self._property_system_tags = value

    @schema_property("framework")
    def framework(self) -> Optional[str]:
        return self._property_framework

    @framework.setter
    def framework(self, value: Optional[str]) -> None:
        if value is None:
            self._property_framework = None
            return
        self.assert_isinstance(value, "framework", six.string_types)
        self._property_framework = value

    @schema_property("design")
    def design(self) -> Optional[dict]:
        return self._property_design

    @design.setter
    def design(self, value: Optional[dict]) -> None:
        if value is None:
            self._property_design = None
            return
        self.assert_isinstance(value, "design", (dict,))
        self._property_design = value

    @schema_property("labels")
    def labels(self) -> Optional[dict]:
        return self._property_labels

    @labels.setter
    def labels(self, value: Optional[dict]) -> None:
        if value is None:
            self._property_labels = None
            return
        self.assert_isinstance(value, "labels", (dict,))
        self._property_labels = value

    @schema_property("uri")
    def uri(self) -> Optional[str]:
        return self._property_uri

    @uri.setter
    def uri(self, value: Optional[str]) -> None:
        if value is None:
            self._property_uri = None
            return
        self.assert_isinstance(value, "uri", six.string_types)
        self._property_uri = value

    @schema_property("ready")
    def ready(self) -> Optional[bool]:
        return self._property_ready

    @ready.setter
    def ready(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_ready = None
            return
        self.assert_isinstance(value, "ready", (bool,))
        self._property_ready = value

    @schema_property("ui_cache")
    def ui_cache(self) -> Optional[dict]:
        return self._property_ui_cache

    @ui_cache.setter
    def ui_cache(self, value: Optional[dict]) -> None:
        if value is None:
            self._property_ui_cache = None
            return
        self.assert_isinstance(value, "ui_cache", (dict,))
        self._property_ui_cache = value

    @schema_property("metadata")
    def metadata(self) -> Optional[dict]:
        return self._property_metadata

    @metadata.setter
    def metadata(self, value: Optional[dict]) -> None:
        if value is None:
            self._property_metadata = None
            return
        self.assert_isinstance(value, "metadata", (dict,))
        self._property_metadata = value

    @schema_property("stats")
    def stats(self) -> Optional[dict]:
        return self._property_stats

    @stats.setter
    def stats(self, value: Optional[dict]) -> None:
        if value is None:
            self._property_stats = None
            return
        self.assert_isinstance(value, "stats", (dict,))
        self._property_stats = value


class AddOrUpdateMetadataRequest(Request):
    """
    Add or update model metadata

    :param model: ID of the model
    :type model: str
    :param metadata: Metadata items to add or update
    :type metadata: Sequence[MetadataItem]
    :param replace_metadata: If set then the all the metadata items will be
        replaced with the provided ones. Otherwise only the provided metadata items
        will be updated or added
    :type replace_metadata: bool
    """

    _service = "models"
    _action = "add_or_update_metadata"
    _version = "2.23"
    _schema = {
        "definitions": {
            "metadata_item": {
                "properties": {
                    "key": {
                        "description": "The key uniquely identifying the metadata item inside the given entity",
                        "type": ["string", "null"],
                    },
                    "type": {
                        "description": "The type of the metadata item",
                        "type": ["string", "null"],
                    },
                    "value": {
                        "description": "The value stored in the metadata item",
                        "type": ["string", "null"],
                    },
                },
                "type": "object",
            }
        },
        "properties": {
            "metadata": {
                "description": "Metadata items to add or update",
                "items": {"$ref": "#/definitions/metadata_item"},
                "type": "array",
            },
            "model": {"description": "ID of the model", "type": "string"},
            "replace_metadata": {
                "default": False,
                "description": "If set then the all the metadata items will be replaced with the provided ones. Otherwise only the provided metadata items will be updated or added",
                "type": "boolean",
            },
        },
        "required": ["model", "metadata"],
        "type": "object",
    }

    def __init__(
        self, model: str, metadata: List[Any], replace_metadata: Optional[bool] = False, **kwargs: Any
    ) -> None:
        super(AddOrUpdateMetadataRequest, self).__init__(**kwargs)
        self.model = model
        self.metadata = metadata
        self.replace_metadata = replace_metadata

    @schema_property("model")
    def model(self) -> str:
        return self._property_model

    @model.setter
    def model(self, value: str) -> None:
        if value is None:
            self._property_model = None
            return
        self.assert_isinstance(value, "model", six.string_types)
        self._property_model = value

    @schema_property("metadata")
    def metadata(self) -> List[Any]:
        return self._property_metadata

    @metadata.setter
    def metadata(self, value: List[Any]) -> None:
        if value is None:
            self._property_metadata = None
            return
        self.assert_isinstance(value, "metadata", (list, tuple))
        if any((isinstance(v, dict) for v in value)):
            value = [MetadataItem.from_dict(v) if isinstance(v, dict) else v for v in value]
        else:
            self.assert_isinstance(value, "metadata", MetadataItem, is_array=True)
        self._property_metadata = value

    @schema_property("replace_metadata")
    def replace_metadata(self) -> Optional[bool]:
        return self._property_replace_metadata

    @replace_metadata.setter
    def replace_metadata(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_replace_metadata = None
            return
        self.assert_isinstance(value, "replace_metadata", (bool,))
        self._property_replace_metadata = value


class AddOrUpdateMetadataResponse(Response):
    """
    Response of models.add_or_update_metadata endpoint.

    :param updated: Number of models updated (0 or 1)
    :type updated: int
    """

    _service = "models"
    _action = "add_or_update_metadata"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "updated": {
                "description": "Number of models updated (0 or 1)",
                "enum": [0, 1],
                "type": ["integer", "null"],
            }
        },
        "type": "object",
    }

    def __init__(self, updated: Optional[int] = None, **kwargs: Any) -> None:
        super(AddOrUpdateMetadataResponse, self).__init__(**kwargs)
        self.updated = updated

    @schema_property("updated")
    def updated(self) -> Optional[int]:
        return self._property_updated

    @updated.setter
    def updated(self, value: Optional[int]) -> None:
        if value is None:
            self._property_updated = None
            return
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        self.assert_isinstance(value, "updated", six.integer_types)
        self._property_updated = value


class ArchiveManyRequest(Request):
    """
    Archive models

    :param ids: IDs of the models to archive
    :type ids: Sequence[str]
    """

    _service = "models"
    _action = "archive_many"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "ids": {
                "description": "IDs of the models to archive",
                "items": {"type": "string"},
                "type": "array",
            }
        },
        "required": ["ids"],
        "type": "object",
    }

    def __init__(self, ids: List[str], **kwargs: Any) -> None:
        super(ArchiveManyRequest, self).__init__(**kwargs)
        self.ids = ids

    @schema_property("ids")
    def ids(self) -> List[str]:
        return self._property_ids

    @ids.setter
    def ids(self, value: List[str]) -> None:
        if value is None:
            self._property_ids = None
            return
        self.assert_isinstance(value, "ids", (list, tuple))
        self.assert_isinstance(value, "ids", six.string_types, is_array=True)
        self._property_ids = value


class ArchiveManyResponse(Response):
    """
    Response of models.archive_many endpoint.

    :param succeeded:
    :type succeeded: Sequence[dict]
    :param failed:
    :type failed: Sequence[dict]
    """

    _service = "models"
    _action = "archive_many"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "failed": {
                "items": {
                    "properties": {
                        "error": {
                            "description": "Error info",
                            "properties": {
                                "codes": {
                                    "items": {"type": "integer"},
                                    "type": "array",
                                },
                                "data": {
                                    "additionalProperties": True,
                                    "type": "object",
                                },
                                "msg": {"type": "string"},
                            },
                            "type": "object",
                        },
                        "id": {
                            "description": "ID of the failed entity",
                            "type": "string",
                        },
                    },
                    "type": "object",
                },
                "type": ["array", "null"],
            },
            "succeeded": {
                "items": {
                    "properties": {
                        "archived": {
                            "description": "Indicates whether the model was archived",
                            "type": "boolean",
                        },
                        "id": {
                            "description": "ID of the succeeded entity",
                            "type": "string",
                        },
                    },
                    "type": "object",
                },
                "type": ["array", "null"],
            },
        },
        "type": "object",
    }

    def __init__(
        self, succeeded: Optional[List[dict]] = None, failed: Optional[List[dict]] = None, **kwargs: Any
    ) -> None:
        super(ArchiveManyResponse, self).__init__(**kwargs)
        self.succeeded = succeeded
        self.failed = failed

    @schema_property("succeeded")
    def succeeded(self) -> Optional[List[dict]]:
        return self._property_succeeded

    @succeeded.setter
    def succeeded(self, value: Optional[List[dict]]) -> None:
        if value is None:
            self._property_succeeded = None
            return
        self.assert_isinstance(value, "succeeded", (list, tuple))
        self.assert_isinstance(value, "succeeded", (dict,), is_array=True)
        self._property_succeeded = value

    @schema_property("failed")
    def failed(self) -> Optional[List[dict]]:
        return self._property_failed

    @failed.setter
    def failed(self, value: Optional[List[dict]]) -> None:
        if value is None:
            self._property_failed = None
            return
        self.assert_isinstance(value, "failed", (list, tuple))
        self.assert_isinstance(value, "failed", (dict,), is_array=True)
        self._property_failed = value


class CreateRequest(Request):
    """
    Create a new model not associated with a task

    :param uri: URI for the model
    :type uri: str
    :param name: Model name Unique within the company.
    :type name: str
    :param comment: Model comment
    :type comment: str
    :param tags: User-defined tags list
    :type tags: Sequence[str]
    :param system_tags: System tags list. This field is reserved for system use,
        please don't use it.
    :type system_tags: Sequence[str]
    :param framework: Framework on which the model is based. Case insensitive.
        Should be identical to the framework of the task which created the model.
    :type framework: str
    :param design: Json[d] object representing the model design. Should be
        identical to the network design of the task which created the model
    :type design: dict
    :param labels: Json object
    :type labels: dict
    :param ready: Indication if the model is final and can be used by other tasks.
        Default is false.
    :type ready: bool
    :param public: Create a public model Default is false.
    :type public: bool
    :param project: Project to which to model belongs
    :type project: str
    :param parent: Parent model
    :type parent: str
    :param task: Associated task ID
    :type task: str
    """

    _service = "models"
    _action = "create"
    _version = "2.23"
    _schema = {
        "definitions": {
            "metadata_item": {
                "properties": {
                    "key": {
                        "description": "The key uniquely identifying the metadata item inside the given entity",
                        "type": "string",
                    },
                    "type": {
                        "description": "The type of the metadata item",
                        "type": "string",
                    },
                    "value": {
                        "description": "The value stored in the metadata item",
                        "type": "string",
                    },
                },
                "type": "object",
            }
        },
        "properties": {
            "comment": {"description": "Model comment", "type": "string"},
            "design": {
                "additionalProperties": True,
                "description": "Json[d] object representing the model design. Should be identical to the network design of the task which created the model",
                "type": "object",
            },
            "framework": {
                "description": "Framework on which the model is based. Case insensitive. Should be identical to the framework of the task which created the model.",
                "type": "string",
            },
            "labels": {
                "additionalProperties": {"type": "integer"},
                "description": "Json object",
                "type": "object",
            },
            "name": {
                "description": "Model name Unique within the company.",
                "type": "string",
            },
            "parent": {"description": "Parent model", "type": "string"},
            "project": {
                "description": "Project to which to model belongs",
                "type": "string",
            },
            "public": {
                "default": False,
                "description": "Create a public model Default is false.",
                "type": "boolean",
            },
            "ready": {
                "default": False,
                "description": "Indication if the model is final and can be used by other tasks. Default is false.",
                "type": "boolean",
            },
            "system_tags": {
                "description": "System tags list. This field is reserved for system use, please don't use it.",
                "items": {"type": "string"},
                "type": "array",
            },
            "tags": {
                "description": "User-defined tags list",
                "items": {"type": "string"},
                "type": "array",
            },
            "task": {"description": "Associated task ID", "type": "string"},
            "uri": {"description": "URI for the model", "type": "string"},
            "metadata": {
                "type": "array",
                "items": {"$ref": "#/definitions/metadata_item"},
                "description": "Model metadata",
            },
        },
        "required": ["uri", "name"],
        "type": "object",
    }

    def __init__(
        self,
        uri: str,
        name: str,
        comment: Optional[str] = None,
        tags: Optional[List[str]] = None,
        system_tags: Optional[List[str]] = None,
        framework: Optional[str] = None,
        design: Optional[dict] = None,
        labels: Optional[dict] = None,
        ready: Optional[bool] = False,
        public: Optional[bool] = False,
        project: Optional[str] = None,
        parent: Optional[str] = None,
        task: Optional[str] = None,
        metadata: Optional[List[Any]] = None,
        **kwargs: Any
    ) -> None:
        super(CreateRequest, self).__init__(**kwargs)
        self.uri = uri
        self.name = name
        self.comment = comment
        self.tags = tags
        self.system_tags = system_tags
        self.framework = framework
        self.design = design
        self.labels = labels
        self.ready = ready
        self.public = public
        self.project = project
        self.parent = parent
        self.task = task
        self.metadata = metadata

    @schema_property("uri")
    def uri(self) -> str:
        return self._property_uri

    @uri.setter
    def uri(self, value: str) -> None:
        if value is None:
            self._property_uri = None
            return
        self.assert_isinstance(value, "uri", six.string_types)
        self._property_uri = value

    @schema_property("name")
    def name(self) -> str:
        return self._property_name

    @name.setter
    def name(self, value: str) -> None:
        if value is None:
            self._property_name = None
            return
        self.assert_isinstance(value, "name", six.string_types)
        self._property_name = value

    @schema_property("comment")
    def comment(self) -> Optional[str]:
        return self._property_comment

    @comment.setter
    def comment(self, value: Optional[str]) -> None:
        if value is None:
            self._property_comment = None
            return
        self.assert_isinstance(value, "comment", six.string_types)
        self._property_comment = value

    @schema_property("tags")
    def tags(self) -> Optional[List[str]]:
        return self._property_tags

    @tags.setter
    def tags(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_tags = None
            return
        self.assert_isinstance(value, "tags", (list, tuple))
        self.assert_isinstance(value, "tags", six.string_types, is_array=True)
        self._property_tags = value

    @schema_property("system_tags")
    def system_tags(self) -> Optional[List[str]]:
        return self._property_system_tags

    @system_tags.setter
    def system_tags(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_system_tags = None
            return
        self.assert_isinstance(value, "system_tags", (list, tuple))
        self.assert_isinstance(value, "system_tags", six.string_types, is_array=True)
        self._property_system_tags = value

    @schema_property("framework")
    def framework(self) -> Optional[str]:
        return self._property_framework

    @framework.setter
    def framework(self, value: Optional[str]) -> None:
        if value is None:
            self._property_framework = None
            return
        self.assert_isinstance(value, "framework", six.string_types)
        self._property_framework = value

    @schema_property("design")
    def design(self) -> Optional[dict]:
        return self._property_design

    @design.setter
    def design(self, value: Optional[dict]) -> None:
        if value is None:
            self._property_design = None
            return
        self.assert_isinstance(value, "design", (dict,))
        self._property_design = value

    @schema_property("labels")
    def labels(self) -> Optional[dict]:
        return self._property_labels

    @labels.setter
    def labels(self, value: Optional[dict]) -> None:
        if value is None:
            self._property_labels = None
            return
        self.assert_isinstance(value, "labels", (dict,))
        self._property_labels = value

    @schema_property("ready")
    def ready(self) -> Optional[bool]:
        return self._property_ready

    @ready.setter
    def ready(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_ready = None
            return
        self.assert_isinstance(value, "ready", (bool,))
        self._property_ready = value

    @schema_property("public")
    def public(self) -> Optional[bool]:
        return self._property_public

    @public.setter
    def public(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_public = None
            return
        self.assert_isinstance(value, "public", (bool,))
        self._property_public = value

    @schema_property("project")
    def project(self) -> Optional[str]:
        return self._property_project

    @project.setter
    def project(self, value: Optional[str]) -> None:
        if value is None:
            self._property_project = None
            return
        self.assert_isinstance(value, "project", six.string_types)
        self._property_project = value

    @schema_property("parent")
    def parent(self) -> Optional[str]:
        return self._property_parent

    @parent.setter
    def parent(self, value: Optional[str]) -> None:
        if value is None:
            self._property_parent = None
            return
        self.assert_isinstance(value, "parent", six.string_types)
        self._property_parent = value

    @schema_property("task")
    def task(self) -> Optional[str]:
        return self._property_task

    @task.setter
    def task(self, value: Optional[str]) -> None:
        if value is None:
            self._property_task = None
            return
        self.assert_isinstance(value, "task", six.string_types)
        self._property_task = value

    @schema_property("metadata")
    def metadata(self) -> Optional[List[Any]]:
        return self._property_metadata

    @metadata.setter
    def metadata(self, value: Optional[List[Any]]) -> None:
        if value is None:
            self._property_metadata = None
            return
        self.assert_isinstance(value, "metadata", (list, tuple))
        if any((isinstance(v, dict) for v in value)):
            value = [MetadataItem.from_dict(v) if isinstance(v, dict) else v for v in value]
        else:
            self.assert_isinstance(value, "metadata", MetadataItem, is_array=True)
        self._property_metadata = value


class CreateResponse(Response):
    """
    Response of models.create endpoint.

    :param id: ID of the model
    :type id: str
    :param created: Was the model created
    :type created: bool
    """

    _service = "models"
    _action = "create"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "created": {
                "description": "Was the model created",
                "type": ["boolean", "null"],
            },
            "id": {"description": "ID of the model", "type": ["string", "null"]},
        },
        "type": "object",
    }

    def __init__(self, id: Optional[str] = None, created: Optional[bool] = None, **kwargs: Any) -> None:
        super(CreateResponse, self).__init__(**kwargs)
        self.id = id
        self.created = created

    @schema_property("id")
    def id(self) -> Optional[str]:
        return self._property_id

    @id.setter
    def id(self, value: Optional[str]) -> None:
        if value is None:
            self._property_id = None
            return
        self.assert_isinstance(value, "id", six.string_types)
        self._property_id = value

    @schema_property("created")
    def created(self) -> Optional[bool]:
        return self._property_created

    @created.setter
    def created(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_created = None
            return
        self.assert_isinstance(value, "created", (bool,))
        self._property_created = value


class DeleteRequest(Request):
    """
    Delete a model.

    :param model: Model ID
    :type model: str
    :param force: Force. Required if there are tasks that use the model as an
        execution model, or if the model's creating task is published.
    :type force: bool
    """

    _service = "models"
    _action = "delete"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "force": {
                "description": "Force. Required if there are tasks that use the model as an execution model, or if the model's creating task is published.\n                    ",
                "type": "boolean",
            },
            "model": {"description": "Model ID", "type": "string"},
        },
        "required": ["model"],
        "type": "object",
    }

    def __init__(self, model: str, force: Optional[bool] = None, **kwargs: Any) -> None:
        super(DeleteRequest, self).__init__(**kwargs)
        self.model = model
        self.force = force

    @schema_property("model")
    def model(self) -> str:
        return self._property_model

    @model.setter
    def model(self, value: str) -> None:
        if value is None:
            self._property_model = None
            return
        self.assert_isinstance(value, "model", six.string_types)
        self._property_model = value

    @schema_property("force")
    def force(self) -> Optional[bool]:
        return self._property_force

    @force.setter
    def force(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_force = None
            return
        self.assert_isinstance(value, "force", (bool,))
        self._property_force = value


class DeleteResponse(Response):
    """
    Response of models.delete endpoint.

    :param deleted: Indicates whether the model was deleted
    :type deleted: bool
    :param url: The url of the model file
    :type url: str
    """

    _service = "models"
    _action = "delete"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "deleted": {
                "description": "Indicates whether the model was deleted",
                "type": ["boolean", "null"],
            },
            "url": {
                "description": "The url of the model file",
                "type": ["string", "null"],
            },
        },
        "type": "object",
    }

    def __init__(self, deleted: Optional[bool] = None, url: Optional[str] = None, **kwargs: Any) -> None:
        super(DeleteResponse, self).__init__(**kwargs)
        self.deleted = deleted
        self.url = url

    @schema_property("deleted")
    def deleted(self) -> Optional[bool]:
        return self._property_deleted

    @deleted.setter
    def deleted(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_deleted = None
            return
        self.assert_isinstance(value, "deleted", (bool,))
        self._property_deleted = value

    @schema_property("url")
    def url(self) -> Optional[str]:
        return self._property_url

    @url.setter
    def url(self, value: Optional[str]) -> None:
        if value is None:
            self._property_url = None
            return
        self.assert_isinstance(value, "url", six.string_types)
        self._property_url = value


class DeleteManyRequest(Request):
    """
    Delete models

    :param ids: IDs of the models to delete
    :type ids: Sequence[str]
    :param force: Force. Required if there are tasks that use the model as an
        execution model, or if the model's creating task is published.
    :type force: bool
    """

    _service = "models"
    _action = "delete_many"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "force": {
                "description": "Force. Required if there are tasks that use the model as an execution model, or if the model's creating task is published.",
                "type": "boolean",
            },
            "ids": {
                "description": "IDs of the models to delete",
                "items": {"type": "string"},
                "type": "array",
            },
        },
        "required": ["ids"],
        "type": "object",
    }

    def __init__(self, ids: List[str], force: Optional[bool] = None, **kwargs: Any) -> None:
        super(DeleteManyRequest, self).__init__(**kwargs)
        self.ids = ids
        self.force = force

    @schema_property("ids")
    def ids(self) -> List[str]:
        return self._property_ids

    @ids.setter
    def ids(self, value: List[str]) -> None:
        if value is None:
            self._property_ids = None
            return
        self.assert_isinstance(value, "ids", (list, tuple))
        self.assert_isinstance(value, "ids", six.string_types, is_array=True)
        self._property_ids = value

    @schema_property("force")
    def force(self) -> Optional[bool]:
        return self._property_force

    @force.setter
    def force(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_force = None
            return
        self.assert_isinstance(value, "force", (bool,))
        self._property_force = value


class DeleteManyResponse(Response):
    """
    Response of models.delete_many endpoint.

    :param succeeded:
    :type succeeded: Sequence[dict]
    :param failed:
    :type failed: Sequence[dict]
    """

    _service = "models"
    _action = "delete_many"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "failed": {
                "items": {
                    "properties": {
                        "error": {
                            "description": "Error info",
                            "properties": {
                                "codes": {
                                    "items": {"type": "integer"},
                                    "type": "array",
                                },
                                "data": {
                                    "additionalProperties": True,
                                    "type": "object",
                                },
                                "msg": {"type": "string"},
                            },
                            "type": "object",
                        },
                        "id": {
                            "description": "ID of the failed entity",
                            "type": "string",
                        },
                    },
                    "type": "object",
                },
                "type": ["array", "null"],
            },
            "succeeded": {
                "items": {
                    "properties": {
                        "deleted": {
                            "description": "Indicates whether the model was deleted",
                            "type": "boolean",
                        },
                        "id": {
                            "description": "ID of the succeeded entity",
                            "type": "string",
                        },
                        "url": {
                            "description": "The url of the model file",
                            "type": "string",
                        },
                    },
                    "type": "object",
                },
                "type": ["array", "null"],
            },
        },
        "type": "object",
    }

    def __init__(
        self, succeeded: Optional[List[dict]] = None, failed: Optional[List[dict]] = None, **kwargs: Any
    ) -> None:
        super(DeleteManyResponse, self).__init__(**kwargs)
        self.succeeded = succeeded
        self.failed = failed

    @schema_property("succeeded")
    def succeeded(self) -> Optional[List[dict]]:
        return self._property_succeeded

    @succeeded.setter
    def succeeded(self, value: Optional[List[dict]]) -> None:
        if value is None:
            self._property_succeeded = None
            return
        self.assert_isinstance(value, "succeeded", (list, tuple))
        self.assert_isinstance(value, "succeeded", (dict,), is_array=True)
        self._property_succeeded = value

    @schema_property("failed")
    def failed(self) -> Optional[List[dict]]:
        return self._property_failed

    @failed.setter
    def failed(self, value: Optional[List[dict]]) -> None:
        if value is None:
            self._property_failed = None
            return
        self.assert_isinstance(value, "failed", (list, tuple))
        self.assert_isinstance(value, "failed", (dict,), is_array=True)
        self._property_failed = value


class DeleteMetadataRequest(Request):
    """
    Delete metadata from model

    :param model: ID of the model
    :type model: str
    :param keys: The list of metadata keys to delete
    :type keys: Sequence[str]
    """

    _service = "models"
    _action = "delete_metadata"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "keys": {
                "description": "The list of metadata keys to delete",
                "items": {"type": "string"},
                "type": "array",
            },
            "model": {"description": "ID of the model", "type": "string"},
        },
        "required": ["model", "keys"],
        "type": "object",
    }

    def __init__(self, model: str, keys: List[str], **kwargs: Any) -> None:
        super(DeleteMetadataRequest, self).__init__(**kwargs)
        self.model = model
        self.keys = keys

    @schema_property("model")
    def model(self) -> str:
        return self._property_model

    @model.setter
    def model(self, value: str) -> None:
        if value is None:
            self._property_model = None
            return
        self.assert_isinstance(value, "model", six.string_types)
        self._property_model = value

    @schema_property("keys")
    def keys(self) -> List[str]:
        return self._property_keys

    @keys.setter
    def keys(self, value: List[str]) -> None:
        if value is None:
            self._property_keys = None
            return
        self.assert_isinstance(value, "keys", (list, tuple))
        self.assert_isinstance(value, "keys", six.string_types, is_array=True)
        self._property_keys = value


class DeleteMetadataResponse(Response):
    """
    Response of models.delete_metadata endpoint.

    :param updated: Number of models updated (0 or 1)
    :type updated: int
    """

    _service = "models"
    _action = "delete_metadata"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "updated": {
                "description": "Number of models updated (0 or 1)",
                "enum": [0, 1],
                "type": ["integer", "null"],
            }
        },
        "type": "object",
    }

    def __init__(self, updated: Optional[int] = None, **kwargs: Any) -> None:
        super(DeleteMetadataResponse, self).__init__(**kwargs)
        self.updated = updated

    @schema_property("updated")
    def updated(self) -> Optional[int]:
        return self._property_updated

    @updated.setter
    def updated(self, value: Optional[int]) -> None:
        if value is None:
            self._property_updated = None
            return
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        self.assert_isinstance(value, "updated", six.integer_types)
        self._property_updated = value


class EditRequest(Request):
    """
    Edit an existing model

    :param model: Model ID
    :type model: str
    :param uri: URI for the model
    :type uri: str
    :param name: Model name Unique within the company.
    :type name: str
    :param comment: Model comment
    :type comment: str
    :param tags: User-defined tags list
    :type tags: Sequence[str]
    :param system_tags: System tags list. This field is reserved for system use,
        please don't use it.
    :type system_tags: Sequence[str]
    :param framework: Framework on which the model is based. Case insensitive.
        Should be identical to the framework of the task which created the model.
    :type framework: str
    :param design: Json[d] object representing the model design. Should be
        identical to the network design of the task which created the model
    :type design: dict
    :param labels: Json object
    :type labels: dict
    :param ready: Indication if the model is final and can be used by other tasks
    :type ready: bool
    :param project: Project to which to model belongs
    :type project: str
    :param parent: Parent model
    :type parent: str
    :param task: Associated task ID
    :type task: str
    :param iteration: Iteration (used to update task statistics)
    :type iteration: int
    :param metadata: Model metadata
    :type metadata: list
    """

    _service = "models"
    _action = "edit"
    _version = "2.23"
    _schema = {
        "definitions": {
            "metadata_item": {
                "properties": {
                    "key": {
                        "description": "The key uniquely identifying the metadata item inside the given entity",
                        "type": "string",
                    },
                    "type": {
                        "description": "The type of the metadata item",
                        "type": "string",
                    },
                    "value": {
                        "description": "The value stored in the metadata item",
                        "type": "string",
                    },
                },
                "type": "object",
            }
        },
        "properties": {
            "comment": {"description": "Model comment", "type": "string"},
            "design": {
                "additionalProperties": True,
                "description": "Json[d] object representing the model design. Should be identical to the network design of the task which created the model",
                "type": "object",
            },
            "framework": {
                "description": "Framework on which the model is based. Case insensitive. Should be identical to the framework of the task which created the model.",
                "type": "string",
            },
            "iteration": {
                "description": "Iteration (used to update task statistics)",
                "type": "integer",
            },
            "labels": {
                "additionalProperties": {"type": "integer"},
                "description": "Json object",
                "type": "object",
            },
            "model": {"description": "Model ID", "type": "string"},
            "name": {
                "description": "Model name Unique within the company.",
                "type": "string",
            },
            "parent": {"description": "Parent model", "type": "string"},
            "project": {
                "description": "Project to which to model belongs",
                "type": "string",
            },
            "ready": {
                "description": "Indication if the model is final and can be used by other tasks",
                "type": "boolean",
            },
            "system_tags": {
                "description": "System tags list. This field is reserved for system use, please don't use it.",
                "items": {"type": "string"},
                "type": "array",
            },
            "tags": {
                "description": "User-defined tags list",
                "items": {"type": "string"},
                "type": "array",
            },
            "task": {"description": "Associated task ID", "type": "string"},
            "uri": {"description": "URI for the model", "type": "string"},
            "metadata": {
                "type": "array",
                "items": {"$ref": "#/definitions/metadata_item"},
                "description": "Model metadata",
            },
        },
        "required": ["model"],
        "type": "object",
    }

    def __init__(
        self,
        model: str,
        uri: Optional[str] = None,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        tags: Optional[List[str]] = None,
        system_tags: Optional[List[str]] = None,
        framework: Optional[str] = None,
        design: Optional[dict] = None,
        labels: Optional[dict] = None,
        ready: Optional[bool] = None,
        project: Optional[str] = None,
        parent: Optional[str] = None,
        task: Optional[str] = None,
        iteration: Optional[int] = None,
        metadata: Optional[List[Any]] = None,
        **kwargs: Any
    ) -> None:
        super(EditRequest, self).__init__(**kwargs)
        self.model = model
        self.uri = uri
        self.name = name
        self.comment = comment
        self.tags = tags
        self.system_tags = system_tags
        self.framework = framework
        self.design = design
        self.labels = labels
        self.ready = ready
        self.project = project
        self.parent = parent
        self.task = task
        self.iteration = iteration
        self.metadata = metadata

    @schema_property("model")
    def model(self) -> str:
        return self._property_model

    @model.setter
    def model(self, value: str) -> None:
        if value is None:
            self._property_model = None
            return
        self.assert_isinstance(value, "model", six.string_types)
        self._property_model = value

    @schema_property("uri")
    def uri(self) -> Optional[str]:
        return self._property_uri

    @uri.setter
    def uri(self, value: Optional[str]) -> None:
        if value is None:
            self._property_uri = None
            return
        self.assert_isinstance(value, "uri", six.string_types)
        self._property_uri = value

    @schema_property("name")
    def name(self) -> Optional[str]:
        return self._property_name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        if value is None:
            self._property_name = None
            return
        self.assert_isinstance(value, "name", six.string_types)
        self._property_name = value

    @schema_property("comment")
    def comment(self) -> Optional[str]:
        return self._property_comment

    @comment.setter
    def comment(self, value: Optional[str]) -> None:
        if value is None:
            self._property_comment = None
            return
        self.assert_isinstance(value, "comment", six.string_types)
        self._property_comment = value

    @schema_property("tags")
    def tags(self) -> Optional[List[str]]:
        return self._property_tags

    @tags.setter
    def tags(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_tags = None
            return
        self.assert_isinstance(value, "tags", (list, tuple))
        self.assert_isinstance(value, "tags", six.string_types, is_array=True)
        self._property_tags = value

    @schema_property("system_tags")
    def system_tags(self) -> Optional[List[str]]:
        return self._property_system_tags

    @system_tags.setter
    def system_tags(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_system_tags = None
            return
        self.assert_isinstance(value, "system_tags", (list, tuple))
        self.assert_isinstance(value, "system_tags", six.string_types, is_array=True)
        self._property_system_tags = value

    @schema_property("framework")
    def framework(self) -> Optional[str]:
        return self._property_framework

    @framework.setter
    def framework(self, value: Optional[str]) -> None:
        if value is None:
            self._property_framework = None
            return
        self.assert_isinstance(value, "framework", six.string_types)
        self._property_framework = value

    @schema_property("design")
    def design(self) -> Optional[dict]:
        return self._property_design

    @design.setter
    def design(self, value: Optional[dict]) -> None:
        if value is None:
            self._property_design = None
            return
        self.assert_isinstance(value, "design", (dict,))
        self._property_design = value

    @schema_property("labels")
    def labels(self) -> Optional[dict]:
        return self._property_labels

    @labels.setter
    def labels(self, value: Optional[dict]) -> None:
        if value is None:
            self._property_labels = None
            return
        self.assert_isinstance(value, "labels", (dict,))
        self._property_labels = value

    @schema_property("ready")
    def ready(self) -> Optional[bool]:
        return self._property_ready

    @ready.setter
    def ready(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_ready = None
            return
        self.assert_isinstance(value, "ready", (bool,))
        self._property_ready = value

    @schema_property("project")
    def project(self) -> Optional[str]:
        return self._property_project

    @project.setter
    def project(self, value: Optional[str]) -> None:
        if value is None:
            self._property_project = None
            return
        self.assert_isinstance(value, "project", six.string_types)
        self._property_project = value

    @schema_property("parent")
    def parent(self) -> Optional[str]:
        return self._property_parent

    @parent.setter
    def parent(self, value: Optional[str]) -> None:
        if value is None:
            self._property_parent = None
            return
        self.assert_isinstance(value, "parent", six.string_types)
        self._property_parent = value

    @schema_property("task")
    def task(self) -> Optional[str]:
        return self._property_task

    @task.setter
    def task(self, value: Optional[str]) -> None:
        if value is None:
            self._property_task = None
            return
        self.assert_isinstance(value, "task", six.string_types)
        self._property_task = value

    @schema_property("iteration")
    def iteration(self) -> Optional[int]:
        return self._property_iteration

    @iteration.setter
    def iteration(self, value: Optional[int]) -> None:
        if value is None:
            self._property_iteration = None
            return
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        self.assert_isinstance(value, "iteration", six.integer_types)
        self._property_iteration = value

    @schema_property("metadata")
    def metadata(self) -> Optional[List[Any]]:
        return self._property_metadata

    @metadata.setter
    def metadata(self, value: Optional[List[Any]]) -> None:
        if value is None:
            self._property_metadata = None
            return
        self.assert_isinstance(value, "metadata", (list, tuple))
        if any((isinstance(v, dict) for v in value)):
            value = [MetadataItem.from_dict(v) if isinstance(v, dict) else v for v in value]
        else:
            self.assert_isinstance(value, "metadata", MetadataItem, is_array=True)
        self._property_metadata = value


class EditResponse(Response):
    """
    Response of models.edit endpoint.

    :param updated: Number of models updated (0 or 1)
    :type updated: int
    :param fields: Updated fields names and values
    :type fields: dict
    """

    _service = "models"
    _action = "edit"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "fields": {
                "additionalProperties": True,
                "description": "Updated fields names and values",
                "type": ["object", "null"],
            },
            "updated": {
                "description": "Number of models updated (0 or 1)",
                "enum": [0, 1],
                "type": ["integer", "null"],
            },
        },
        "type": "object",
    }

    def __init__(self, updated: Optional[int] = None, fields: Optional[dict] = None, **kwargs: Any) -> None:
        super(EditResponse, self).__init__(**kwargs)
        self.updated = updated
        self.fields = fields

    @schema_property("updated")
    def updated(self) -> Optional[int]:
        return self._property_updated

    @updated.setter
    def updated(self, value: Optional[int]) -> None:
        if value is None:
            self._property_updated = None
            return
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        self.assert_isinstance(value, "updated", six.integer_types)
        self._property_updated = value

    @schema_property("fields")
    def fields(self) -> Optional[dict]:
        return self._property_fields

    @fields.setter
    def fields(self, value: Optional[dict]) -> None:
        if value is None:
            self._property_fields = None
            return
        self.assert_isinstance(value, "fields", (dict,))
        self._property_fields = value


class GetAllRequest(Request):
    """
    Get all models

    :param name: Get only models whose name matches this pattern (python regular
        expression syntax)
    :type name: str
    :param user: List of user IDs used to filter results by the model's creating
        user
    :type user: Sequence[str]
    :param ready: Indication whether to retrieve only models that are marked ready
        If not supplied returns both ready and not-ready projects.
    :type ready: bool
    :param tags: User-defined tags list used to filter results. Prepend '-' to tag
        name to indicate exclusion
    :type tags: Sequence[str]
    :param system_tags: System tags list used to filter results. Prepend '-' to
        system tag name to indicate exclusion
    :type system_tags: Sequence[str]
    :param only_fields: List of model field names (if applicable, nesting is
        supported using '.'). If provided, this list defines the query's projection
        (only these fields will be returned for each result entry)
    :type only_fields: Sequence[str]
    :param page: Page number, returns a specific page out of the resulting list of
        models
    :type page: int
    :param page_size: Page size, specifies the number of results returned in each
        page (last page may contain fewer results)
    :type page_size: int
    :param project: List of associated project IDs
    :type project: Sequence[str]
    :param order_by: List of field names to order by. When search_text is used,
        '@text_score' can be used as a field representing the text score of returned
        documents. Use '-' prefix to specify descending order. Optional, recommended
        when using page
    :type order_by: Sequence[str]
    :param task: List of associated task IDs
    :type task: Sequence[str]
    :param id: List of model IDs
    :type id: Sequence[str]
    :param search_text: Free text search query
    :type search_text: str
    :param framework: List of frameworks
    :type framework: Sequence[str]
    :param uri: List of model URIs
    :type uri: Sequence[str]
    :param last_update: List of last_update constraint strings (utcformat, epoch)
        with an optional prefix modifier (\\>,\\>=, \\<, \\<=)
    :type last_update: Sequence[str]
    :param _all_: Multi-field pattern condition (all fields match pattern)
    :type _all_: MultiFieldPatternData
    :param _any_: Multi-field pattern condition (any field matches pattern)
    :type _any_: MultiFieldPatternData
    :param scroll_id: Scroll ID returned from the previos calls to get_all
    :type scroll_id: str
    :param refresh_scroll: If set then all the data received with this scroll will
        be requeried
    :type refresh_scroll: bool
    :param size: The number of models to retrieve
    :type size: int
    """

    _service = "models"
    _action = "get_all"
    _version = "2.23"
    _schema = {
        "definitions": {
            "multi_field_pattern_data": {
                "properties": {
                    "fields": {
                        "description": "List of field names",
                        "items": {"type": "string"},
                        "type": ["array", "null"],
                    },
                    "pattern": {
                        "description": "Pattern string (regex)",
                        "type": ["string", "null"],
                    },
                },
                "type": "object",
            }
        },
        "dependencies": {"page": ["page_size"]},
        "properties": {
            "_all_": {
                "description": "Multi-field pattern condition (all fields match pattern)",
                "oneOf": [
                    {"$ref": "#/definitions/multi_field_pattern_data"},
                    {"type": "null"},
                ],
            },
            "_any_": {
                "description": "Multi-field pattern condition (any field matches pattern)",
                "oneOf": [
                    {"$ref": "#/definitions/multi_field_pattern_data"},
                    {"type": "null"},
                ],
            },
            "framework": {
                "description": "List of frameworks",
                "items": {"type": "string"},
                "type": ["array", "null"],
            },
            "id": {
                "description": "List of model IDs",
                "items": {"type": "string"},
                "type": ["array", "null"],
            },
            "last_update": {
                "description": "List of last_update constraint strings, or a single string (utcformat, epoch) with an optional prefix modifier (\\>,\\>=, \\<, \\<=)",
                "items": {"pattern": "^(>=|>|<=|<)?.*$", "type": "string"},
                "type": ["string", "array", "null"],
            },
            "name": {
                "description": "Get only models whose name matches this pattern (python regular expression syntax)",
                "type": ["string", "null"],
            },
            "only_fields": {
                "description": "List of model field names (if applicable, nesting is supported using '.'). If provided, this list defines the query's projection (only these fields will be returned for each result entry)",
                "items": {"type": "string"},
                "type": ["array", "null"],
            },
            "order_by": {
                "description": "List of field names to order by. When search_text is used, '@text_score' can be used as a field representing the text score of returned documents. Use '-' prefix to specify descending order. Optional, recommended when using page",
                "items": {"type": "string"},
                "type": ["array", "null"],
            },
            "page": {
                "description": "Page number, returns a specific page out of the resulting list of models",
                "minimum": 0,
                "type": ["integer", "null"],
            },
            "page_size": {
                "description": "Page size, specifies the number of results returned in each page (last page may contain fewer results)",
                "minimum": 1,
                "type": ["integer", "null"],
            },
            "project": {
                "description": "List of associated project IDs",
                "items": {"type": "string"},
                "type": ["array", "null"],
            },
            "ready": {
                "description": "Indication whether to retrieve only models that are marked ready If not supplied returns both ready and not-ready projects.",
                "type": ["boolean", "null"],
            },
            "refresh_scroll": {
                "description": "If set then all the data received with this scroll will be requeried",
                "type": ["boolean", "null"],
            },
            "scroll_id": {
                "description": "Scroll ID returned from the previos calls to get_all",
                "type": ["string", "null"],
            },
            "search_text": {
                "description": "Free text search query",
                "type": ["string", "null"],
            },
            "size": {
                "description": "The number of models to retrieve",
                "minimum": 1,
                "type": ["integer", "null"],
            },
            "system_tags": {
                "description": "System tags list used to filter results. Prepend '-' to system tag name to indicate exclusion",
                "items": {"type": "string"},
                "type": ["array", "null"],
            },
            "tags": {
                "description": "User-defined tags list used to filter results. Prepend '-' to tag name to indicate exclusion",
                "items": {"type": "string"},
                "type": ["array", "null"],
            },
            "task": {
                "description": "List of associated task IDs",
                "items": {"type": "string"},
                "type": ["array", "null"],
            },
            "uri": {
                "description": "List of model URIs",
                "items": {"type": "string"},
                "type": ["array", "null"],
            },
            "user": {
                "description": "List of user IDs used to filter results by the model's creating user",
                "items": {"type": "string"},
                "type": ["array", "null"],
            },
        },
        "type": "object",
    }

    def __init__(
        self,
        name: Optional[str] = None,
        user: Optional[List[str]] = None,
        ready: Optional[bool] = None,
        tags: Optional[List[str]] = None,
        system_tags: Optional[List[str]] = None,
        only_fields: Optional[List[str]] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        project: Optional[List[str]] = None,
        order_by: Optional[List[str]] = None,
        task: Optional[List[str]] = None,
        id: Optional[List[str]] = None,
        search_text: Optional[str] = None,
        framework: Optional[List[str]] = None,
        uri: Optional[List[str]] = None,
        last_update: Optional[Union[str, List[str]]] = None,
        _all_: Any = None,
        _any_: Any = None,
        scroll_id: Optional[str] = None,
        refresh_scroll: Optional[bool] = None,
        size: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        super(GetAllRequest, self).__init__(**kwargs)
        self.name = name
        self.user = user
        self.ready = ready
        self.tags = tags
        self.system_tags = system_tags
        self.only_fields = only_fields
        self.page = page
        self.page_size = page_size
        self.project = project
        self.order_by = order_by
        self.task = task
        self.id = id
        self.search_text = search_text
        self.framework = framework
        self.uri = uri
        self.last_update = last_update
        self._all_ = _all_
        self._any_ = _any_
        self.scroll_id = scroll_id
        self.refresh_scroll = refresh_scroll
        self.size = size

    @schema_property("name")
    def name(self) -> Optional[str]:
        return self._property_name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        if value is None:
            self._property_name = None
            return
        self.assert_isinstance(value, "name", six.string_types)
        self._property_name = value

    @schema_property("user")
    def user(self) -> Optional[List[str]]:
        return self._property_user

    @user.setter
    def user(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_user = None
            return
        self.assert_isinstance(value, "user", (list, tuple))
        self.assert_isinstance(value, "user", six.string_types, is_array=True)
        self._property_user = value

    @schema_property("ready")
    def ready(self) -> Optional[bool]:
        return self._property_ready

    @ready.setter
    def ready(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_ready = None
            return
        self.assert_isinstance(value, "ready", (bool,))
        self._property_ready = value

    @schema_property("tags")
    def tags(self) -> Optional[List[str]]:
        return self._property_tags

    @tags.setter
    def tags(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_tags = None
            return
        self.assert_isinstance(value, "tags", (list, tuple))
        self.assert_isinstance(value, "tags", six.string_types, is_array=True)
        self._property_tags = value

    @schema_property("system_tags")
    def system_tags(self) -> Optional[List[str]]:
        return self._property_system_tags

    @system_tags.setter
    def system_tags(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_system_tags = None
            return
        self.assert_isinstance(value, "system_tags", (list, tuple))
        self.assert_isinstance(value, "system_tags", six.string_types, is_array=True)
        self._property_system_tags = value

    @schema_property("only_fields")
    def only_fields(self) -> Optional[List[str]]:
        return self._property_only_fields

    @only_fields.setter
    def only_fields(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_only_fields = None
            return
        self.assert_isinstance(value, "only_fields", (list, tuple))
        self.assert_isinstance(value, "only_fields", six.string_types, is_array=True)
        self._property_only_fields = value

    @schema_property("page")
    def page(self) -> Optional[int]:
        return self._property_page

    @page.setter
    def page(self, value: Optional[int]) -> None:
        if value is None:
            self._property_page = None
            return
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        self.assert_isinstance(value, "page", six.integer_types)
        self._property_page = value

    @schema_property("page_size")
    def page_size(self) -> Optional[int]:
        return self._property_page_size

    @page_size.setter
    def page_size(self, value: Optional[int]) -> None:
        if value is None:
            self._property_page_size = None
            return
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        self.assert_isinstance(value, "page_size", six.integer_types)
        self._property_page_size = value

    @schema_property("project")
    def project(self) -> Optional[List[str]]:
        return self._property_project

    @project.setter
    def project(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_project = None
            return
        self.assert_isinstance(value, "project", (list, tuple))
        self.assert_isinstance(value, "project", six.string_types, is_array=True)
        self._property_project = value

    @schema_property("order_by")
    def order_by(self) -> Optional[List[str]]:
        return self._property_order_by

    @order_by.setter
    def order_by(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_order_by = None
            return
        self.assert_isinstance(value, "order_by", (list, tuple))
        self.assert_isinstance(value, "order_by", six.string_types, is_array=True)
        self._property_order_by = value

    @schema_property("task")
    def task(self) -> Optional[List[str]]:
        return self._property_task

    @task.setter
    def task(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_task = None
            return
        self.assert_isinstance(value, "task", (list, tuple))
        self.assert_isinstance(value, "task", six.string_types, is_array=True)
        self._property_task = value

    @schema_property("id")
    def id(self) -> Optional[List[str]]:
        return self._property_id

    @id.setter
    def id(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_id = None
            return
        self.assert_isinstance(value, "id", (list, tuple))
        self.assert_isinstance(value, "id", six.string_types, is_array=True)
        self._property_id = value

    @schema_property("search_text")
    def search_text(self) -> Optional[str]:
        return self._property_search_text

    @search_text.setter
    def search_text(self, value: Optional[str]) -> None:
        if value is None:
            self._property_search_text = None
            return
        self.assert_isinstance(value, "search_text", six.string_types)
        self._property_search_text = value

    @schema_property("framework")
    def framework(self) -> Optional[List[str]]:
        return self._property_framework

    @framework.setter
    def framework(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_framework = None
            return
        self.assert_isinstance(value, "framework", (list, tuple))
        self.assert_isinstance(value, "framework", six.string_types, is_array=True)
        self._property_framework = value

    @schema_property("uri")
    def uri(self) -> Optional[List[str]]:
        return self._property_uri

    @uri.setter
    def uri(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_uri = None
            return
        self.assert_isinstance(value, "uri", (list, tuple))
        self.assert_isinstance(value, "uri", six.string_types, is_array=True)
        self._property_uri = value

    @schema_property("last_update")
    def last_update(self) -> Optional[Union[str, List[str]]]:
        return self._property_last_update

    @last_update.setter
    def last_update(self, value: Optional[Union[str, List[str]]]) -> None:
        if value is None:
            self._property_last_update = None
            return
        self.assert_isinstance(value, "last_update", (str, list, tuple))
        if not isinstance(value, six.string_types):
            self.assert_isinstance(value, "last_update", six.string_types, is_array=True)
        self._property_last_update = value

    @schema_property("_all_")
    def _all_(self) -> Any:
        return self._property__all_

    @_all_.setter
    def _all_(self, value: Any) -> None:
        if value is None:
            self._property__all_ = None
            return
        if isinstance(value, dict):
            value = MultiFieldPatternData.from_dict(value)
        else:
            self.assert_isinstance(value, "_all_", MultiFieldPatternData)
        self._property__all_ = value

    @schema_property("_any_")
    def _any_(self) -> Any:
        return self._property__any_

    @_any_.setter
    def _any_(self, value: Any) -> None:
        if value is None:
            self._property__any_ = None
            return
        if isinstance(value, dict):
            value = MultiFieldPatternData.from_dict(value)
        else:
            self.assert_isinstance(value, "_any_", MultiFieldPatternData)
        self._property__any_ = value

    @schema_property("scroll_id")
    def scroll_id(self) -> Optional[str]:
        return self._property_scroll_id

    @scroll_id.setter
    def scroll_id(self, value: Optional[str]) -> None:
        if value is None:
            self._property_scroll_id = None
            return
        self.assert_isinstance(value, "scroll_id", six.string_types)
        self._property_scroll_id = value

    @schema_property("refresh_scroll")
    def refresh_scroll(self) -> Optional[bool]:
        return self._property_refresh_scroll

    @refresh_scroll.setter
    def refresh_scroll(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_refresh_scroll = None
            return
        self.assert_isinstance(value, "refresh_scroll", (bool,))
        self._property_refresh_scroll = value

    @schema_property("size")
    def size(self) -> Optional[int]:
        return self._property_size

    @size.setter
    def size(self, value: Optional[int]) -> None:
        if value is None:
            self._property_size = None
            return
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        self.assert_isinstance(value, "size", six.integer_types)
        self._property_size = value


class GetAllResponse(Response):
    """
    Response of models.get_all endpoint.

    :param models: Models list
    :type models: Sequence[Model]
    :param scroll_id: Scroll ID that can be used with the next calls to get_all to
        retrieve more data
    :type scroll_id: str
    """

    _service = "models"
    _action = "get_all"
    _version = "2.23"
    _schema = {
        "definitions": {
            "metadata_item": {
                "properties": {
                    "key": {
                        "description": "The key uniquely identifying the metadata item inside the given entity",
                        "type": ["string", "null"],
                    },
                    "type": {
                        "description": "The type of the metadata item",
                        "type": ["string", "null"],
                    },
                    "value": {
                        "description": "The value stored in the metadata item",
                        "type": ["string", "null"],
                    },
                },
                "type": "object",
            },
            "model": {
                "properties": {
                    "comment": {
                        "description": "Model comment",
                        "type": ["string", "null"],
                    },
                    "company": {
                        "description": "Company id",
                        "type": ["string", "null"],
                    },
                    "created": {
                        "description": "Model creation time",
                        "format": "date-time",
                        "type": ["string", "null"],
                    },
                    "design": {
                        "additionalProperties": True,
                        "description": "Json object representing the model design. Should be identical to the network design of the task which created the model",
                        "type": ["object", "null"],
                    },
                    "framework": {
                        "description": "Framework on which the model is based. Should be identical to the framework of the task which created the model",
                        "type": ["string", "null"],
                    },
                    "id": {"description": "Model id", "type": ["string", "null"]},
                    "labels": {
                        "additionalProperties": {"type": "integer"},
                        "description": "Json object representing the ids of the labels in the model. The keys are the layers' names and the values are the ids.",
                        "type": ["object", "null"],
                    },
                    "last_update": {
                        "description": "Model last update time",
                        "format": "date-time",
                        "type": ["string", "null"],
                    },
                    "metadata": {
                        "additionalProperties": {"$ref": "#/definitions/metadata_item"},
                        "description": "Model metadata",
                        "type": ["object", "null"],
                    },
                    "name": {"description": "Model name", "type": ["string", "null"]},
                    "parent": {
                        "description": "Parent model ID",
                        "type": ["string", "null"],
                    },
                    "project": {
                        "description": "Associated project ID",
                        "type": ["string", "null"],
                    },
                    "ready": {
                        "description": "Indication if the model is final and can be used by other tasks",
                        "type": ["boolean", "null"],
                    },
                    "stats": {
                        "description": "Model statistics",
                        "properties": {
                            "labels_count": {
                                "description": "Number of the model labels",
                                "type": "integer",
                            }
                        },
                        "type": ["object", "null"],
                    },
                    "system_tags": {
                        "description": "System tags. This field is reserved for system use, please don't use it.",
                        "items": {"type": "string"},
                        "type": ["array", "null"],
                    },
                    "tags": {
                        "description": "User-defined tags",
                        "items": {"type": "string"},
                        "type": ["array", "null"],
                    },
                    "task": {
                        "description": "Task ID of task in which the model was created",
                        "type": ["string", "null"],
                    },
                    "ui_cache": {
                        "additionalProperties": True,
                        "description": "UI cache for this model",
                        "type": ["object", "null"],
                    },
                    "uri": {
                        "description": "URI for the model, pointing to the destination storage.",
                        "type": ["string", "null"],
                    },
                    "user": {
                        "description": "Associated user id",
                        "type": ["string", "null"],
                    },
                },
                "type": "object",
            },
        },
        "properties": {
            "models": {
                "description": "Models list",
                "items": {"$ref": "#/definitions/model"},
                "type": ["array", "null"],
            },
            "scroll_id": {
                "description": "Scroll ID that can be used with the next calls to get_all to retrieve more data",
                "type": ["string", "null"],
            },
        },
        "type": "object",
    }

    def __init__(self, models: Optional[List[Any]] = None, scroll_id: Optional[str] = None, **kwargs: Any) -> None:
        super(GetAllResponse, self).__init__(**kwargs)
        self.models = models
        self.scroll_id = scroll_id

    @schema_property("models")
    def models(self) -> Optional[List[Any]]:
        return self._property_models

    @models.setter
    def models(self, value: Optional[List[Any]]) -> None:
        if value is None:
            self._property_models = None
            return
        self.assert_isinstance(value, "models", (list, tuple))
        if any((isinstance(v, dict) for v in value)):
            value = [Model.from_dict(v) if isinstance(v, dict) else v for v in value]
        else:
            self.assert_isinstance(value, "models", Model, is_array=True)
        self._property_models = value

    @schema_property("scroll_id")
    def scroll_id(self) -> Optional[str]:
        return self._property_scroll_id

    @scroll_id.setter
    def scroll_id(self, value: Optional[str]) -> None:
        if value is None:
            self._property_scroll_id = None
            return
        self.assert_isinstance(value, "scroll_id", six.string_types)
        self._property_scroll_id = value


class GetByIdRequest(Request):
    """
    Gets model information

    :param model: Model id
    :type model: str
    """

    _service = "models"
    _action = "get_by_id"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {"model": {"description": "Model id", "type": "string"}},
        "required": ["model"],
        "type": "object",
    }

    def __init__(self, model: str, **kwargs: Any) -> None:
        super(GetByIdRequest, self).__init__(**kwargs)
        self.model = model

    @schema_property("model")
    def model(self) -> str:
        return self._property_model

    @model.setter
    def model(self, value: str) -> None:
        if value is None:
            self._property_model = None
            return
        self.assert_isinstance(value, "model", six.string_types)
        self._property_model = value


class GetByIdResponse(Response):
    """
    Response of models.get_by_id endpoint.

    :param model: Model info
    :type model: Model
    """

    _service = "models"
    _action = "get_by_id"
    _version = "2.23"
    _schema = {
        "definitions": {
            "metadata_item": {
                "properties": {
                    "key": {
                        "description": "The key uniquely identifying the metadata item inside the given entity",
                        "type": ["string", "null"],
                    },
                    "type": {
                        "description": "The type of the metadata item",
                        "type": ["string", "null"],
                    },
                    "value": {
                        "description": "The value stored in the metadata item",
                        "type": ["string", "null"],
                    },
                },
                "type": "object",
            },
            "model": {
                "properties": {
                    "comment": {
                        "description": "Model comment",
                        "type": ["string", "null"],
                    },
                    "company": {
                        "description": "Company id",
                        "type": ["string", "null"],
                    },
                    "created": {
                        "description": "Model creation time",
                        "format": "date-time",
                        "type": ["string", "null"],
                    },
                    "design": {
                        "additionalProperties": True,
                        "description": "Json object representing the model design. Should be identical to the network design of the task which created the model",
                        "type": ["object", "null"],
                    },
                    "framework": {
                        "description": "Framework on which the model is based. Should be identical to the framework of the task which created the model",
                        "type": ["string", "null"],
                    },
                    "id": {"description": "Model id", "type": ["string", "null"]},
                    "labels": {
                        "additionalProperties": {"type": "integer"},
                        "description": "Json object representing the ids of the labels in the model. The keys are the layers' names and the values are the ids.",
                        "type": ["object", "null"],
                    },
                    "last_update": {
                        "description": "Model last update time",
                        "format": "date-time",
                        "type": ["string", "null"],
                    },
                    "metadata": {
                        "additionalProperties": {"$ref": "#/definitions/metadata_item"},
                        "description": "Model metadata",
                        "type": ["object", "null"],
                    },
                    "name": {"description": "Model name", "type": ["string", "null"]},
                    "parent": {
                        "description": "Parent model ID",
                        "type": ["string", "null"],
                    },
                    "project": {
                        "description": "Associated project ID",
                        "type": ["string", "null"],
                    },
                    "ready": {
                        "description": "Indication if the model is final and can be used by other tasks",
                        "type": ["boolean", "null"],
                    },
                    "stats": {
                        "description": "Model statistics",
                        "properties": {
                            "labels_count": {
                                "description": "Number of the model labels",
                                "type": "integer",
                            }
                        },
                        "type": ["object", "null"],
                    },
                    "system_tags": {
                        "description": "System tags. This field is reserved for system use, please don't use it.",
                        "items": {"type": "string"},
                        "type": ["array", "null"],
                    },
                    "tags": {
                        "description": "User-defined tags",
                        "items": {"type": "string"},
                        "type": ["array", "null"],
                    },
                    "task": {
                        "description": "Task ID of task in which the model was created",
                        "type": ["string", "null"],
                    },
                    "ui_cache": {
                        "additionalProperties": True,
                        "description": "UI cache for this model",
                        "type": ["object", "null"],
                    },
                    "uri": {
                        "description": "URI for the model, pointing to the destination storage.",
                        "type": ["string", "null"],
                    },
                    "user": {
                        "description": "Associated user id",
                        "type": ["string", "null"],
                    },
                },
                "type": "object",
            },
        },
        "properties": {
            "model": {
                "description": "Model info",
                "oneOf": [{"$ref": "#/definitions/model"}, {"type": "null"}],
            }
        },
        "type": "object",
    }

    def __init__(self, model: Any = None, **kwargs: Any) -> None:
        super(GetByIdResponse, self).__init__(**kwargs)
        self.model = model

    @schema_property("model")
    def model(self) -> Any:
        return self._property_model

    @model.setter
    def model(self, value: Any) -> None:
        if value is None:
            self._property_model = None
            return
        if isinstance(value, dict):
            value = Model.from_dict(value)
        else:
            self.assert_isinstance(value, "model", Model)
        self._property_model = value


class GetByTaskIdRequest(Request):
    """
    Gets model information

    :param task: Task id
    :type task: str
    """

    _service = "models"
    _action = "get_by_task_id"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {"task": {"description": "Task id", "type": ["string", "null"]}},
        "type": "object",
    }

    def __init__(self, task: Optional[str] = None, **kwargs: Any) -> None:
        super(GetByTaskIdRequest, self).__init__(**kwargs)
        self.task = task

    @schema_property("task")
    def task(self) -> Optional[str]:
        return self._property_task

    @task.setter
    def task(self, value: Optional[str]) -> None:
        if value is None:
            self._property_task = None
            return
        self.assert_isinstance(value, "task", six.string_types)
        self._property_task = value


class GetByTaskIdResponse(Response):
    """
    Response of models.get_by_task_id endpoint.

    :param model: Model info
    :type model: Model
    """

    _service = "models"
    _action = "get_by_task_id"
    _version = "2.23"
    _schema = {
        "definitions": {
            "metadata_item": {
                "properties": {
                    "key": {
                        "description": "The key uniquely identifying the metadata item inside the given entity",
                        "type": ["string", "null"],
                    },
                    "type": {
                        "description": "The type of the metadata item",
                        "type": ["string", "null"],
                    },
                    "value": {
                        "description": "The value stored in the metadata item",
                        "type": ["string", "null"],
                    },
                },
                "type": "object",
            },
            "model": {
                "properties": {
                    "comment": {
                        "description": "Model comment",
                        "type": ["string", "null"],
                    },
                    "company": {
                        "description": "Company id",
                        "type": ["string", "null"],
                    },
                    "created": {
                        "description": "Model creation time",
                        "format": "date-time",
                        "type": ["string", "null"],
                    },
                    "design": {
                        "additionalProperties": True,
                        "description": "Json object representing the model design. Should be identical to the network design of the task which created the model",
                        "type": ["object", "null"],
                    },
                    "framework": {
                        "description": "Framework on which the model is based. Should be identical to the framework of the task which created the model",
                        "type": ["string", "null"],
                    },
                    "id": {"description": "Model id", "type": ["string", "null"]},
                    "labels": {
                        "additionalProperties": {"type": "integer"},
                        "description": "Json object representing the ids of the labels in the model. The keys are the layers' names and the values are the ids.",
                        "type": ["object", "null"],
                    },
                    "last_update": {
                        "description": "Model last update time",
                        "format": "date-time",
                        "type": ["string", "null"],
                    },
                    "metadata": {
                        "additionalProperties": {"$ref": "#/definitions/metadata_item"},
                        "description": "Model metadata",
                        "type": ["object", "null"],
                    },
                    "name": {"description": "Model name", "type": ["string", "null"]},
                    "parent": {
                        "description": "Parent model ID",
                        "type": ["string", "null"],
                    },
                    "project": {
                        "description": "Associated project ID",
                        "type": ["string", "null"],
                    },
                    "ready": {
                        "description": "Indication if the model is final and can be used by other tasks",
                        "type": ["boolean", "null"],
                    },
                    "stats": {
                        "description": "Model statistics",
                        "properties": {
                            "labels_count": {
                                "description": "Number of the model labels",
                                "type": "integer",
                            }
                        },
                        "type": ["object", "null"],
                    },
                    "system_tags": {
                        "description": "System tags. This field is reserved for system use, please don't use it.",
                        "items": {"type": "string"},
                        "type": ["array", "null"],
                    },
                    "tags": {
                        "description": "User-defined tags",
                        "items": {"type": "string"},
                        "type": ["array", "null"],
                    },
                    "task": {
                        "description": "Task ID of task in which the model was created",
                        "type": ["string", "null"],
                    },
                    "ui_cache": {
                        "additionalProperties": True,
                        "description": "UI cache for this model",
                        "type": ["object", "null"],
                    },
                    "uri": {
                        "description": "URI for the model, pointing to the destination storage.",
                        "type": ["string", "null"],
                    },
                    "user": {
                        "description": "Associated user id",
                        "type": ["string", "null"],
                    },
                },
                "type": "object",
            },
        },
        "properties": {
            "model": {
                "description": "Model info",
                "oneOf": [{"$ref": "#/definitions/model"}, {"type": "null"}],
            }
        },
        "type": "object",
    }

    def __init__(self, model: Any = None, **kwargs: Any) -> None:
        super(GetByTaskIdResponse, self).__init__(**kwargs)
        self.model = model

    @schema_property("model")
    def model(self) -> Any:
        return self._property_model

    @model.setter
    def model(self, value: Any) -> None:
        if value is None:
            self._property_model = None
            return
        if isinstance(value, dict):
            value = Model.from_dict(value)
        else:
            self.assert_isinstance(value, "model", Model)
        self._property_model = value


class MakePrivateRequest(Request):
    """
    Convert public models to private

    :param ids: Ids of the models to convert. Only the models originated by the
        company can be converted
    :type ids: Sequence[str]
    """

    _service = "models"
    _action = "make_private"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "ids": {
                "description": "Ids of the models to convert. Only the models originated by the company can be converted",
                "items": {"type": "string"},
                "type": ["array", "null"],
            }
        },
        "type": "object",
    }

    def __init__(self, ids: Optional[List[str]] = None, **kwargs: Any) -> None:
        super(MakePrivateRequest, self).__init__(**kwargs)
        self.ids = ids

    @schema_property("ids")
    def ids(self) -> Optional[List[str]]:
        return self._property_ids

    @ids.setter
    def ids(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_ids = None
            return
        self.assert_isinstance(value, "ids", (list, tuple))
        self.assert_isinstance(value, "ids", six.string_types, is_array=True)
        self._property_ids = value


class MakePrivateResponse(Response):
    """
    Response of models.make_private endpoint.

    :param updated: Number of models updated
    :type updated: int
    """

    _service = "models"
    _action = "make_private"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "updated": {
                "description": "Number of models updated",
                "type": ["integer", "null"],
            }
        },
        "type": "object",
    }

    def __init__(self, updated: Optional[int] = None, **kwargs: Any) -> None:
        super(MakePrivateResponse, self).__init__(**kwargs)
        self.updated = updated

    @schema_property("updated")
    def updated(self) -> Optional[int]:
        return self._property_updated

    @updated.setter
    def updated(self, value: Optional[int]) -> None:
        if value is None:
            self._property_updated = None
            return
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        self.assert_isinstance(value, "updated", six.integer_types)
        self._property_updated = value


class MakePublicRequest(Request):
    """
    Convert company models to public

    :param ids: Ids of the models to convert
    :type ids: Sequence[str]
    """

    _service = "models"
    _action = "make_public"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "ids": {
                "description": "Ids of the models to convert",
                "items": {"type": "string"},
                "type": ["array", "null"],
            }
        },
        "type": "object",
    }

    def __init__(self, ids: Optional[List[str]] = None, **kwargs: Any) -> None:
        super(MakePublicRequest, self).__init__(**kwargs)
        self.ids = ids

    @schema_property("ids")
    def ids(self) -> Optional[List[str]]:
        return self._property_ids

    @ids.setter
    def ids(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_ids = None
            return
        self.assert_isinstance(value, "ids", (list, tuple))
        self.assert_isinstance(value, "ids", six.string_types, is_array=True)
        self._property_ids = value


class MakePublicResponse(Response):
    """
    Response of models.make_public endpoint.

    :param updated: Number of models updated
    :type updated: int
    """

    _service = "models"
    _action = "make_public"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "updated": {
                "description": "Number of models updated",
                "type": ["integer", "null"],
            }
        },
        "type": "object",
    }

    def __init__(self, updated: Optional[int] = None, **kwargs: Any) -> None:
        super(MakePublicResponse, self).__init__(**kwargs)
        self.updated = updated

    @schema_property("updated")
    def updated(self) -> Optional[int]:
        return self._property_updated

    @updated.setter
    def updated(self, value: Optional[int]) -> None:
        if value is None:
            self._property_updated = None
            return
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        self.assert_isinstance(value, "updated", six.integer_types)
        self._property_updated = value


class GetFrameworksRequest(Request):
    """
    Get the list of frameworks used in the company models

    :param projects: The list of projects which models will be analyzed. If not
        passed or empty then all the company and public models will be analyzed
    :type projects: Sequence[str]
    """

    _service = "models"
    _action = "get_frameworks"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "projects": {
                "description": "The list of projects which models will be analyzed. If not passed or empty then all the company and public models will be analyzed",
                "items": {"type": "string"},
                "type": ["array", "null"],
            }
        },
        "type": "object",
    }

    def __init__(self, projects: Optional[List[str]] = None, **kwargs: Any) -> None:
        super(GetFrameworksRequest, self).__init__(**kwargs)
        self.projects = projects

    @schema_property("projects")
    def projects(self) -> Optional[List[str]]:
        return self._property_projects

    @projects.setter
    def projects(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_projects = None
            return
        self.assert_isinstance(value, "projects", (list, tuple))
        self.assert_isinstance(value, "projects", six.string_types, is_array=True)
        self._property_projects = value


class GetFrameworksResponse(Response):
    """
    Response of models.get_frameworks endpoint.

    :param frameworks: Unique list of the frameworks used in the company models
    :type frameworks: Sequence[str]
    """

    _service = "models"
    _action = "get_frameworks"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "frameworks": {
                "description": "Unique list of the frameworks used in the company models",
                "items": {"type": "string"},
                "type": ["array", "null"],
            }
        },
        "type": "object",
    }

    def __init__(self, frameworks: Optional[List[str]] = None, **kwargs: Any) -> None:
        super(GetFrameworksResponse, self).__init__(**kwargs)
        self.frameworks = frameworks

    @schema_property("frameworks")
    def frameworks(self) -> Optional[List[str]]:
        return self._property_frameworks

    @frameworks.setter
    def frameworks(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_frameworks = None
            return
        self.assert_isinstance(value, "frameworks", (list, tuple))
        self.assert_isinstance(value, "frameworks", six.string_types, is_array=True)
        self._property_frameworks = value


class MoveRequest(Request):
    """
    Move models to a project

    :param ids: Models to move
    :type ids: Sequence[str]
    :param project: Target project ID. If not provided, `project_name` must be
        provided. Use null for the root project
    :type project: str
    :param project_name: Target project name. If provided and a project with this
        name does not exist, a new project will be created. If not provided, `project`
        must be provided.
    :type project_name: str
    """

    _service = "models"
    _action = "move"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "ids": {
                "description": "Models to move",
                "items": {"type": "string"},
                "type": "array",
            },
            "project": {
                "description": "Target project ID. If not provided, `project_name` must be provided. Use null for the root project",
                "type": "string",
            },
            "project_name": {
                "description": "Target project name. If provided and a project with this name does not exist, a new project will be created. If not provided, `project` must be provided.",
                "type": "string",
            },
        },
        "required": ["ids"],
        "type": "object",
    }

    def __init__(
        self, ids: List[str], project: Optional[str] = None, project_name: Optional[str] = None, **kwargs: Any
    ) -> None:
        super(MoveRequest, self).__init__(**kwargs)
        self.ids = ids
        self.project = project
        self.project_name = project_name

    @schema_property("ids")
    def ids(self) -> List[str]:
        return self._property_ids

    @ids.setter
    def ids(self, value: List[str]) -> None:
        if value is None:
            self._property_ids = None
            return
        self.assert_isinstance(value, "ids", (list, tuple))
        self.assert_isinstance(value, "ids", six.string_types, is_array=True)
        self._property_ids = value

    @schema_property("project")
    def project(self) -> Optional[str]:
        return self._property_project

    @project.setter
    def project(self, value: Optional[str]) -> None:
        if value is None:
            self._property_project = None
            return
        self.assert_isinstance(value, "project", six.string_types)
        self._property_project = value

    @schema_property("project_name")
    def project_name(self) -> Optional[str]:
        return self._property_project_name

    @project_name.setter
    def project_name(self, value: Optional[str]) -> None:
        if value is None:
            self._property_project_name = None
            return
        self.assert_isinstance(value, "project_name", six.string_types)
        self._property_project_name = value


class MoveResponse(Response):
    """
    Response of models.move endpoint.

    """

    _service = "models"
    _action = "move"
    _version = "2.23"
    _schema = {"additionalProperties": True, "definitions": {}, "type": "object"}


class PublishManyRequest(Request):
    """
    Publish models

    :param ids: IDs of the models to publish
    :type ids: Sequence[str]
    :param force_publish_task: Publish the associated tasks (if exist) even if they
        are not in the 'stopped' state. Optional, the default value is False.
    :type force_publish_task: bool
    :param publish_tasks: Indicates that the associated tasks (if exist) should be
        published. Optional, the default value is True.
    :type publish_tasks: bool
    """

    _service = "models"
    _action = "publish_many"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "force_publish_task": {
                "description": "Publish the associated tasks (if exist) even if they are not in the 'stopped' state. Optional, the default value is False.",
                "type": "boolean",
            },
            "ids": {
                "description": "IDs of the models to publish",
                "items": {"type": "string"},
                "type": "array",
            },
            "publish_tasks": {
                "description": "Indicates that the associated tasks (if exist) should be published. Optional, the default value is True.",
                "type": "boolean",
            },
        },
        "required": ["ids"],
        "type": "object",
    }

    def __init__(
        self,
        ids: List[str],
        force_publish_task: Optional[bool] = None,
        publish_tasks: Optional[bool] = None,
        **kwargs: Any
    ) -> None:
        super(PublishManyRequest, self).__init__(**kwargs)
        self.ids = ids
        self.force_publish_task = force_publish_task
        self.publish_tasks = publish_tasks

    @schema_property("ids")
    def ids(self) -> List[str]:
        return self._property_ids

    @ids.setter
    def ids(self, value: List[str]) -> None:
        if value is None:
            self._property_ids = None
            return
        self.assert_isinstance(value, "ids", (list, tuple))
        self.assert_isinstance(value, "ids", six.string_types, is_array=True)
        self._property_ids = value

    @schema_property("force_publish_task")
    def force_publish_task(self) -> Optional[bool]:
        return self._property_force_publish_task

    @force_publish_task.setter
    def force_publish_task(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_force_publish_task = None
            return
        self.assert_isinstance(value, "force_publish_task", (bool,))
        self._property_force_publish_task = value

    @schema_property("publish_tasks")
    def publish_tasks(self) -> Optional[bool]:
        return self._property_publish_tasks

    @publish_tasks.setter
    def publish_tasks(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_publish_tasks = None
            return
        self.assert_isinstance(value, "publish_tasks", (bool,))
        self._property_publish_tasks = value


class PublishManyResponse(Response):
    """
    Response of models.publish_many endpoint.

    :param succeeded:
    :type succeeded: Sequence[dict]
    :param failed:
    :type failed: Sequence[dict]
    """

    _service = "models"
    _action = "publish_many"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "failed": {
                "items": {
                    "properties": {
                        "error": {
                            "description": "Error info",
                            "properties": {
                                "codes": {
                                    "items": {"type": "integer"},
                                    "type": "array",
                                },
                                "data": {
                                    "additionalProperties": True,
                                    "type": "object",
                                },
                                "msg": {"type": "string"},
                            },
                            "type": "object",
                        },
                        "id": {
                            "description": "ID of the failed entity",
                            "type": "string",
                        },
                    },
                    "type": "object",
                },
                "type": ["array", "null"],
            },
            "succeeded": {
                "items": {
                    "properties": {
                        "id": {
                            "description": "ID of the succeeded entity",
                            "type": "string",
                        },
                        "published_task": {
                            "description": "Result of publishing of the model's associated task (if exists). Returned only if the task was published successfully as part of the model publishing.",
                            "properties": {
                                "data": {
                                    "description": "Data returned from the task publishing operation.",
                                    "properties": {
                                        "fields": {
                                            "additionalProperties": True,
                                            "description": "Updated fields names and values",
                                            "type": "object",
                                        },
                                        "updated": {
                                            "description": "Number of tasks updated (0 or 1)",
                                            "enum": [0, 1],
                                            "type": "integer",
                                        },
                                    },
                                    "type": "object",
                                },
                                "id": {"description": "Task id", "type": "string"},
                            },
                            "type": "object",
                        },
                        "updated": {
                            "description": "Indicates whether the model was updated",
                            "type": "boolean",
                        },
                    },
                    "type": "object",
                },
                "type": ["array", "null"],
            },
        },
        "type": "object",
    }

    def __init__(
        self, succeeded: Optional[List[dict]] = None, failed: Optional[List[dict]] = None, **kwargs: Any
    ) -> None:
        super(PublishManyResponse, self).__init__(**kwargs)
        self.succeeded = succeeded
        self.failed = failed

    @schema_property("succeeded")
    def succeeded(self) -> Optional[List[dict]]:
        return self._property_succeeded

    @succeeded.setter
    def succeeded(self, value: Optional[List[dict]]) -> None:
        if value is None:
            self._property_succeeded = None
            return
        self.assert_isinstance(value, "succeeded", (list, tuple))
        self.assert_isinstance(value, "succeeded", (dict,), is_array=True)
        self._property_succeeded = value

    @schema_property("failed")
    def failed(self) -> Optional[List[dict]]:
        return self._property_failed

    @failed.setter
    def failed(self, value: Optional[List[dict]]) -> None:
        if value is None:
            self._property_failed = None
            return
        self.assert_isinstance(value, "failed", (list, tuple))
        self.assert_isinstance(value, "failed", (dict,), is_array=True)
        self._property_failed = value


class SetReadyRequest(Request):
    """
    Set the model ready flag to True. If the model is an output model of a task then try to publish the task.

    :param model: Model id
    :type model: str
    :param force_publish_task: Publish the associated task (if exists) even if it
        is not in the 'stopped' state. Optional, the default value is False.
    :type force_publish_task: bool
    :param publish_task: Indicates that the associated task (if exists) should be
        published. Optional, the default value is True.
    :type publish_task: bool
    """

    _service = "models"
    _action = "set_ready"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "force_publish_task": {
                "description": "Publish the associated task (if exists) even if it is not in the 'stopped' state. Optional, the default value is False.",
                "type": "boolean",
            },
            "model": {"description": "Model id", "type": "string"},
            "publish_task": {
                "description": "Indicates that the associated task (if exists) should be published. Optional, the default value is True.",
                "type": "boolean",
            },
        },
        "required": ["model"],
        "type": "object",
    }

    def __init__(
        self, model: str, force_publish_task: Optional[bool] = None, publish_task: Optional[bool] = None, **kwargs: Any
    ) -> None:
        super(SetReadyRequest, self).__init__(**kwargs)
        self.model = model
        self.force_publish_task = force_publish_task
        self.publish_task = publish_task

    @schema_property("model")
    def model(self) -> str:
        return self._property_model

    @model.setter
    def model(self, value: str) -> None:
        if value is None:
            self._property_model = None
            return
        self.assert_isinstance(value, "model", six.string_types)
        self._property_model = value

    @schema_property("force_publish_task")
    def force_publish_task(self) -> Optional[bool]:
        return self._property_force_publish_task

    @force_publish_task.setter
    def force_publish_task(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_force_publish_task = None
            return
        self.assert_isinstance(value, "force_publish_task", (bool,))
        self._property_force_publish_task = value

    @schema_property("publish_task")
    def publish_task(self) -> Optional[bool]:
        return self._property_publish_task

    @publish_task.setter
    def publish_task(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_publish_task = None
            return
        self.assert_isinstance(value, "publish_task", (bool,))
        self._property_publish_task = value


class SetReadyResponse(Response):
    """
    Response of models.set_ready endpoint.

    :param updated: Number of models updated (0 or 1)
    :type updated: int
    :param published_task: Result of publishing of the model's associated task (if
        exists). Returned only if the task was published successfully as part of the
        model publishing.
    :type published_task: dict
    """

    _service = "models"
    _action = "set_ready"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "published_task": {
                "description": "Result of publishing of the model's associated task (if exists). Returned only if the task was published successfully as part of the model publishing.",
                "properties": {
                    "data": {
                        "description": "Data returned from the task publishing operation.",
                        "properties": {
                            "fields": {
                                "additionalProperties": True,
                                "description": "Updated fields names and values",
                                "type": "object",
                            },
                            "updated": {
                                "description": "Number of tasks updated (0 or 1)",
                                "enum": [0, 1],
                                "type": "integer",
                            },
                        },
                        "type": "object",
                    },
                    "id": {"description": "Task id", "type": "string"},
                },
                "type": ["object", "null"],
            },
            "updated": {
                "description": "Number of models updated (0 or 1)",
                "enum": [0, 1],
                "type": ["integer", "null"],
            },
        },
        "type": "object",
    }

    def __init__(self, updated: Optional[int] = None, published_task: Optional[dict] = None, **kwargs: Any) -> None:
        super(SetReadyResponse, self).__init__(**kwargs)
        self.updated = updated
        self.published_task = published_task

    @schema_property("updated")
    def updated(self) -> Optional[int]:
        return self._property_updated

    @updated.setter
    def updated(self, value: Optional[int]) -> None:
        if value is None:
            self._property_updated = None
            return
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        self.assert_isinstance(value, "updated", six.integer_types)
        self._property_updated = value

    @schema_property("published_task")
    def published_task(self) -> Optional[dict]:
        return self._property_published_task

    @published_task.setter
    def published_task(self, value: Optional[dict]) -> None:
        if value is None:
            self._property_published_task = None
            return
        self.assert_isinstance(value, "published_task", (dict,))
        self._property_published_task = value


class UnarchiveManyRequest(Request):
    """
    Unarchive models

    :param ids: IDs of the models to unarchive
    :type ids: Sequence[str]
    """

    _service = "models"
    _action = "unarchive_many"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "ids": {
                "description": "IDs of the models to unarchive",
                "items": {"type": "string"},
                "type": "array",
            }
        },
        "required": ["ids"],
        "type": "object",
    }

    def __init__(self, ids: List[str], **kwargs: Any) -> None:
        super(UnarchiveManyRequest, self).__init__(**kwargs)
        self.ids = ids

    @schema_property("ids")
    def ids(self) -> List[str]:
        return self._property_ids

    @ids.setter
    def ids(self, value: List[str]) -> None:
        if value is None:
            self._property_ids = None
            return
        self.assert_isinstance(value, "ids", (list, tuple))
        self.assert_isinstance(value, "ids", six.string_types, is_array=True)
        self._property_ids = value


class UnarchiveManyResponse(Response):
    """
    Response of models.unarchive_many endpoint.

    :param succeeded:
    :type succeeded: Sequence[dict]
    :param failed:
    :type failed: Sequence[dict]
    """

    _service = "models"
    _action = "unarchive_many"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "failed": {
                "items": {
                    "properties": {
                        "error": {
                            "description": "Error info",
                            "properties": {
                                "codes": {
                                    "items": {"type": "integer"},
                                    "type": "array",
                                },
                                "data": {
                                    "additionalProperties": True,
                                    "type": "object",
                                },
                                "msg": {"type": "string"},
                            },
                            "type": "object",
                        },
                        "id": {
                            "description": "ID of the failed entity",
                            "type": "string",
                        },
                    },
                    "type": "object",
                },
                "type": ["array", "null"],
            },
            "succeeded": {
                "items": {
                    "properties": {
                        "id": {
                            "description": "ID of the succeeded entity",
                            "type": "string",
                        },
                        "unarchived": {
                            "description": "Indicates whether the model was unarchived",
                            "type": "boolean",
                        },
                    },
                    "type": "object",
                },
                "type": ["array", "null"],
            },
        },
        "type": "object",
    }

    def __init__(
        self, succeeded: Optional[List[dict]] = None, failed: Optional[List[dict]] = None, **kwargs: Any
    ) -> None:
        super(UnarchiveManyResponse, self).__init__(**kwargs)
        self.succeeded = succeeded
        self.failed = failed

    @schema_property("succeeded")
    def succeeded(self) -> Optional[List[dict]]:
        return self._property_succeeded

    @succeeded.setter
    def succeeded(self, value: Optional[List[dict]]) -> None:
        if value is None:
            self._property_succeeded = None
            return
        self.assert_isinstance(value, "succeeded", (list, tuple))
        self.assert_isinstance(value, "succeeded", (dict,), is_array=True)
        self._property_succeeded = value

    @schema_property("failed")
    def failed(self) -> Optional[List[dict]]:
        return self._property_failed

    @failed.setter
    def failed(self, value: Optional[List[dict]]) -> None:
        if value is None:
            self._property_failed = None
            return
        self.assert_isinstance(value, "failed", (list, tuple))
        self.assert_isinstance(value, "failed", (dict,), is_array=True)
        self._property_failed = value


class UpdateRequest(Request):
    """
    Update a model

    :param model: Model id
    :type model: str
    :param name: Model name Unique within the company.
    :type name: str
    :param comment: Model comment
    :type comment: str
    :param tags: User-defined tags list
    :type tags: Sequence[str]
    :param system_tags: System tags list. This field is reserved for system use,
        please don't use it.
    :type system_tags: Sequence[str]
    :param ready: Indication if the model is final and can be used by other tasks
        Default is false.
    :type ready: bool
    :param created: Model creation time (UTC)
    :type created: datetime.datetime
    :param ui_cache: UI cache for this model
    :type ui_cache: dict
    :param project: Project to which to model belongs
    :type project: str
    :param task: Associated task ID
    :type task: str
    :param iteration: Iteration (used to update task statistics if an associated
        task is reported)
    :type iteration: int
    """

    _service = "models"
    _action = "update"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "comment": {"description": "Model comment", "type": "string"},
            "created": {
                "description": "Model creation time (UTC) ",
                "format": "date-time",
                "type": "string",
            },
            "iteration": {
                "description": "Iteration (used to update task statistics if an associated task is reported)",
                "type": "integer",
            },
            "model": {"description": "Model id", "type": "string"},
            "name": {
                "description": "Model name Unique within the company.",
                "type": "string",
            },
            "project": {
                "description": "Project to which to model belongs",
                "type": "string",
            },
            "ready": {
                "default": False,
                "description": "Indication if the model is final and can be used by other tasks Default is false.",
                "type": "boolean",
            },
            "system_tags": {
                "description": "System tags list. This field is reserved for system use, please don't use it.",
                "items": {"type": "string"},
                "type": "array",
            },
            "tags": {
                "description": "User-defined tags list",
                "items": {"type": "string"},
                "type": "array",
            },
            "task": {"description": "Associated task ID", "type": "string"},
            "ui_cache": {
                "additionalProperties": True,
                "description": "UI cache for this model",
                "type": "object",
            },
        },
        "required": ["model"],
        "type": "object",
    }

    def __init__(
        self,
        model: str,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        tags: Optional[List[str]] = None,
        system_tags: Optional[List[str]] = None,
        ready: Optional[bool] = False,
        created: Optional[str] = None,
        ui_cache: Optional[dict] = None,
        project: Optional[str] = None,
        task: Optional[str] = None,
        iteration: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        super(UpdateRequest, self).__init__(**kwargs)
        self.model = model
        self.name = name
        self.comment = comment
        self.tags = tags
        self.system_tags = system_tags
        self.ready = ready
        self.created = created
        self.ui_cache = ui_cache
        self.project = project
        self.task = task
        self.iteration = iteration

    @schema_property("model")
    def model(self) -> str:
        return self._property_model

    @model.setter
    def model(self, value: str) -> None:
        if value is None:
            self._property_model = None
            return
        self.assert_isinstance(value, "model", six.string_types)
        self._property_model = value

    @schema_property("name")
    def name(self) -> Optional[str]:
        return self._property_name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        if value is None:
            self._property_name = None
            return
        self.assert_isinstance(value, "name", six.string_types)
        self._property_name = value

    @schema_property("comment")
    def comment(self) -> Optional[str]:
        return self._property_comment

    @comment.setter
    def comment(self, value: Optional[str]) -> None:
        if value is None:
            self._property_comment = None
            return
        self.assert_isinstance(value, "comment", six.string_types)
        self._property_comment = value

    @schema_property("tags")
    def tags(self) -> Optional[List[str]]:
        return self._property_tags

    @tags.setter
    def tags(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_tags = None
            return
        self.assert_isinstance(value, "tags", (list, tuple))
        self.assert_isinstance(value, "tags", six.string_types, is_array=True)
        self._property_tags = value

    @schema_property("system_tags")
    def system_tags(self) -> Optional[List[str]]:
        return self._property_system_tags

    @system_tags.setter
    def system_tags(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_system_tags = None
            return
        self.assert_isinstance(value, "system_tags", (list, tuple))
        self.assert_isinstance(value, "system_tags", six.string_types, is_array=True)
        self._property_system_tags = value

    @schema_property("ready")
    def ready(self) -> Optional[bool]:
        return self._property_ready

    @ready.setter
    def ready(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_ready = None
            return
        self.assert_isinstance(value, "ready", (bool,))
        self._property_ready = value

    @schema_property("created")
    def created(self) -> Optional[str]:
        return self._property_created

    @created.setter
    def created(self, value: Optional[str]) -> None:
        if value is None:
            self._property_created = None
            return
        self.assert_isinstance(value, "created", six.string_types + (datetime,))
        if not isinstance(value, datetime):
            value = parse_datetime(value)
        self._property_created = value

    @schema_property("ui_cache")
    def ui_cache(self) -> Optional[dict]:
        return self._property_ui_cache

    @ui_cache.setter
    def ui_cache(self, value: Optional[dict]) -> None:
        if value is None:
            self._property_ui_cache = None
            return
        self.assert_isinstance(value, "ui_cache", (dict,))
        self._property_ui_cache = value

    @schema_property("project")
    def project(self) -> Optional[str]:
        return self._property_project

    @project.setter
    def project(self, value: Optional[str]) -> None:
        if value is None:
            self._property_project = None
            return
        self.assert_isinstance(value, "project", six.string_types)
        self._property_project = value

    @schema_property("task")
    def task(self) -> Optional[str]:
        return self._property_task

    @task.setter
    def task(self, value: Optional[str]) -> None:
        if value is None:
            self._property_task = None
            return
        self.assert_isinstance(value, "task", six.string_types)
        self._property_task = value

    @schema_property("iteration")
    def iteration(self) -> Optional[int]:
        return self._property_iteration

    @iteration.setter
    def iteration(self, value: Optional[int]) -> None:
        if value is None:
            self._property_iteration = None
            return
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        self.assert_isinstance(value, "iteration", six.integer_types)
        self._property_iteration = value


class UpdateResponse(Response):
    """
    Response of models.update endpoint.

    :param updated: Number of models updated (0 or 1)
    :type updated: int
    :param fields: Updated fields names and values
    :type fields: dict
    """

    _service = "models"
    _action = "update"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "fields": {
                "additionalProperties": True,
                "description": "Updated fields names and values",
                "type": ["object", "null"],
            },
            "updated": {
                "description": "Number of models updated (0 or 1)",
                "enum": [0, 1],
                "type": ["integer", "null"],
            },
        },
        "type": "object",
    }

    def __init__(self, updated: Optional[int] = None, fields: Optional[dict] = None, **kwargs: Any) -> None:
        super(UpdateResponse, self).__init__(**kwargs)
        self.updated = updated
        self.fields = fields

    @schema_property("updated")
    def updated(self) -> Optional[int]:
        return self._property_updated

    @updated.setter
    def updated(self, value: Optional[int]) -> None:
        if value is None:
            self._property_updated = None
            return
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        self.assert_isinstance(value, "updated", six.integer_types)
        self._property_updated = value

    @schema_property("fields")
    def fields(self) -> Optional[dict]:
        return self._property_fields

    @fields.setter
    def fields(self, value: Optional[dict]) -> None:
        if value is None:
            self._property_fields = None
            return
        self.assert_isinstance(value, "fields", (dict,))
        self._property_fields = value


class UpdateForTaskRequest(Request):
    """
    Create or update a new model for a task

    :param task: Task id
    :type task: str
    :param uri: URI for the model. Exactly one of uri or override_model_id is a
        required.
    :type uri: str
    :param name: Model name Unique within the company.
    :type name: str
    :param comment: Model comment
    :type comment: str
    :param tags: User-defined tags list
    :type tags: Sequence[str]
    :param system_tags: System tags list. This field is reserved for system use,
        please don't use it.
    :type system_tags: Sequence[str]
    :param override_model_id: Override model ID. If provided, this model is updated
        in the task. Exactly one of override_model_id or uri is required.
    :type override_model_id: str
    :param iteration: Iteration (used to update task statistics)
    :type iteration: int
    """

    _service = "models"
    _action = "update_for_task"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "comment": {"description": "Model comment", "type": "string"},
            "iteration": {
                "description": "Iteration (used to update task statistics)",
                "type": "integer",
            },
            "name": {
                "description": "Model name Unique within the company.",
                "type": "string",
            },
            "override_model_id": {
                "description": "Override model ID. If provided, this model is updated in the task. Exactly one of override_model_id or uri is required.",
                "type": "string",
            },
            "system_tags": {
                "description": "System tags list. This field is reserved for system use, please don't use it.",
                "items": {"type": "string"},
                "type": "array",
            },
            "tags": {
                "description": "User-defined tags list",
                "items": {"type": "string"},
                "type": "array",
            },
            "task": {"description": "Task id", "type": "string"},
            "uri": {
                "description": "URI for the model. Exactly one of uri or override_model_id is a required.",
                "type": "string",
            },
        },
        "required": ["task"],
        "type": "object",
    }

    def __init__(
        self,
        task: str,
        uri: Optional[str] = None,
        name: Optional[str] = None,
        comment: Optional[str] = None,
        tags: Optional[List[str]] = None,
        system_tags: Optional[List[str]] = None,
        override_model_id: Optional[str] = None,
        iteration: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        super(UpdateForTaskRequest, self).__init__(**kwargs)
        self.task = task
        self.uri = uri
        self.name = name
        self.comment = comment
        self.tags = tags
        self.system_tags = system_tags
        self.override_model_id = override_model_id
        self.iteration = iteration

    @schema_property("task")
    def task(self) -> str:
        return self._property_task

    @task.setter
    def task(self, value: str) -> None:
        if value is None:
            self._property_task = None
            return
        self.assert_isinstance(value, "task", six.string_types)
        self._property_task = value

    @schema_property("uri")
    def uri(self) -> Optional[str]:
        return self._property_uri

    @uri.setter
    def uri(self, value: Optional[str]) -> None:
        if value is None:
            self._property_uri = None
            return
        self.assert_isinstance(value, "uri", six.string_types)
        self._property_uri = value

    @schema_property("name")
    def name(self) -> Optional[str]:
        return self._property_name

    @name.setter
    def name(self, value: Optional[str]) -> None:
        if value is None:
            self._property_name = None
            return
        self.assert_isinstance(value, "name", six.string_types)
        self._property_name = value

    @schema_property("comment")
    def comment(self) -> Optional[str]:
        return self._property_comment

    @comment.setter
    def comment(self, value: Optional[str]) -> None:
        if value is None:
            self._property_comment = None
            return
        self.assert_isinstance(value, "comment", six.string_types)
        self._property_comment = value

    @schema_property("tags")
    def tags(self) -> Optional[List[str]]:
        return self._property_tags

    @tags.setter
    def tags(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_tags = None
            return
        self.assert_isinstance(value, "tags", (list, tuple))
        self.assert_isinstance(value, "tags", six.string_types, is_array=True)
        self._property_tags = value

    @schema_property("system_tags")
    def system_tags(self) -> Optional[List[str]]:
        return self._property_system_tags

    @system_tags.setter
    def system_tags(self, value: Optional[List[str]]) -> None:
        if value is None:
            self._property_system_tags = None
            return
        self.assert_isinstance(value, "system_tags", (list, tuple))
        self.assert_isinstance(value, "system_tags", six.string_types, is_array=True)
        self._property_system_tags = value

    @schema_property("override_model_id")
    def override_model_id(self) -> Optional[str]:
        return self._property_override_model_id

    @override_model_id.setter
    def override_model_id(self, value: Optional[str]) -> None:
        if value is None:
            self._property_override_model_id = None
            return
        self.assert_isinstance(value, "override_model_id", six.string_types)
        self._property_override_model_id = value

    @schema_property("iteration")
    def iteration(self) -> Optional[int]:
        return self._property_iteration

    @iteration.setter
    def iteration(self, value: Optional[int]) -> None:
        if value is None:
            self._property_iteration = None
            return
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        self.assert_isinstance(value, "iteration", six.integer_types)
        self._property_iteration = value


class UpdateForTaskResponse(Response):
    """
    Response of models.update_for_task endpoint.

    :param id: ID of the model
    :type id: str
    :param created: Was the model created
    :type created: bool
    :param updated: Number of models updated (0 or 1)
    :type updated: int
    :param fields: Updated fields names and values
    :type fields: dict
    """

    _service = "models"
    _action = "update_for_task"
    _version = "2.23"
    _schema = {
        "definitions": {},
        "properties": {
            "created": {
                "description": "Was the model created",
                "type": ["boolean", "null"],
            },
            "fields": {
                "additionalProperties": True,
                "description": "Updated fields names and values",
                "type": ["object", "null"],
            },
            "id": {"description": "ID of the model", "type": ["string", "null"]},
            "updated": {
                "description": "Number of models updated (0 or 1)",
                "type": ["integer", "null"],
            },
        },
        "type": "object",
    }

    def __init__(
        self,
        id: Optional[str] = None,
        created: Optional[bool] = None,
        updated: Optional[int] = None,
        fields: Optional[dict] = None,
        **kwargs: Any
    ) -> None:
        super(UpdateForTaskResponse, self).__init__(**kwargs)
        self.id = id
        self.created = created
        self.updated = updated
        self.fields = fields

    @schema_property("id")
    def id(self) -> Optional[str]:
        return self._property_id

    @id.setter
    def id(self, value: Optional[str]) -> None:
        if value is None:
            self._property_id = None
            return
        self.assert_isinstance(value, "id", six.string_types)
        self._property_id = value

    @schema_property("created")
    def created(self) -> Optional[bool]:
        return self._property_created

    @created.setter
    def created(self, value: Optional[bool]) -> None:
        if value is None:
            self._property_created = None
            return
        self.assert_isinstance(value, "created", (bool,))
        self._property_created = value

    @schema_property("updated")
    def updated(self) -> Optional[int]:
        return self._property_updated

    @updated.setter
    def updated(self, value: Optional[int]) -> None:
        if value is None:
            self._property_updated = None
            return
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        self.assert_isinstance(value, "updated", six.integer_types)
        self._property_updated = value

    @schema_property("fields")
    def fields(self) -> Optional[dict]:
        return self._property_fields

    @fields.setter
    def fields(self, value: Optional[dict]) -> None:
        if value is None:
            self._property_fields = None
            return
        self.assert_isinstance(value, "fields", (dict,))
        self._property_fields = value


response_mapping = {
    GetByIdRequest: GetByIdResponse,
    GetByTaskIdRequest: GetByTaskIdResponse,
    GetAllRequest: GetAllResponse,
    GetFrameworksRequest: GetFrameworksResponse,
    UpdateForTaskRequest: UpdateForTaskResponse,
    CreateRequest: CreateResponse,
    EditRequest: EditResponse,
    UpdateRequest: UpdateResponse,
    PublishManyRequest: PublishManyResponse,
    SetReadyRequest: SetReadyResponse,
    ArchiveManyRequest: ArchiveManyResponse,
    UnarchiveManyRequest: UnarchiveManyResponse,
    DeleteManyRequest: DeleteManyResponse,
    DeleteRequest: DeleteResponse,
    MakePublicRequest: MakePublicResponse,
    MakePrivateRequest: MakePrivateResponse,
    MoveRequest: MoveResponse,
    AddOrUpdateMetadataRequest: AddOrUpdateMetadataResponse,
    DeleteMetadataRequest: DeleteMetadataResponse,
}
