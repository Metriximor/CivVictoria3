from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString
from ruamel.yaml.compat import StringIO

class MyYAML(YAML):
    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()

yaml = MyYAML(typ="rt")
yaml.default_flow_style = False
yaml.width = 999999999 # type: ignore

def dq(str: str) -> DoubleQuotedScalarString:
    return DoubleQuotedScalarString(str)

def dumps(data) -> str:
    yaml_str = yaml.dump(data)
    match yaml_str:
        case None:
            return ""
        case _:
            return yaml_str