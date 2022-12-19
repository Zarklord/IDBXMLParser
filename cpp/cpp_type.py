from .cpp_base import cpp_base
from .lookups import set_cpp_obj_for_datatype

class cpp_type_def(cpp_base):
    def __init__(self, name, size, ghidra_namespace):
        self.cpp_name = name
        self.ghidra_namespace = ghidra_namespace
        self.size = size

        set_cpp_obj_for_datatype(self, name)

    def data_size(self):
        return self.size