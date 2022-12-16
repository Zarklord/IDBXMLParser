def get_xml(cpp_list, parent):
    for cpp_obj in cpp_list:
        cpp_obj.get_xml(parent)

def resolve_types(cpp_list):
    for cpp_obj in cpp_list:
        cpp_obj.resolve_types()

class namespace_container():
    def __init__(self):
        self.namespaces = []
        
    def add_namespace(self, unqualified_name):
        for namespace in self.namespaces:
            if namespace.unqualified_name == unqualified_name:
                return namespace

        from .cpp_namespace import cpp_namespace_def
        cpp_namespace = cpp_namespace_def(unqualified_name, self.cpp_name, self.child_ghidra_namespace)
        self.namespaces.append(cpp_namespace)

        return cpp_namespace

    def get_xml(self, parent):
        get_xml(self.namespaces, parent)

    def resolve_types(self):
        resolve_types(self.namespaces)

class class_container():
    def __init__(self):
        self.classes = []
        
    def add_class(self, unqualified_name, *args):
        from .cpp_class import cpp_class_def
        cpp_class = cpp_class_def(unqualified_name, self.cpp_name, self.child_ghidra_namespace, *args)
        self.classes.append(cpp_class)

        return cpp_class

    def get_xml(self, parent):
        get_xml(self.classes, parent)

    def resolve_types(self):
        resolve_types(self.classes)

class union_container():
    def __init__(self):
        self.unions = []

    def add_union(self, unqualified_name, *args):
        from .cpp_union import cpp_union_def
        cpp_union = cpp_union_def(unqualified_name, self.cpp_name, self.child_ghidra_namespace, *args)
        self.unions.append(cpp_union)

        return cpp_union

    def get_xml(self, parent):
        get_xml(self.unions, parent)

    def resolve_types(self):
        resolve_types(self.unions)

class enum_container():
    def __init__(self):
        self.enums = []

    def add_enum(self, unqualified_name, *args):        
        from .cpp_enum import cpp_enum_def
        cpp_enum = cpp_enum_def(unqualified_name, self.cpp_name, self.child_ghidra_namespace, *args)
        self.enums.append(cpp_enum)

        return cpp_enum

    def get_xml(self, parent):
        get_xml(self.enums, parent)

    def resolve_types(self):
        resolve_types(self.enums)

class static_function_container():
    def __init__(self):
        self.static_functions = []

    def add_function(self, unqualified_name, *args):
        from .cpp_function import cpp_function_def
        cpp_function = cpp_function_def(unqualified_name, self.cpp_name, self.child_ghidra_namespace, *args)
        self.static_functions.append(cpp_function)

        return cpp_function

    def get_xml(self, parent):
        get_xml(self.static_functions, parent)

    def resolve_types(self):
        resolve_types(self.static_functions)

class member_function_container():
    def __init__(self):
        self.member_functions = []
        self.virtual_functions = []

    def add_member_function(self, unqualified_name, *args):
        from .cpp_function import cpp_member_function_def
        cpp_function = cpp_member_function_def(unqualified_name, self.cpp_name, self.child_ghidra_namespace, self.cpp_name, *args)
        self.member_functions.append(cpp_function)

        return cpp_function

    def add_virtual_function(self, unqualified_name, *args):
        from .cpp_function import cpp_virtual_function_def
        cpp_function = cpp_virtual_function_def(unqualified_name, *args)
        self.virtual_functions.append(cpp_function)

        return cpp_function

    def get_vtable_xml(self, parent, offset):
        for cpp_function in self.virtual_functions:
            offset = cpp_function.get_vtable_xml(parent, offset)
        return offset

    def get_xml(self, parent):
        get_xml(self.member_functions, parent)

    def resolve_types(self):
        resolve_types(self.member_functions)
        resolve_types(self.virtual_functions)

class typedef_container():
    def __init__(self):
        self.typedefs = []

    def add_typedef(self, unqualified_name, *args):
        from .cpp_typedef import cpp_typedef_def
        cpp_typedef = cpp_typedef_def(unqualified_name, self.cpp_name, self.child_ghidra_namespace, *args)
        self.typedefs.append(cpp_typedef)

        return cpp_typedef

    def get_xml(self, parent):
        get_xml(self.typedefs, parent)

    def resolve_types(self):
        resolve_types(self.typedefs)

class variable_container():
    def __init__(self):
        self.variables = []

    def add_variable(self, unqualified_name, *args):
        from .cpp_variable import cpp_variable_def
        cpp_variable = cpp_variable_def(unqualified_name, *args)
        self.variables.append(cpp_variable)

        return cpp_variable

    def get_xml(self, parent):
        get_xml(self.variables, parent)

    def resolve_types(self):
        resolve_types(self.variables)

class types_container():
    def __init__(self):
        self.types = []

    def add_type(self, typename, size, ghidra_namespace):
        from .cpp_type import cpp_type_def
        cpp_type = cpp_type_def(typename, size, ghidra_namespace)
        self.types.append(cpp_type)

        return cpp_type

    def get_xml(self, parent):
        pass

    def resolve_types(self):
        pass