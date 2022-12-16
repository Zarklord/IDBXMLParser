from .containers import *
from .cpp_base import cpp_base

cpp_namespace_lookup = [namespace_container, class_container, union_container, enum_container, static_function_container, typedef_container]

class cpp_namespace_def(cpp_base, *cpp_namespace_lookup):
    def __init__(self, unqualified_name, cpp_namespace, ghidra_namespace):
        cpp_base.__init__(self, unqualified_name, cpp_namespace, ghidra_namespace)
        for container in cpp_namespace_lookup:
            container.__init__(self)
    
    def get_xml(self, parent):
        for container in cpp_namespace_lookup:
            container.get_xml(self, parent)
    
    def resolve_types(self):
        for container in cpp_namespace_lookup:
            container.resolve_types(self)

    def parse(self, ls):
        while True:
            ls.skip_cpp_comment()
            if ls.is_eof() or ls.is_current('}'):
                break
            elif ls.is_current ('#'):
                ls.skip_to_newline_or_eof()
            elif ls.is_alpha():
                token = ls.read_token()
                #process_token(ls, token, self)
            else:
                ls.next()