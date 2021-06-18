"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import monocle.task_data_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class SearchSuggestionsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    INDEX_FIELD_NUMBER: builtins.int
    index: typing.Text = ...
    def __init__(
        self,
        *,
        index: typing.Text = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["index", b"index"]
    ) -> None: ...

global___SearchSuggestionsRequest = SearchSuggestionsRequest

class SearchSuggestionsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    TASK_TYPES_FIELD_NUMBER: builtins.int
    AUTHORS_FIELD_NUMBER: builtins.int
    APPROVALS_FIELD_NUMBER: builtins.int
    PRIORITIES_FIELD_NUMBER: builtins.int
    SEVERITIES_FIELD_NUMBER: builtins.int
    task_types: google.protobuf.internal.containers.RepeatedScalarFieldContainer[
        typing.Text
    ] = ...
    authors: google.protobuf.internal.containers.RepeatedScalarFieldContainer[
        typing.Text
    ] = ...
    approvals: google.protobuf.internal.containers.RepeatedScalarFieldContainer[
        typing.Text
    ] = ...
    priorities: google.protobuf.internal.containers.RepeatedScalarFieldContainer[
        typing.Text
    ] = ...
    severities: google.protobuf.internal.containers.RepeatedScalarFieldContainer[
        typing.Text
    ] = ...
    def __init__(
        self,
        *,
        task_types: typing.Optional[typing.Iterable[typing.Text]] = ...,
        authors: typing.Optional[typing.Iterable[typing.Text]] = ...,
        approvals: typing.Optional[typing.Iterable[typing.Text]] = ...,
        priorities: typing.Optional[typing.Iterable[typing.Text]] = ...,
        severities: typing.Optional[typing.Iterable[typing.Text]] = ...,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "approvals",
            b"approvals",
            "authors",
            b"authors",
            "priorities",
            b"priorities",
            "severities",
            b"severities",
            "task_types",
            b"task_types",
        ],
    ) -> None: ...

global___SearchSuggestionsResponse = SearchSuggestionsResponse

class FieldsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    VERSION_FIELD_NUMBER: builtins.int
    version: typing.Text = ...
    def __init__(
        self,
        *,
        version: typing.Text = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["version", b"version"]
    ) -> None: ...

global___FieldsRequest = FieldsRequest

class Field(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class _Type(
        google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Type.V],
        builtins.type,
    ):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
        FIELD_DATE = Field.Type.V(0)
        FIELD_NUMBER = Field.Type.V(1)
        FIELD_TEXT = Field.Type.V(2)
        FIELD_BOOL = Field.Type.V(3)
        FIELD_REGEX = Field.Type.V(4)
    class Type(metaclass=_Type):
        V = typing.NewType("V", builtins.int)
    FIELD_DATE = Field.Type.V(0)
    FIELD_NUMBER = Field.Type.V(1)
    FIELD_TEXT = Field.Type.V(2)
    FIELD_BOOL = Field.Type.V(3)
    FIELD_REGEX = Field.Type.V(4)

    NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    name: typing.Text = ...
    description: typing.Text = ...
    type: global___Field.Type.V = ...
    def __init__(
        self,
        *,
        name: typing.Text = ...,
        description: typing.Text = ...,
        type: global___Field.Type.V = ...,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "description", b"description", "name", b"name", "type", b"type"
        ],
    ) -> None: ...

global___Field = Field

class FieldsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    FIELDS_FIELD_NUMBER: builtins.int
    @property
    def fields(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___Field
    ]: ...
    def __init__(
        self,
        *,
        fields: typing.Optional[typing.Iterable[global___Field]] = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["fields", b"fields"]
    ) -> None: ...

global___FieldsResponse = FieldsResponse

class QueryError(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    MESSAGE_FIELD_NUMBER: builtins.int
    POSITION_FIELD_NUMBER: builtins.int
    message: typing.Text = ...
    position: builtins.int = ...
    def __init__(
        self,
        *,
        message: typing.Text = ...,
        position: builtins.int = ...,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "message", b"message", "position", b"position"
        ],
    ) -> None: ...

global___QueryError = QueryError

class QueryRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    INDEX_FIELD_NUMBER: builtins.int
    QUERY_FIELD_NUMBER: builtins.int
    index: typing.Text = ...
    query: typing.Text = ...
    def __init__(
        self,
        *,
        index: typing.Text = ...,
        query: typing.Text = ...,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal["index", b"index", "query", b"query"],
    ) -> None: ...

global___QueryRequest = QueryRequest

class File(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ADDITIONS_FIELD_NUMBER: builtins.int
    DELETIONS_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    additions: builtins.int = ...
    deletions: builtins.int = ...
    path: typing.Text = ...
    def __init__(
        self,
        *,
        additions: builtins.int = ...,
        deletions: builtins.int = ...,
        path: typing.Text = ...,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "additions", b"additions", "deletions", b"deletions", "path", b"path"
        ],
    ) -> None: ...

global___File = File

class Commit(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    SHA_FIELD_NUMBER: builtins.int
    TITLE_FIELD_NUMBER: builtins.int
    AUTHOR_FIELD_NUMBER: builtins.int
    AUTHORED_AT_FIELD_NUMBER: builtins.int
    COMMITTER_FIELD_NUMBER: builtins.int
    COMMITTED_AT_FIELD_NUMBER: builtins.int
    ADDITIONS_FIELD_NUMBER: builtins.int
    DELETIONS_FIELD_NUMBER: builtins.int
    sha: typing.Text = ...
    title: typing.Text = ...
    author: typing.Text = ...
    committer: typing.Text = ...
    additions: builtins.int = ...
    deletions: builtins.int = ...
    @property
    def authored_at(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    @property
    def committed_at(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    def __init__(
        self,
        *,
        sha: typing.Text = ...,
        title: typing.Text = ...,
        author: typing.Text = ...,
        authored_at: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        committer: typing.Text = ...,
        committed_at: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        additions: builtins.int = ...,
        deletions: builtins.int = ...,
    ) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions.Literal[
            "authored_at", b"authored_at", "committed_at", b"committed_at"
        ],
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "additions",
            b"additions",
            "author",
            b"author",
            "authored_at",
            b"authored_at",
            "committed_at",
            b"committed_at",
            "committer",
            b"committer",
            "deletions",
            b"deletions",
            "sha",
            b"sha",
            "title",
            b"title",
        ],
    ) -> None: ...

global___Commit = Commit

class Change(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    CHANGE_ID_FIELD_NUMBER: builtins.int
    AUTHOR_FIELD_NUMBER: builtins.int
    TITLE_FIELD_NUMBER: builtins.int
    URL_FIELD_NUMBER: builtins.int
    REPOSITORY_FULLNAME_FIELD_NUMBER: builtins.int
    STATE_FIELD_NUMBER: builtins.int
    BRANCH_FIELD_NUMBER: builtins.int
    TARGET_BRANCH_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    UPDATED_AT_FIELD_NUMBER: builtins.int
    MERGED_AT_FIELD_NUMBER: builtins.int
    MERGED_BY_FIELD_NUMBER: builtins.int
    TEXT_FIELD_NUMBER: builtins.int
    ADDITIONS_FIELD_NUMBER: builtins.int
    DELETIONS_FIELD_NUMBER: builtins.int
    APPROVAL_FIELD_NUMBER: builtins.int
    ASSIGNEES_FIELD_NUMBER: builtins.int
    LABELS_FIELD_NUMBER: builtins.int
    DRAFT_FIELD_NUMBER: builtins.int
    MERGEABLE_FIELD_NUMBER: builtins.int
    CHANGED_FILES_FIELD_NUMBER: builtins.int
    CHANGED_FILES_COUNT_FIELD_NUMBER: builtins.int
    COMMITS_FIELD_NUMBER: builtins.int
    COMMITS_COUNT_FIELD_NUMBER: builtins.int
    TASK_DATA_FIELD_NUMBER: builtins.int
    change_id: typing.Text = ...
    author: typing.Text = ...
    title: typing.Text = ...
    url: typing.Text = ...
    repository_fullname: typing.Text = ...
    state: typing.Text = ...
    branch: typing.Text = ...
    target_branch: typing.Text = ...
    merged_by: typing.Text = ...
    text: typing.Text = ...
    additions: builtins.int = ...
    deletions: builtins.int = ...
    approval: google.protobuf.internal.containers.RepeatedScalarFieldContainer[
        typing.Text
    ] = ...
    assignees: google.protobuf.internal.containers.RepeatedScalarFieldContainer[
        typing.Text
    ] = ...
    labels: google.protobuf.internal.containers.RepeatedScalarFieldContainer[
        typing.Text
    ] = ...
    draft: builtins.bool = ...
    mergeable: builtins.bool = ...
    changed_files_count: builtins.int = ...
    commits_count: builtins.int = ...
    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    @property
    def updated_at(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    @property
    def merged_at(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    @property
    def changed_files(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___File
    ]: ...
    @property
    def commits(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___Commit
    ]: ...
    @property
    def task_data(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        monocle.task_data_pb2.TaskData
    ]: ...
    def __init__(
        self,
        *,
        change_id: typing.Text = ...,
        author: typing.Text = ...,
        title: typing.Text = ...,
        url: typing.Text = ...,
        repository_fullname: typing.Text = ...,
        state: typing.Text = ...,
        branch: typing.Text = ...,
        target_branch: typing.Text = ...,
        created_at: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        updated_at: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        merged_at: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        merged_by: typing.Text = ...,
        text: typing.Text = ...,
        additions: builtins.int = ...,
        deletions: builtins.int = ...,
        approval: typing.Optional[typing.Iterable[typing.Text]] = ...,
        assignees: typing.Optional[typing.Iterable[typing.Text]] = ...,
        labels: typing.Optional[typing.Iterable[typing.Text]] = ...,
        draft: builtins.bool = ...,
        mergeable: builtins.bool = ...,
        changed_files: typing.Optional[typing.Iterable[global___File]] = ...,
        changed_files_count: builtins.int = ...,
        commits: typing.Optional[typing.Iterable[global___Commit]] = ...,
        commits_count: builtins.int = ...,
        task_data: typing.Optional[
            typing.Iterable[monocle.task_data_pb2.TaskData]
        ] = ...,
    ) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions.Literal[
            "created_at",
            b"created_at",
            "merged_at",
            b"merged_at",
            "merged_by",
            b"merged_by",
            "merged_byM",
            b"merged_byM",
            "updated_at",
            b"updated_at",
        ],
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "additions",
            b"additions",
            "approval",
            b"approval",
            "assignees",
            b"assignees",
            "author",
            b"author",
            "branch",
            b"branch",
            "change_id",
            b"change_id",
            "changed_files",
            b"changed_files",
            "changed_files_count",
            b"changed_files_count",
            "commits",
            b"commits",
            "commits_count",
            b"commits_count",
            "created_at",
            b"created_at",
            "deletions",
            b"deletions",
            "draft",
            b"draft",
            "labels",
            b"labels",
            "mergeable",
            b"mergeable",
            "merged_at",
            b"merged_at",
            "merged_by",
            b"merged_by",
            "merged_byM",
            b"merged_byM",
            "repository_fullname",
            b"repository_fullname",
            "state",
            b"state",
            "target_branch",
            b"target_branch",
            "task_data",
            b"task_data",
            "text",
            b"text",
            "title",
            b"title",
            "updated_at",
            b"updated_at",
            "url",
            b"url",
        ],
    ) -> None: ...
    def WhichOneof(
        self, oneof_group: typing_extensions.Literal["merged_byM", b"merged_byM"]
    ) -> typing_extensions.Literal["merged_by"]: ...

global___Change = Change

class Changes(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    CHANGES_FIELD_NUMBER: builtins.int
    @property
    def changes(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___Change
    ]: ...
    def __init__(
        self,
        *,
        changes: typing.Optional[typing.Iterable[global___Change]] = ...,
    ) -> None: ...
    def ClearField(
        self, field_name: typing_extensions.Literal["changes", b"changes"]
    ) -> None: ...

global___Changes = Changes

class QueryResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ERROR_FIELD_NUMBER: builtins.int
    ITEMS_FIELD_NUMBER: builtins.int
    @property
    def error(self) -> global___QueryError: ...
    @property
    def items(self) -> global___Changes: ...
    def __init__(
        self,
        *,
        error: typing.Optional[global___QueryError] = ...,
        items: typing.Optional[global___Changes] = ...,
    ) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions.Literal[
            "error", b"error", "items", b"items", "result", b"result"
        ],
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "error", b"error", "items", b"items", "result", b"result"
        ],
    ) -> None: ...
    def WhichOneof(
        self, oneof_group: typing_extensions.Literal["result", b"result"]
    ) -> typing_extensions.Literal["error", "items"]: ...

global___QueryResponse = QueryResponse

class ChangesHistos(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class Event(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        DOC_COUNT_FIELD_NUMBER: builtins.int
        KEY_FIELD_NUMBER: builtins.int
        KEY_AS_STRING_FIELD_NUMBER: builtins.int
        doc_count: builtins.int = ...
        key: builtins.int = ...
        key_as_string: typing.Text = ...
        def __init__(
            self,
            *,
            doc_count: builtins.int = ...,
            key: builtins.int = ...,
            key_as_string: typing.Text = ...,
        ) -> None: ...
        def ClearField(
            self,
            field_name: typing_extensions.Literal[
                "doc_count",
                b"doc_count",
                "key",
                b"key",
                "key_as_string",
                b"key_as_string",
            ],
        ) -> None: ...
    CHANGEABANDONEDEVENT_FIELD_NUMBER: builtins.int
    CHANGECOMMITFORCEPUSHEDEVENT_FIELD_NUMBER: builtins.int
    CHANGECOMMITPUSHEDEVENT_FIELD_NUMBER: builtins.int
    CHANGECREATEDEVENT_FIELD_NUMBER: builtins.int
    CHANGEMERGEDEVENT_FIELD_NUMBER: builtins.int
    @property
    def ChangeAbandonedEvent(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___ChangesHistos.Event
    ]: ...
    @property
    def ChangeCommitForcePushedEvent(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___ChangesHistos.Event
    ]: ...
    @property
    def ChangeCommitPushedEvent(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___ChangesHistos.Event
    ]: ...
    @property
    def ChangeCreatedEvent(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___ChangesHistos.Event
    ]: ...
    @property
    def ChangeMergedEvent(
        self,
    ) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[
        global___ChangesHistos.Event
    ]: ...
    def __init__(
        self,
        *,
        ChangeAbandonedEvent: typing.Optional[
            typing.Iterable[global___ChangesHistos.Event]
        ] = ...,
        ChangeCommitForcePushedEvent: typing.Optional[
            typing.Iterable[global___ChangesHistos.Event]
        ] = ...,
        ChangeCommitPushedEvent: typing.Optional[
            typing.Iterable[global___ChangesHistos.Event]
        ] = ...,
        ChangeCreatedEvent: typing.Optional[
            typing.Iterable[global___ChangesHistos.Event]
        ] = ...,
        ChangeMergedEvent: typing.Optional[
            typing.Iterable[global___ChangesHistos.Event]
        ] = ...,
    ) -> None: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "ChangeAbandonedEvent",
            b"ChangeAbandonedEvent",
            "ChangeCommitForcePushedEvent",
            b"ChangeCommitForcePushedEvent",
            "ChangeCommitPushedEvent",
            b"ChangeCommitPushedEvent",
            "ChangeCreatedEvent",
            b"ChangeCreatedEvent",
            "ChangeMergedEvent",
            b"ChangeMergedEvent",
        ],
    ) -> None: ...

global___ChangesHistos = ChangesHistos

class ChangesLifecycle(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class Event(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        AUTHORS_COUNT_FIELD_NUMBER: builtins.int
        EVENTS_COUNT_FIELD_NUMBER: builtins.int
        authors_count: builtins.int = ...
        events_count: builtins.int = ...
        def __init__(
            self,
            *,
            authors_count: builtins.int = ...,
            events_count: builtins.int = ...,
        ) -> None: ...
        def ClearField(
            self,
            field_name: typing_extensions.Literal[
                "authors_count", b"authors_count", "events_count", b"events_count"
            ],
        ) -> None: ...
    class Ratios(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        ABANDONED_FIELD_NUMBER: builtins.int
        ITERATIONS_FIELD_NUMBER: builtins.int
        MERGED_FIELD_NUMBER: builtins.int
        SELF_MERGED_FIELD_NUMBER: builtins.int
        abandoned: builtins.float = ...
        iterations: builtins.float = ...
        merged: builtins.float = ...
        self_merged: builtins.float = ...
        def __init__(
            self,
            *,
            abandoned: builtins.float = ...,
            iterations: builtins.float = ...,
            merged: builtins.float = ...,
            self_merged: builtins.float = ...,
        ) -> None: ...
        def ClearField(
            self,
            field_name: typing_extensions.Literal[
                "abandoned",
                b"abandoned",
                "iterations",
                b"iterations",
                "merged",
                b"merged",
                "self_merged",
                b"self_merged",
            ],
        ) -> None: ...
    CHANGECOMMITFORCEPUSHEDEVENT_FIELD_NUMBER: builtins.int
    CHANGECOMMITPUSHEDEVENT_FIELD_NUMBER: builtins.int
    CHANGECREATEDEVENT_FIELD_NUMBER: builtins.int
    ABANDONED_FIELD_NUMBER: builtins.int
    COMMITS_FIELD_NUMBER: builtins.int
    DURATION_FIELD_NUMBER: builtins.int
    DURATION_VARIABILITY_FIELD_NUMBER: builtins.int
    HISTOS_FIELD_NUMBER: builtins.int
    MERGED_FIELD_NUMBER: builtins.int
    OPENED_FIELD_NUMBER: builtins.int
    RATIOS_FIELD_NUMBER: builtins.int
    SELF_MERGED_FIELD_NUMBER: builtins.int
    TESTS_FIELD_NUMBER: builtins.int
    abandoned: builtins.int = ...
    commits: builtins.float = ...
    duration: builtins.float = ...
    duration_variability: builtins.float = ...
    merged: builtins.int = ...
    opened: builtins.int = ...
    self_merged: builtins.int = ...
    tests: builtins.float = ...
    @property
    def ChangeCommitForcePushedEvent(self) -> global___ChangesLifecycle.Event: ...
    @property
    def ChangeCommitPushedEvent(self) -> global___ChangesLifecycle.Event: ...
    @property
    def ChangeCreatedEvent(self) -> global___ChangesLifecycle.Event: ...
    @property
    def histos(self) -> global___ChangesHistos: ...
    @property
    def ratios(self) -> global___ChangesLifecycle.Ratios: ...
    def __init__(
        self,
        *,
        ChangeCommitForcePushedEvent: typing.Optional[
            global___ChangesLifecycle.Event
        ] = ...,
        ChangeCommitPushedEvent: typing.Optional[global___ChangesLifecycle.Event] = ...,
        ChangeCreatedEvent: typing.Optional[global___ChangesLifecycle.Event] = ...,
        abandoned: builtins.int = ...,
        commits: builtins.float = ...,
        duration: builtins.float = ...,
        duration_variability: builtins.float = ...,
        histos: typing.Optional[global___ChangesHistos] = ...,
        merged: builtins.int = ...,
        opened: builtins.int = ...,
        ratios: typing.Optional[global___ChangesLifecycle.Ratios] = ...,
        self_merged: builtins.int = ...,
        tests: builtins.float = ...,
    ) -> None: ...
    def HasField(
        self,
        field_name: typing_extensions.Literal[
            "ChangeCommitForcePushedEvent",
            b"ChangeCommitForcePushedEvent",
            "ChangeCommitPushedEvent",
            b"ChangeCommitPushedEvent",
            "ChangeCreatedEvent",
            b"ChangeCreatedEvent",
            "histos",
            b"histos",
            "ratios",
            b"ratios",
        ],
    ) -> builtins.bool: ...
    def ClearField(
        self,
        field_name: typing_extensions.Literal[
            "ChangeCommitForcePushedEvent",
            b"ChangeCommitForcePushedEvent",
            "ChangeCommitPushedEvent",
            b"ChangeCommitPushedEvent",
            "ChangeCreatedEvent",
            b"ChangeCreatedEvent",
            "abandoned",
            b"abandoned",
            "commits",
            b"commits",
            "duration",
            b"duration",
            "duration_variability",
            b"duration_variability",
            "histos",
            b"histos",
            "merged",
            b"merged",
            "opened",
            b"opened",
            "ratios",
            b"ratios",
            "self_merged",
            b"self_merged",
            "tests",
            b"tests",
        ],
    ) -> None: ...

global___ChangesLifecycle = ChangesLifecycle