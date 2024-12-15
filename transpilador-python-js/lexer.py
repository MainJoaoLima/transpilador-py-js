import re

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []

    def tokenize(self):
        token_specification = [
            ("NUMBER", r'\d+(\.\d*)?'),                 # Inteiros 
            ("COMPARISON", r'==|!=|<=|>=|<|>'),         # Operadores de comparação
            ("COMPOUND_ASSIGN", r'\+=|-=|\*=|/=|%='),   # Operadores compostos
            ("ASSIGN", r'='),                           # Atribuição
            ("END", r';'),                              # Fim de linha
            ("IN", r'in'),                              # Palavra-chave 'in'
            ("LOGICAL_OP", r'and|or'),                  # Operadores lógicos (and, or)
            ("ID", r'[A-Za-z_]\w*'),                    # Identificadores
            ("OP", r'[+\-*/%]'),                        # Operadores aritméticos
            ("LPAREN", r'\('),                          # Parêntese esquerdo
            ("RPAREN", r'\)'),                          # Parêntese direito
            ("LBRACKET", r'\['),                        # Colchete esquerdo
            ("RBRACKET", r'\]'),                        # Colchete direito
            ("COLON", r':'),                            # Dois pontos
            ("COMMA", r','),                            # Vírgula
            ("NEWLINE", r'\n'),                         # Nova linha
            ("SKIP", r'[ \t]+'),                        # Espaços
            ("MISMATCH", r'.'),                         # Caracteres não esperados
        ]

        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)

        for match in re.finditer(tok_regex, self.source_code):
            kind = match.lastgroup  
            value = match.group()  
            if kind == "NUMBER":
                value = float(value) if '.' in value else int(value)
            elif kind == "ID" and value in {"if", "else", "for", "while", "def", "return"}:
                kind = value.upper()
            elif kind == "SKIP":
                continue
            elif kind == "MISMATCH":
                raise RuntimeError(f"Unexpected character: {value}")
            self.tokens.append((kind, value))
        return self.tokens
