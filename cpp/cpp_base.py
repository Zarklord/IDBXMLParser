import re
from .lookups import set_cpp_obj_for_datatype, lookup_type
from . import mv
from copy import deepcopy

class cpp_name_lookup():
    def __init__(self):
        self.active_namespaces = mv.cpp_global.get_active_namespaces()

    def lookup_datatype(self, datatype):
        if self.active_namespaces:
            resolved_datatype = lookup_type(datatype, self.active_namespaces)
            self.active_namespaces = None
            return resolved_datatype
        return datatype

def is_pointer_to_type(qualified_name, datatype):
    return re.match(qualified_name + r"\s*\*+", datatype) is not None

def make_cpp_name(cpp_namespace, unqualified_name):
    return ("" if cpp_namespace == "" else cpp_namespace + "::") + unqualified_name

def make_child_ghidra_namespace(ghidra_namespace, unqualified_name):
    return ghidra_namespace + "/" + unqualified_name

class cpp_base(cpp_name_lookup):
    def __init__(self, unqualified_name, cpp_namespace, ghidra_namespace):
        cpp_name_lookup.__init__(self)
        self.cpp_name = make_cpp_name(cpp_namespace, unqualified_name)
        self.ghidra_namespace = ghidra_namespace
        self.child_ghidra_namespace = make_child_ghidra_namespace(self.ghidra_namespace, unqualified_name)

        set_cpp_obj_for_datatype(self, self.cpp_name)

class cpp_member_variables():
    def __init__(self):
        self.variables = []

    def add_member_variable(self, name, datatype):
        from .cpp_variable import cpp_variable_def
        cpp_variable = cpp_variable_def(name, datatype)
        self.variables.append(cpp_variable)

        return cpp_variable

    def resolve_types(self):
        for cpp_variable in self.variables:
            cpp_variable.resolve_types()

