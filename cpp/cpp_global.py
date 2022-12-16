import io
from .cpp_namespace import cpp_namespace_def
from .containers import *
from .preprocessor_define import preprocessor_function_define, preprocessor_variable_define
from . import mv
from .lexer.cpp_lexer import lex

cpp_global_lookups = [cpp_namespace_def, types_container]

class cpp_global_def(*cpp_global_lookups):
    def __init__(self, ghidra_namespace):
        assert(mv.cpp_global == None)

        mv.cpp_global = self
        self.active_namespaces = {}

        cpp_namespace_def.__init__(self, "", "", "")
        types_container.__init__(self)
        self.ghidra_namespace = "/" + ghidra_namespace
        self.child_ghidra_namespace = None

        self.defines = {}
        self.function_defines = {}

    def get_active_namespaces(self):
        return self.active_namespaces.copy()
    
    def get_xml(self, parent):
        for container in cpp_global_lookups:
            container.get_xml(self, parent)
    
    def resolve_types(self):
        for container in cpp_global_lookups:
            container.resolve_types(self)

    def preprocessor_parse(self, file):
        ls = lex(file)
        while True:
            ls.skip_cpp_comment()
            if ls.is_eof():
                break
            elif ls.is_current ('#'):
                ls.next()
        
                token = ls.read_token()
                if token == "define":
                    ls.skip_whitespace()

                    name = ls.read_token()
                    args = ls.read_parameters()
                    ls.skip_whitespace()
                    macro = ls.read_macro_value()

                    #print(name, args, macro)
                    if args != "":
                        self.function_defines[name] = preprocessor_function_define(name, args, macro)
                    else:
                        self.defines[name] = preprocessor_variable_define(name, macro)
                else:
                    while not ls.is_newline_or_eof():
                        ls.next()
            else:
                ls.next()

    def apply_preprocessor(self, file):
        ls = lex(file)
        file_buffer = ""
        while True:
            ls.skip_cpp_comment(True)
            if ls.is_eof():
                break
            elif ls.is_current ('#'):
                ls.skip_to_newline_or_eof(True)
            elif ls.is_alpha():
                file_buffer += ls.buffer
                token = ls.read_token()
                if token in self.defines:
                    token = self.defines[token].get_value()
                elif token in self.function_defines:
                    pass #not implementing at the moment
                ls.buffer = token
            else:
                ls.save_and_next()
        file_buffer += ls.buffer

        return io.StringIO(file_buffer)

    def parse(self, file):
        file = self.apply_preprocessor(file)
        ls = lex(file)