import json
from typing import Optional, IO

from .core import SerializationFormat, SerializationDecodeError
from .exceptiones import ConfigFileException

ROOT_NODE_FUNC_NAME_SET: set = {'dict', 'dump', 'dumps', 'load', 'loads'}


class Node:
    _is_node: bool = True
    _is_root_node: bool = False


class Root(Node):
    _is_root_node: bool = True
    _file = None

    _serialization_format: SerializationFormat = SerializationFormat.JSON

    def __init__(
        self,
        file: Optional[str] = None,
        serialization: SerializationFormat = None,
    ):
        if serialization is not None:
            self._serialization_format = serialization
        if file is not None:
            self._file = file

    def dict(self) -> dict:
        return convert_object2dict(self)

    def dumps(self, serialization: SerializationFormat = None) -> str:
        if serialization is None:
            serialization = self._serialization_format

        if serialization == SerializationFormat.TOML:
            import toml

            s = toml.dumps(self.dict())

        else:
            s = json.dumps(self.dict(), indent=2)

        return s

    def dump(
        self, fp: IO = None, serialization: SerializationFormat = None
    ) -> int:
        if serialization is None:
            serialization = self._serialization_format

        s = self.dumps(serialization)

        if fp is None:
            close_fp_before_return = True
            try:
                fp = open(self._file, 'w')
            except FileNotFoundError as e:
                raise ConfigFileException(e)

        else:
            close_fp_before_return = False

        ret = fp.write(s)

        if close_fp_before_return:
            fp.close()
        return ret

    def loads(self, s: str, serialization: SerializationFormat = None) -> None:
        if serialization is None:
            serialization = self._serialization_format

        if serialization == SerializationFormat.TOML:
            import toml

            try:
                obj = toml.loads(s)

            except toml.TomlDecodeError as e:
                raise SerializationDecodeError(e)

        else:
            try:
                obj = json.loads(s)

            except json.JSONDecodeError as e:
                raise SerializationDecodeError(e)

        convert_dict2obj(obj, self)
        return

    def load(
        self, fp: IO = None, serialization: SerializationFormat = None
    ) -> None:
        if serialization is None:
            serialization = self._serialization_format

        if fp is None:
            close_fp_before_return = True
            try:
                fp = open(self._file)
            except FileNotFoundError as e:
                raise ConfigFileException(e)
        else:
            close_fp_before_return = False

        s = fp.read()
        if close_fp_before_return:
            fp.close()

        self.loads(s, serialization)
        return


class Branch(Node):
    pass


class OtherNode(Node):
    """comment or other special node"""
    # TODO
    pass


def convert_object2dict(cls: object) -> Optional[dict]:
    try:
        getattr(cls, '_is_node')
    except AttributeError:
        return None

    is_root_node = getattr(cls, '_is_root_node')

    d = {}
    for attr_name in dir(cls):
        if attr_name[:1] == '_':
            continue

        if is_root_node and attr_name in ROOT_NODE_FUNC_NAME_SET:
            continue

        attr_obj = getattr(cls, attr_name)
        if isinstance(attr_obj, type(Branch)):
            d[attr_name] = convert_object2dict(attr_obj)

        elif isinstance(attr_obj, type(Node)):
            # skip other node type
            continue

        else:
            # found config item
            # TODO: type check by typing hint
            d[attr_name] = attr_obj

    return d


def convert_dict2obj(d: dict, cls: object) -> None:
    if d is None:
        return

    try:
        getattr(cls, '_is_node')
    except AttributeError:
        return

    is_root_node = getattr(cls, '_is_root_node')

    for attr_name in dir(cls):
        if attr_name[0] == '_':
            continue

        if is_root_node and attr_name in ROOT_NODE_FUNC_NAME_SET:
            continue

        attr_obj = getattr(cls, attr_name)
        if isinstance(attr_obj, type(Branch)):
            convert_dict2obj(d.get(attr_name), attr_obj)

        elif isinstance(attr_obj, type(Node)):
            # skip other node type
            continue

        elif attr_name in d:
            # found new item value in dict object
            # TODO: typing hint
            setattr(cls, attr_name, d[attr_name])
            continue

        # item not in dict object
        # skip update item

    return
