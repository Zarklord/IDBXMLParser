class lex():
    def __init__(self, file):
        self.file = file
        self.buffer = ""
        self.next()

    def next(self, save=False):
        if save:
            self.save()
        self.current = self.file.read(1)

    def save(self):
        self.buffer += self.current

    def save_and_next(self):
        self.save()
        self.next()

    def reset_buffer(self):
        self.buffer = ""

    def check_next(self, *chars):
        save = False
        if isinstance(chars[0], bool):
            save = chars[0]

        for char in chars:
            if isinstance(char, bool):
                continue

            if self.current == char:
                self.next(save)
                return True
        return False

    def is_current(self, *chars):
        for char in chars:
            if self.current == char:
                return True
        return False

    def is_eof(self):
        return self.current == ''

    def is_alpha(self):
        return self.current.isalpha() or self.current == '_'

    def is_alnum(self):
        return self.current.isalnum() or self.current == '_'

    def is_whitespace(self):
        return self.is_current(' ', '\f', '\t', '\v')

    def is_newline(self):
        return self.is_current('\r', '\n')

    def is_newline_or_eof(self):
        return self.is_newline() or self.is_eof()

    def skip_whitespace(self):
        while self.is_whitespace():
            self.next()

    def skip_cpp_comment(self, save=False):
        if self.is_current('/'):
            self.next(save)
            if self.check_next(save, '/'):
                while not self.is_newline() and not self.is_eof():
                    self.next(save)
            elif self.check_next(save, '*'):
                while True:
                    if self.check_next(save, '*'):
                        if self.check_next(save, '/'):
                            break
                    else:
                        self.next(save)

    def read_token(self):
        self.reset_buffer()
        if self.is_alpha():
            while self.is_alnum():
                self.save_and_next()
            return self.buffer

    def read_type(self):
        self.reset_buffer()
        if self.is_alpha() or self.is_current(':'):
            while self.is_alnum() or self.is_current(':', '<'):
                self.save_and_next()
                self.read_and_save_mirrored_set('<', '>')
            return self.buffer

    def read_parameters(self):
        self.reset_buffer()
        self.read_and_save_mirrored_set('(', ')')
        return self.buffer

    def read_and_save_mirrored_set(self, opening, closing):
        if self.is_current(opening):
            self.save_and_next()
            depth = 1
            while depth > 0:
                if self.is_current(opening):
                    depth += 1
                elif self.is_current(closing):
                    depth -= 1
                self.save_and_next()

    def read_macro_value(self):
        self.reset_buffer()
        last_char_is_backslash = False

        macro_buffer = ""
        while not self.is_eof():
            if self.is_current('\\'):
                macro_buffer += self.buffer
                self.reset_buffer()
                last_char_is_backslash = True
            elif self.is_newline():
                if last_char_is_backslash:
                    self.reset_buffer()
                    last_char_is_backslash = False
                    while self.is_newline():
                        self.save_and_next()
                else:
                    break
            elif not self.is_whitespace():
                last_char_is_backslash = False
            self.save_and_next()

        macro_buffer += self.buffer

        return macro_buffer

    def read_to_newline_or_eof(self):
        self.reset_buffer()
        while not self.is_newline_or_eof():
            self.save_and_next()
        return self.buffer

    def skip_to(self, *chars):
        while not self.is_current(chars):
            self.next()

    def skip_to_newline_or_eof(self, save=False):
        while not self.is_newline_or_eof():
            self.next(save)


def read_keywords(ls, word, outfile):
    if word == "namespace":
        ls.skip_whitespace()

        namespace = ls.read_word()

        print("Word: ", word)
        print("Namspace: ", namespace)

        outfile.write(word + " " + namespace)
    else:
        print(word)
        outfile.write(word)

def lex_cpp(file):
    outfile = open("outfile.txt", "w")
    ls = lex(file)
    while True:
        if ls.is_eof():
            break
        elif ls.is_newline() or ls.is_whitespace():
            outfile.write(ls.current)
            ls.next()
        elif ls.is_current('/'):
            ls.next()
            if ls.check_next('/'):
                while not ls.is_newline() and not ls.is_eof():
                    ls.next() #skip until the end of the line or file
            elif ls.check_next('*'):
                while True:
                    if ls.check_next('*'):
                        if ls.check_next('/'):
                            break
                    else:
                        ls.next()
            else:
                outfile.write('/')
        elif ls.is_current ('#'):
            while not ls.is_newline() and not ls.is_eof():
                ls.save_and_next()
        elif ls.is_alpha():
            word = ls.read_word()

            read_keywords(ls, word, outfile)
        else:
            outfile.write(ls.current)
            ls.next()

    outfile.close()