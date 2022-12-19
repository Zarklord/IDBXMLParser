import os
from cpp_predefined_types import apply_predefined_types
from cpp_to_xml import *
import gv

from cpp import init_cpp, write_xml

if __name__ == '__main__':

    cpp_global = init_cpp("Spore")
    apply_predefined_types(cpp_global)

    PrimaryBaseClass = cpp_global.add_class("PrimaryBaseClass")
    PrimaryBaseClass.add_member_variable("baseMemberVariable", "uint32_t")

    baseMemberFunction = PrimaryBaseClass.add_member_function("baseMemberFunction", "void")
    baseMemberFunction.add_function_arg("arg1", "uint8_t")

    PrimaryBaseClass.add_virtual_function("baseVirtualFunction", "uint16_t")
    
    SecondaryBaseClass = cpp_global.add_class("SecondaryBaseClass")
    SecondaryBaseClass.add_member_variable("secondaryMemberVariable", "uint16_t")

    secondaryMemberFunction = SecondaryBaseClass.add_member_function("secondaryMemberFunction", "uint8_t")
    secondaryMemberFunction.add_function_arg("arguement", "uint16_t")

    secondaryVirtualFunction = SecondaryBaseClass.add_virtual_function("secondaryVirtualFunction", "void")
    secondaryVirtualFunction.add_function_arg("arg1", "bool")
    secondaryVirtualFunction.add_function_arg("arg2", "bool")


    DerivedClass = cpp_global.add_class("DerivedClass")
    DerivedClass.add_parent_class("PrimaryBaseClass")
    DerivedClass.add_parent_class("SecondaryBaseClass")

    DerivedClass.add_member_variable("derivedMemberVariable", "char")

    derivedMemberFunction = DerivedClass.add_member_function("derivedMemberFunction", "uint8_t")

    derivedVirtualFunction = DerivedClass.add_virtual_function("derivedVirtualFunction", "uint32_t")

    #override baseVirtualFunction
    DerivedClass.add_virtual_function("baseVirtualFunction", "uint16_t")

    write_xml("cpp_class_example.xml", "SporeModAPI.h", {
        'NAME':"metapc",
        'ENDIAN':"little",
        'ADDRESS_MODEL':"32-bit"
    })