import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []

    def tokenize(self):
        token_specification = [
            ("NUMBER", r'\d+(\.\d*)?'),
            ("COMPARISON", r'==|!=|<=|>=|<|>'),
            ("COMPOUND_ASSIGN", r'\+=|-=|\*=|/=|%='),
            ("ASSIGN", r'='),
            ("LOGICAL_OP", r'and|or'),
            ("ID", r'[A-Za-z_]\w*'),
            ("OP", r'[+\-*/%]'),
            ("LPAREN", r'\('),
            ("RPAREN", r'\)'),
            ("COLON", r':'),
            ("COMMA", r','),
            ("LBRACKET", r'\['),  
            ("RBRACKET", r'\]'),  
            ("NEWLINE", r'\n'),
            ("SKIP", r'[ \t]+'),
            ("MISMATCH", r'.'),
        ]

        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)

        for match in re.finditer(tok_regex, self.source_code):
            kind, value = match.lastgroup, match.group()
            if kind == "SKIP":
                continue
            if kind == "MISMATCH":
                raise RuntimeError(f"Unexpected character: {value}")
            if kind == "NUMBER":
                value = float(value) if '.' in value else int(value)
            elif kind == "ID" and value in {"if", "else", "for", "while", "def", "return", "in"}:  # Added 'in'
                kind = value.upper()
            self.tokens.append((kind, value))
        return self.tokens
