from xml.etree.ElementTree import SubElement
from .lookups import get_data_size
from .cpp_base import cpp_base
        
class cpp_enumerator_def():
    XML_TYPE = "ENUM_ENTRY"

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_xml(self, parent):
        SubElement(parent, self.XML_TYPE, {
            'NAME': self.name,
            'VALUE': self.value,
        })

class cpp_enum_def(cpp_base):
    XML_TYPE = "ENUM"

    def __init__(self, unqualified_name, cpp_namespace, ghidra_namespace, size_type):
        cpp_base.__init__(self, unqualified_name, cpp_namespace, ghidra_namespace)
        self.size_type = size_type
        self.enumerators = []

    def data_size(self):
        return get_data_size(self.size_type)

    def get_xml(self, parent):
        element = SubElement(parent, self.XML_TYPE, {
            'NAME': self.cpp_name,
            'NAMESPACE': self.ghidra_namespace,
            'SIZE': hex(self.data_size())
        })
        for cpp_enumerator in self.enumerators:
            cpp_enumerator.get_xml(element)

    def resolve_types(self):
        self.size_type = self.lookup_datatype(self.size_type)

    def add_enumerator(self, name, value):
        cpp_enumerator = cpp_enumerator_def(name, value)
        self.enumerators.append(cpp_enumerator)

        return cpp_enumerator
