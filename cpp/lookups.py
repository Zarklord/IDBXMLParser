import re
        
type_match_regex = re.compile(r"(.+?)([\*\s]*)$")

def is_pointer_type(datatype):
    pointer_group = re.match(type_match_regex, datatype).group(2)
    return pointer_group is not None and '*' in pointer_group

#removes extra pointers
def get_base_type(datatype):
    return re.match(type_match_regex, datatype).group(1)

datatype_to_cpp_obj = []
def set_cpp_obj_for_datatype(cpp_obj, datatype):
    if datatype != "":
        datatype_to_cpp_obj[datatype] = cpp_obj

def get_cpp_obj(datatype):
    return datatype_to_cpp_obj[datatype]

def get_ghidra_namespace(datatype):
    datatype = get_base_type(datatype)

    cpp_obj = datatype_to_cpp_obj[datatype]
    if cpp_obj:
        return cpp_obj.ghidra_namespace

    assert(False, "unable to lookup data type")
    return "/" #unknown type

def get_data_size(datatype):
    if is_pointer_type(datatype):
        return 4

    cpp_obj = datatype_to_cpp_obj[datatype]
    if cpp_obj:
        return cpp_obj.data_size()

    assert(False, "unable to lookup data type")
    return 4 #unknown type

def lookup_type(datatype, active_namespaces):
    for namespace in active_namespaces:
        resolved_datatype = namespace + "::" + datatype
        if datatype_to_cpp_obj[resolved_datatype] is not None:
            return resolved_datatype
    
    #incase its in the global namespace
    if datatype_to_cpp_obj[datatype] is not None:
        return datatype
        
    assert(False, "unable to lookup data type")