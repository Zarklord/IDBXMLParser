cpp_keywords = [
    "alignas", "alignof", "asm", "auto", "break", "case", "catch",
    "class", "const", "constexpr", "continue", "decltype", "default",
    "delete", "do", "else", "enum", "explicit", "export ", "extern",
    "for", "friend", "goto", "if", "inline", "mutable", "namespace",
    "new", "noexcept", "nullptr", "private", "protected", "public",
    "register", "return", "sizeof", "static", "struct", "switch",
    "template", "thread_local", "throw", "try", "typedef", "typeid",
    "typename", "union", "using", "virtual", "volatile", "while",
]

cpp_visibility_keywords = ["public", "protected", "private"]

cpp_classtype_keywords = ["class", "struct"]

def process_word(ls, word, parser):
    pass

def process_token(ls, token, parser):
    if token == "namespace":
        ls.skip_whitespace()
        name = ls.read_token()
        
        namespace = parser.find_namespace()
        if namespace is None:
            namespace = cpp_namespace(name)
            parser.namespaces.append(namespace)
        
        ls.skip_to('{')

        ls.skip()
        namespace.parse(ls)
    elif token in cpp_classtype_keywords:
        ls.skip_whitespace()
        name = ls.read_token()

        cppclass = cpp_class(name)
        cppclass.class_key = token

        ls.skip_to(':', '{')

        #read inheritance
        while not ls.is_current('{'):
            ls.skip()
            ls.skip_whitespace()
            parent_name = ls.read_type()

            visibility = "lookup"
            if parent_name in cpp_visibility_keywords:
                visibility = parent_name
                ls.skip_whitespace()
                parent_name = ls.read_type()

            cppclass.parent_classes.append(cpp_parent_class(parent_name, visibility))
            
            ls.skip_to(',', '{')
                
        parser.classes.append(cppclass)
        ls.skip()
        cppclass.parse(ls)
    elif token == "union":
        ls.skip_whitespace()

        name = None
        if not ls.is_current('{'):
            name = ls.read_token()

        ls.skip_to('{', ';')

        if ls.is_current(';'):
            return #just a forward declaration, which we don't care about

        union = cpp_union(name)

        parser.unions.append(union)
        ls.skip()
        union.parse(ls)
        pass
    elif token == "enum":
        ls.skip_whitespace()

        name = None
        datatype = "int"
        if not ls.is_current('{', ':'):
            name = ls.read_token()

            if name in cpp_classtype_keywords:
                ls.skip_whitespace()
                name = ls.read_token()

        ls.skip_to('{', ':', ';')

        if ls.is_current(":"):
            ls.skip_whitespace()
            datatype = ls.read_type()
            ls.skip_to('{', ';')

        if ls.is_current(';'):
            return #just a forward declaration, which we don't care about
                
        enum = cpp_enum(name, datatype)

        parser.enums.append(enum)
        ls.skip()
        enum.parse(ls)
    elif token == "typedef":
        pass
    else:
        if token in cpp_keywords:
            print("unknown cpp keyword: " + token)
        process_word(ls, token, parser)
