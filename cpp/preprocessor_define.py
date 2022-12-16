class preprocessor_variable_define():
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_value(self):
        return self.value

    def __str__(self) -> str:
        return "#define " + self.name + " " + self.value

def get_split_args(args):
    return [arg.strip() for arg in args[1:-1].split(",")]

class preprocessor_function_define():
    def __init__(self, name, args, value):
        self.name = name
        self.args = args
        self.value = value

    def get_value(self, arguments):
        args = 
        arguments = 
        arg_dicitonary = dict(zip(get_split_args(self.args), get_split_args(arguments)))


        pass

    def __str__(self) -> str:
        return "#define " + self.name + self.args + " " + self.value