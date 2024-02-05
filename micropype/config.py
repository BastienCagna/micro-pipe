from warnings import warn
import yaml
from .utils import MessageIntent, cprint


def read_annotations(cls):
    """ 
        Parameters
        ==========
    
    """
    attributes = {}
    for attr, attr_type in cls.__annotations__.items():
        default = cls.__getattribute__(cls, attr) if hasattr(cls, attr) else None
        t = attr_type.__name__
        attributes[attr] = (t, default)
    return attributes



class Config:
    def __init__(self, yaml_f=None, **kwargs) -> None:
        if yaml_f is not None:
            raise NotImplementedError()
            # TODO: overide kwargs with yaml values (do it also in chlids)
            cfg = yaml.load(open(yaml_f, 'r'))

        attributes = read_annotations(self.__class__)

        used_kwargs = 0 
        for attr_name, (attr_t, default_v) in attributes.items():
            useDefault = not attr_name in kwargs
            if not useDefault:
                used_kwargs += 1
            isASubClass = attr_t in globals() and isinstance(globals()[attr_t], type)

            if isASubClass:
                value = globals()[attr_t]() if useDefault else globals()[attr_t](**kwargs[attr_name])
            else:
                value = default_v if useDefault else kwargs[attr_name]
            self.__setattr__(attr_name, value)
        if used_kwargs < len(kwargs.keys()):
            for k in kwargs.keys():
                if not k in attributes.keys():
                    cprint(
                        f'"{k}" is not an attribute of {self.__class__.__name__}. Skipping this setting.',
                        intent=MessageIntent.WARNING
                    )
                    continue
                

# if __name__ == "__main__":
#     class SubConfig(Config):
#         name:   str = "Albert"
#         age:    float
#     class AConfig(Config):
#         num:        float = .3
#         foo:        dict
#         subject:    SubConfig

#     conf = {
#         "paul": "jeje",
#         "foo": {"item1": 0.1, "item2": 0.2},
#         "subject": {
#             "name": "ciceron",
#             "age":  12
#         }
#     }

#     config = AConfig(**conf)
#     pass
