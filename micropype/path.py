import os.path as op
import re
from typing import Any, List
import inspect
from xml.dom import minidom
from glob import glob


MAX_PATH_PROCESS_DEPTH = 5


def find_one_file_or_get_none(path):
    items = glob(path)
    if items and len(items) > 0:
        return items[0]
    return None

class Paths(object):
    """
        Object to centralize all files paths
        This class aims to be extended by other classes which could initiliaze paths in __init__()

        Paths are constants defined in the class (every attributes not starting by "_")
    """
    # Params are used when calling a path to replace values in {}
    # /my/{toto} => /my/path if param['toto'] = "path"
    params = {}
    read_only = True

    def __init__(self, read_only=True) -> None:
        self.read_only = read_only

    def _get_path_names(self) -> List[str]:
        return [attr for attr in dir(self) if not attr.startswith("_")]
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if not __name in ["read_only", "params"] and hasattr(self, __name) and hasattr(self, "read_only") and self.read_only:
            raise IOError(f'Cannot overwrite "{__name}" as it is already defined and paths are readonly. It\'s advised to use new variable rather than trying to modify those paths.')
        return super().__setattr__(__name, __value)
    
    def __getattribute__(self, __name: str) -> Any:
        if __name.startswith("_"):
            return super().__getattribute__(__name)
        caller = inspect.stack()[1].frame.f_locals.get('self', None)
        if caller is self or not __name in self._get_path_names():
            return super().__getattribute__(__name)
        
        path = self.__getattribute__(__name)

        if callable(path):
            def executable_path(*arg, **kwargs):
                # FIXME: need more testing of this
                return self._get_path_instance(path(*arg, **kwargs))
            return executable_path
        return self._get_path_instance(path)
    
    def _get_path_instance(self, path: str) -> str:
        """ Convert path template to path replacing variable name by their values.

            When a "*" is in the path, it return only the first item matching the path
            or None if there is no result from glob()
        """
    
        # Replace all inner brackets values of the path by the values defined in self.params
        # The first loop allow nested {}, usefull if a params value contains brackets
        ret_path = path
        path_has_changed = True
        for depth in range(MAX_PATH_PROCESS_DEPTH):
            if not path_has_changed or not '{' in ret_path:
                break
            path_has_changed = False

            # Extract all the values contained in brakets
            needed_param_keys = re.findall(r'\{([^}]*)\}', ret_path)
            for needed_key in needed_param_keys:
                if not needed_key in self.params.keys():
                    raise ValueError(f'"{needed_key} parameter is not defined. Requested in path: "{path}"')
                ret_path = ret_path.replace('{' + needed_key +'}', self.params[needed_key])
                path_has_changed = True
        if depth == MAX_PATH_PROCESS_DEPTH-1:
            raise RuntimeError(f'Maximum path update iteration reached ({MAX_PATH_PROCESS_DEPTH}) for path "{path}".')

        if "*" in ret_path:
            res = glob(ret_path)
            if len(res) > 0:
                ret_path = res[0]
        return ret_path
