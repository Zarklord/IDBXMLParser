from xml.dom import minidom
import xml.etree.ElementTree as ET
from . import mv
from .cpp_global import cpp_global_def

def init_cpp(ghidra_namespace):
    return cpp_global_def(ghidra_namespace)

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8', xml_declaration=False)
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ").split('\n', 1)[1]

def write_xml(file_path, name, processor_specification):
    program = ET.Element("PROGRAM", {'NAME':name})
    ET.SubElement(program, "PROCESSOR", processor_specification)
    mv.cpp_global.get_xml(ET.SubElement(program, "DATATYPES"))

    with open(file_path, "w") as f:
        f.write('<?xml version="1.0" standalone="yes"?>\n')
        f.write('<?program_dtd version="1"?>\n')
        f.write(prettify_xml(program))