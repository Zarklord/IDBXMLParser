from .containers import *
from xml.etree.ElementTree import SubElement
from .cpp_base import cpp_base, cpp_member_variables

cpp_union_lookup = [class_container, union_container, enum_container, static_function_container, member_function_container, typedef_container]

class cpp_union_def(cpp_base, cpp_member_variables, *cpp_union_lookup):
    XML_TYPE = "UNION"

    def __init__(self, unqualified_name, cpp_namespace, ghidra_namespace):
        cpp_base.__init__(self, unqualified_name, cpp_namespace, ghidra_namespace)
        cpp_member_variables.__init__(self)

        for container in cpp_union_lookup:
            container.__init__(self)
            
    def data_size(self):
        size = 0
        for cpp_variable in self.variables:
            size = max(size, cpp_variable.data_size())
        return size

    def get_xml(self, parent):
        for container in cpp_union_lookup:
            container.get_xml(self, parent)

        element = SubElement(parent, self.XML_TYPE, {
            'NAME': self.cpp_name,
            'NAMESPACE': self.ghidra_namespace,
            'SIZE': hex(self.data_size())
        })
        for cpp_variable in self.variables:
            cpp_variable.get_xml(element, 0)
    
    def resolve_types(self):
        for container in cpp_union_lookup:
            container.resolve_types(self)
        cpp_member_variables.resolve_types(self)
