from xml.etree.ElementTree import SubElement
from .lookups import get_data_size, get_ghidra_namespace
from .cpp_base import cpp_name_lookup

class cpp_variable_def(cpp_name_lookup):
    XML_TYPE = "MEMBER"

    def __init__(self, name, datatype):
        cpp_name_lookup.__init__(self)
        self.name = name
        self.datatype = datatype

    def get_size(self):
        return get_data_size(self.datatype)

    def get_xml(self, parent, offset):
        data_size = self.data_size()
        SubElement(parent, self.XML_TYPE, {
            'OFFSET': hex(offset),
            'DATATYPE': self.datatype,
            'DATATYPE_NAMESPACE': get_ghidra_namespace(self.datatype),
            'NAME': self.name,
            'SIZE': hex(data_size),
        })
        return offset + data_size
    
    def resolve_types(self):
        self.datatype = self.lookup_datatype(self.datatype)

