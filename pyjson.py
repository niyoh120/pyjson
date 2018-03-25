from collections import OrderedDict


NUMBER = 'NUMBER'
STRING = 'STRING'
BOOL = 'BOOL'
NULL = 'NULL'

LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
LSBRAC = 'LSBRAC'
RSBRAC = 'RSBRAC'
LBRAC = 'LBRAC'
RBRAC = 'RBRAC'
COLON = 'COLON'
COMMA = 'COMMA'
EOF = 'EOF'


class ParseException(Exception):
    pass


class CharacterException(ParseException):
    pass


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token({type},{value})".format(type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[0]
        self.end = len(text)
        self.current_row = 1
        self.current_col = 1

    def error(self):
        raise CharacterException(
            "Invaild character {char} at row:{row},col:{col} ".format(char=self.current_char, row=self.current_row, col=self.current_col))

    def advance(self):
        if self.current_char == '\n':
            self.current_row += 1
            self.current_col = 0
        self.pos += 1
        if self.pos < self.end:
            self.current_col += 1
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def peek(self):
        pos = self.pos+1
        if pos < self.end:
            return self.text[pos]
        else:
            return None

    def skip_empty(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def string(self):
        result = ''
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\' and self.peek():
                # todo: escape character
                result += self.current_char
                self.advance()
            result += self.current_char
            self.advance()
        self.advance()
        return result

    def number(self):
        result = ''
        is_float = False
        if self.current_char == '-':
            result += self.current_char
            self.advance()
        if not self.current_char.isdigit():
            self.error()
        if self.current_char != '0':
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        else:
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            is_float = True
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        if self.current_char.lower() == 'e':
            is_float = True
            result += self.current_char
            self.advance()
            if self.current_char == '+' or self.current_char == '-':
                result += self.current_char
                self.advance()
            if not self.current_char.isdigit():
                self.error()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
        return float(result) if is_float else int(result)

    def bool(self, flag):
        string = 'true' if flag else 'false'
        self.match(string)
        return flag

    def null(self):
        self.match('null')
        return None

    def match(self, string):
        for c in string:
            if self.current_char != c:
                self.error()
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_empty()
                continue
            if self.current_char == '{':
                self.advance()
                return Token(LBRAC)
            if self.current_char == '}':
                self.advance()
                return Token(RBRAC)
            if self.current_char == '[':
                self.advance()
                return Token(LSBRAC)
            if self.current_char == ']':
                self.advance()
                return Token(RSBRAC)
            if self.current_char == ':':
                self.advance()
                return Token(COLON)
            if self.current_char == ',':
                self.advance()
                return Token(COMMA)
            if self.current_char == 'f':
                return Token(BOOL, self.bool(False))
            if self.current_char == 't':
                return Token(BOOL, self.bool(True))
            if self.current_char == 'n':
                return Token(NULL, self.null())
            if self.current_char == '"':
                return Token(STRING, self.string())
            if self.current_char == '-' or self.current_char.isdigit():
                return Token(NUMBER, self.number())
            self.error()
        return Token(EOF)


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise ParseException('Invalid syntax .token:{token} ,row:{row},col:{col}'.format(
            token=self.current_token, row=self.lexer.current_row, col=self.lexer.current_col))

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def key(self):
        token = self.current_token
        self.eat(STRING)
        return token.value

    def value(self):
        token = self.current_token
        if token.type == LBRAC:
            return self.object()
        if token.type == LSBRAC:
            return self.array()
        if token.type in (STRING, NUMBER, BOOL, NULL):
            self.eat(token.type)
            return token.value

    def array(self):
        self.eat(LSBRAC)
        result = []
        while self.current_token.type != RSBRAC:
            result.append(self.value())
            if self.current_token.type == RSBRAC:
                break
            self.eat(COMMA)
        self.eat(RSBRAC)
        return result

    def object(self):
        self.eat(LBRAC)
        result = OrderedDict()
        while self.current_token.type != RBRAC:
            key = self.key()
            self.eat(COLON)
            result[key] = self.value()
            if self.current_token.type == RBRAC:
                break
            self.eat(COMMA)
        self.eat(RBRAC)
        return result

    def parse(self):
        result = None
        if self.current_token.type == LBRAC:
            result = self.object()
        elif self.current_token.type == LSBRAC:
            result = self.array()
        elif self.current_token.type in (STRING, NUMBER, BOOL, NULL):
            result = self.value()
        self.eat(EOF)
        return result


def load_from_text(text):
    if len(text) == 0:
        return None
    lexer = Lexer(text)
    parser = Parser(lexer)
    return parser.parse()


def load_from_file(filename):
    with open(filename) as f:
        return load_from_text(f.read())


def test():
    import glob
    pattern = './test/pass*.json'
    filename_list = glob.glob(pattern)
    for filename in filename_list:
        result = load_from_file(filename)


if __name__ == '__main__':
    test()
