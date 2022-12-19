from xml.etree.ElementTree import SubElement
from .lookups import get_data_size, get_ghidra_namespace
from .cpp_base import cpp_base, cpp_name_lookup

class cpp_function_return_def(cpp_name_lookup):
    XML_TYPE = "RETURN_TYPE"

    def __init__(self, datatype):
        cpp_name_lookup.__init__(self)
        self.datatype = datatype

    def __eq__(self, other):
        return self.datatype == other.datatype

    def get_xml(self, parent):
        SubElement(parent, self.XML_TYPE, {
            'DATATYPE':self.datatype,
            'DATATYPE_NAMESPACE':get_ghidra_namespace(self.datatype),
            'SIZE':hex(get_data_size(self.datatype)),
        })
        
    def resolve_types(self):
        self.datatype = self.lookup_datatype(self.datatype)

class cpp_function_arg_def(cpp_name_lookup):
    XML_TYPE = "PARAMETER"

    def __init__(self, name, datatype):
        cpp_name_lookup.__init__(self)
        self.name = name
        self.datatype = datatype

    def __eq__(self, other):
        return self.name == other.name and self.datatype == other.datatype

    def get_xml(self, parent, ordinal):
        SubElement(parent, self.XML_TYPE, {
            'ORDINAL':hex(ordinal),
            'DATATYPE':self.datatype,
            'DATATYPE_NAMESPACE':get_ghidra_namespace(self.datatype),
            'NAME':self.name,
            'SIZE':hex(get_data_size(self.datatype)),
        })
        
    def resolve_types(self):
        self.datatype = self.lookup_datatype(self.datatype)

class cpp_function_base():
    XML_TYPE = "FUNCTION_DEF"
    def __init__(self, return_datatype):
        self.set_return_type(return_datatype)
        self.args = []

    def matches_function_signature(self, other):
        if self.return_type != other.return_type or len(self.args) != len(other.args):
            return False
            
        for i in range(len(self.args)):
            if self.args[i] != other.args[i]:
                return False

        return True

    def data_size(self):
        return 4 #functions are always pointers!

    def set_return_type(self, return_name):
        self.return_type = cpp_function_return_def(return_name)

    def add_function_arg(self, name, datatype):
        cpp_function_arg = cpp_function_arg_def(name, datatype)
        self.args.append(cpp_function_arg)

        return cpp_function_arg
        
    def resolve_types(self):
        self.return_type.resolve_types()
        for arg in self.args:
            arg.resolve_types()

class cpp_function_def(cpp_base, cpp_function_base):
    def __init__(self, unqualified_name, cpp_namespace, ghidra_namespace, return_datatype):
        cpp_base.__init__(self, unqualified_name, cpp_namespace, ghidra_namespace)
        cpp_function_base.__init__(self, return_datatype)

    def get_xml(self, parent):
        element = SubElement(parent, self.XML_TYPE, {
            'NAME': self.cpp_name,
            'NAMESPACE': self.ghidra_namespace,
        })

        self.return_type.get_xml(element)

        ordinal = 0
        for arg in self.args:
            arg.get_xml(element, ordinal)
            ordinal += 1

class cpp_member_function_def(cpp_function_def):
    def __init__(self, unqualified_name, cpp_namespace, ghidra_namespace, this_datatype, return_datatype):
        cpp_function_def.__init__(self, unqualified_name, cpp_namespace, ghidra_namespace, return_datatype)
        self.add_function_arg("this", this_datatype + " *")

class cpp_virtual_function_def(cpp_function_base):
    XML_VIRTUAL_TYPE = "MEMBER"

    def __init__(self, name, return_datatype):
        cpp_function_base.__init__(self, return_datatype)
        self.function_name = name

    def get_xml(self, parent, this_datatype, cpp_namespace, ghidra_namespace):
        element = SubElement(parent, self.XML_TYPE, {
            'NAME': cpp_namespace + self.function_name,
            'NAMESPACE': ghidra_namespace,
        })

        self.return_type.get_xml(element)

        cpp_function_arg_def("this", this_datatype + " *").get_xml(element, 0)

        ordinal = 1
        for arg in self.args:
            arg.get_xml(element, ordinal)
            ordinal += 1

    def get_vtable_xml(self, parent, offset, cpp_namespace, ghidra_namespace):
        data_size = 4
        SubElement(parent, self.XML_VIRTUAL_TYPE, {
            'OFFSET': hex(offset),
            'DATATYPE': cpp_namespace + self.function_name + " *",
            'DATATYPE_NAMESPACE': ghidra_namespace,
            'NAME': self.function_name,
            'SIZE': hex(data_size),
        })
        return offset + data_size