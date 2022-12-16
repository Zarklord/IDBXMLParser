from .cpp_base import cpp_base

class cpp_type_def(cpp_base):
    def __init__(self, name, size, ghidra_namespace):
        self.cpp_name = name
        self.ghidra_namespace = ghidra_namespace
        self.size = size

    def data_size(self):
        return self.size