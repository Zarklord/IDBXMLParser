import os
from cpp_predefined_types import apply_predefined_types
from cpp_to_xml import *
import gv

from cpp import init_cpp, write_xml



def for_every_file(path, func):
    for root, subdirs, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            with open(file_path, "r") as f:
                func(f)

def do_preprocess(f):
    cpp_global.preprocessor_parse(f)

def do_parse(f):
    cpp_global.parse(f)

if __name__ == '__main__':

    cpp_global = init_cpp("Spore")
    apply_predefined_types(cpp_global)
    
    for_every_file(gv.spore_mod_api_path, do_preprocess)

    for name, function_define in cpp_global.function_defines.items():
        print(function_define)
    
    with open('F:\Spore\Spore-ModAPI\Spore ModAPI\Spore\App\cGameModeManager.h', 'r') as f:
        cpp_global.parse(f)
    
    #for_every_file(gv.spore_mod_api_path, do_parse)

    write_xml("test.xml", "SporeModAPI.h", {
        'NAME':"metapc",
        'ENDIAN':"little",
        'ADDRESS_MODEL':"32-bit"
    })
    
    #with open('F:\Spore\Spore-ModAPI\Spore ModAPI\Spore\App\PropertyList.h', 'r') as f:
    #    gv.cpp_namespace.parse(lex(f))

    #for define in gv.cpp_preprocessor.defines:
    #    print(define)
    #for define in gv.cpp_preprocessor.function_defines:
    #    print(define)