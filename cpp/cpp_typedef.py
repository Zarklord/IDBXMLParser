from xml.etree.ElementTree import SubElement
from .lookups import get_data_size, get_ghidra_namespace
from .cpp_base import cpp_base

class cpp_typedef_def(cpp_base):
    XML_TYPE = "TYPE_DEF"

    def __init__(self, unqualified_name, cpp_namespace, ghidra_namespace, datatype):
        cpp_base.__init__(self, unqualified_name, cpp_namespace, ghidra_namespace)
        self.datatype = datatype
    
    def data_size(self):
        return get_data_size(self.datatype)

    def get_xml(self, parent):
        SubElement(parent, self.XML_TYPE, {
            'NAME': self.cpp_name,
            'NAMESPACE': self.ghidra_namespace,
            'DATATYPE': self.datatype,
            'DATATYPE_NAMESPACE': get_ghidra_namespace(self.datatype),
        })
    
    def resolve_types(self):
        self.datatype = self.lookup_datatype(self.datatype)
