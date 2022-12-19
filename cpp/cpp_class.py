from .containers import *
from .cpp_base import cpp_base, cpp_member_variables, cpp_name_lookup
from .lookups import get_cpp_obj
from xml.etree.ElementTree import SubElement

cpp_class_lookup = [class_container, union_container, enum_container, static_function_container, member_function_container, typedef_container]

class cpp_parent_class_def(cpp_name_lookup):
    def __init__(self, classname):
        cpp_name_lookup.__init__(self)
        self.classname = classname

    def data_size(self):
        cpp_class = get_cpp_obj(self.classname)
        return cpp_class.data_size()

    def get_class_xml(self, *args):
        cpp_class = get_cpp_obj(self.classname)
        return cpp_class.get_class_xml(*args)

    def get_primary_vtbl_name(self):
        cpp_class = get_cpp_obj(self.classname)
        return cpp_class.get_primary_vtbl_name()

    def get_vtables(self, *args):
        cpp_class = get_cpp_obj(self.classname)
        return cpp_class.get_vtables(*args)

def find_function_in_vtbl(vtbl_function, virtual_functions):
    for cpp_virtual_function in virtual_functions:
        if vtbl_function.function_name == cpp_virtual_function.function_name and vtbl_function.matches_function_signature(cpp_virtual_function):
            return cpp_virtual_function

class cpp_class_def(cpp_base, cpp_member_variables, *cpp_class_lookup):
    XML_TYPE = "STRUCTURE"
    XML_VTBL_TYPE = "MEMBER"
    VTBL_POSTFIX = "_vtbl"

    def __init__(self, unqualified_name, cpp_namespace, ghidra_namespace):
        cpp_base.__init__(self, unqualified_name, cpp_namespace, ghidra_namespace)
        cpp_member_variables.__init__(self)

        self.class_name = unqualified_name

        for container in cpp_class_lookup:
            container.__init__(self)

        self.parent_classes = []

    def add_parent_class(self, parent_class_name):
        cpp_parent_class = cpp_parent_class_def(parent_class_name)
        self.parent_classes.append(cpp_parent_class)

        return cpp_parent_class
        
    def is_base_class(self):
        return len(self.parent_classes) == 0

    def write_vtable(self):
        return self.is_base_class() and len(self.virtual_functions) > 0

    def data_size(self):
        size = 0
        for cpp_parent_class in self.parent_classes:
            size += cpp_parent_class.data_size()

        if self.write_vtable():
            size += 4

        for cpp_variable in self.variables:
            size += cpp_variable.data_size()

        return size

    def get_xml(self, parent):
        for container in cpp_class_lookup:
            container.get_xml(self, parent)

        self.get_vtable_xml(parent)

        data_size = self.data_size()
        element = SubElement(parent, self.XML_TYPE, {
            'NAME': self.cpp_name,
            'NAMESPACE': self.ghidra_namespace,
            'SIZE': hex(data_size),
        })
        offset = self.get_class_xml(element, 0, "", self.child_ghidra_namespace)

        assert(offset == data_size)

    def resolve_types(self):
        for container in cpp_class_lookup:
            container.resolve_types(self)
        cpp_member_variables.resolve_types(self)
        
    def get_vtable_xml(self, parent):
        virtual_member_functions = set()
        child_cpp_name = self.cpp_name + "::"

        for vtbl_name, vtbl_functions in self.get_vtables().items():
            data_size = len(vtbl_functions) * 4
            vtbl_element = SubElement(parent, self.XML_TYPE, {
                'NAME': vtbl_name + self.VTBL_POSTFIX,
                'NAMESPACE': self.child_ghidra_namespace,
                'SIZE': hex(data_size),
            })
            offset = 0

            for vtbl_function in vtbl_functions:
                virtual_member_functions.add(vtbl_function)
                offset = vtbl_function.get_vtable_xml(vtbl_element, offset, child_cpp_name, self.child_ghidra_namespace)

            assert(offset == data_size)

        for virtual_member_function in virtual_member_functions:
            virtual_member_function.get_xml(parent, self.cpp_name, child_cpp_name, self.child_ghidra_namespace)

    def get_class_xml(self, parent, offset, vtbl_parent_name, vtbl_ghidra_namespace):
        for cpp_parent_class in self.parent_classes:
            offset = cpp_parent_class.get_class_xml(parent, offset, vtbl_parent_name + self.class_name + "_", vtbl_ghidra_namespace)
        if self.write_vtable():
            data_size = 4
            SubElement(parent, self.XML_VTBL_TYPE, {
                'OFFSET': hex(offset),
                'DATATYPE': vtbl_parent_name + self.class_name + self.VTBL_POSTFIX,
                'DATATYPE_NAMESPACE': vtbl_ghidra_namespace,
                'SIZE': hex(data_size),
            })
            offset += data_size

        for cpp_variable in self.variables:
            offset = cpp_variable.get_xml(parent, offset)
        
        return offset
        
    def get_primary_vtbl_name(self):
        if len(self.parent_classes) > 0:
            cpp_parent_class = self.parent_classes[1]
            return self.class_name + "_" + cpp_parent_class.get_primary_vtbl_name()
        return self.class_name

    def get_vtables(self, parent_vtbl_name=""):
        vtbl_base_name = parent_vtbl_name + self.class_name

        parent_vtbl_dictionaries = []
        for cpp_parent_class in self.parent_classes:
            parent_vtbl_dictionaries.append(cpp_parent_class.get_vtables(vtbl_base_name + "_"))

        virtual_function_refs = {}

        for parent_vtbl_dictionary in parent_vtbl_dictionaries:
            for vtbl_name, vtbl_functions in parent_vtbl_dictionary.items():
                for vtbl_function_index in range(len(vtbl_functions)):
                    vtbl_function = vtbl_functions[vtbl_function_index]

                    cpp_virtual_function = find_function_in_vtbl(vtbl_function, self.virtual_functions)
                    if cpp_virtual_function:
                        vtbl_functions[vtbl_function_index] = cpp_virtual_function

                        virtual_function_refs[cpp_virtual_function] = True

        vtbl_dictionary = {}
        for parent_vtbl_dictionary in parent_vtbl_dictionaries:
            vtbl_dictionary = {**vtbl_dictionary, **parent_vtbl_dictionary}

        primary_vtbl_name = parent_vtbl_name + self.get_primary_vtbl_name()

        if len(vtbl_dictionary) == 0:
            vtbl_dictionary[primary_vtbl_name] = []

        for cpp_virtual_function in self.virtual_functions:
            if cpp_virtual_function not in virtual_function_refs:
                vtbl_dictionary[primary_vtbl_name].append(cpp_virtual_function)

        return vtbl_dictionary