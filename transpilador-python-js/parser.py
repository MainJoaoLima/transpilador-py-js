class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_position = 0

    def parse(self):
        ast = []
        while self.current_position < len(self.tokens):
            token = self.peek()
            if token[0] == "NEWLINE":
                self.advance()
                continue
            ast.append(self.statement())
        return ast

    def statement(self):
        token = self.peek()
        if token[0] == "DEF":
            return self.function_definition()
        elif token[0] == "RETURN":
            self.consume("RETURN")
            return {"type": "return", "value": self.expression()}
        elif token[0] == "IF":
            return self.conditional()
        elif token[0] == "ID":
            if self.lookahead(1) and self.lookahead(1)[0] == "LPAREN":
                return self.function_call()
            return self.assignment()
        elif token[0] == "FOR":
            return self.loop()
        elif token[0] == "COLON":
            self.error("Unexpected colon outside of valid structure.")
        self.error(f"Unexpected token: {token}")


    def peek(self):
        if self.current_position < len(self.tokens):
            return self.tokens[self.current_position]
        return ("EOF", None)
    
    def consume(self, expected_type):
        token = self.peek()
        if token[0] != expected_type:
            self.error(f"Expected {expected_type}, got {token[0]}")
        self.advance()
        return token
    
    def advance(self):
        self.current_position += 1

    def lookahead(self, n):
        pos = self.current_position + n
        if pos < len(self.tokens):
            return self.tokens[pos]
        return ("EOF", None)

    def error(self, message):
        token = self.peek()
        raise SyntaxError(f"{message} at token {token}")
    
    def assignment(self):
        var_name = self.consume("ID")[1]  
        token = self.peek()
        if token[0] == "ASSIGN":
            self.consume("ASSIGN")
            expr = self.expression()  
            return {"type": "assignment", "name": var_name, "value": expr}
        elif token[0] == "COMPOUND_ASSIGN":
            operator = self.consume("COMPOUND_ASSIGN")[1]
            expr = self.expression()
            return {"type": "compound_assignment", "name": var_name, "operator": operator, "value": expr}
        else:
            self.error(f"Unexpected token in assignment: {token}")

    def expression(self):
        return self.parse_expression()

    def parse_expression(self):
        left = self.term()
        while self.current_position < len(self.tokens) and self.peek()[0] in {"OP", "LOGICAL_OP", "COMPARISON"}:
            op = self.consume(self.peek()[0])[1]
            right = self.term()
            left = {"type": "binary_operation", "operator": op, "left": left, "right": right}
        return left

    def term(self):
        token = self.peek()
        if token[0] == "NUMBER":
            return {"type": "literal", "value": self.consume("NUMBER")[1]}
        elif token[0] == "ID":
            if self.lookahead(1) and self.lookahead(1)[0] == "LPAREN":
                return self.function_call()  
            return {"type": "variable", "value": self.consume("ID")[1]}
        elif token[0] == "LPAREN":
            self.consume("LPAREN")
            expr = self.parse_expression()
            self.consume("RPAREN")
            return expr
        elif token[0] == "LBRACKET":  
            return self.parse_list()
        else:
            self.error(f"Unexpected token in term: {token}")

    def parse_list(self):
        self.consume("LBRACKET")  
        elements = []
        while self.peek()[0] != "RBRACKET":
            elements.append(self.expression())  
            if self.peek()[0] == "COMMA":
                self.consume("COMMA")  
        self.consume("RBRACKET")  
        return {"type": "list", "elements": elements}


    def function_definition(self):
        self.consume("DEF")
        func_name = self.consume("ID")[1]
        self.consume("LPAREN")
        parameters = []

        
        while self.peek()[0] != "RPAREN":
            param = self.consume("ID")[1]
            parameters.append(param)
            if self.peek()[0] == "COMMA":
                self.consume("COMMA")
        self.consume("RPAREN")
        self.consume("COLON")

        
        body = self.parse_block()
        return {"type": "function", "name": func_name, "parameters": parameters, "body": body}

    
    def parse_block(self, end_tokens=None):
        if end_tokens is None:
            end_tokens = {"DEDENT", "EOF", "ELSE"}
        block = []
        while self.current_position < len(self.tokens):
            token = self.peek()
            if token[0] == "NEWLINE":
                self.advance()  
                continue
            if token[0] in end_tokens:  
                break
            block.append(self.statement())
        return block



    def conditional(self):
        self.consume("IF")  
        condition = self.expression()  
        self.consume("COLON")  
        if_body = self.parse_block()  

        
        else_body = None
        if self.current_position < len(self.tokens) and self.peek()[0] == "ELSE":
            self.consume("ELSE")  
            self.consume("COLON")  
            else_body = self.parse_block()  

        return {
            "type": "if",
            "condition": condition,
            "if_body": if_body,
            "else_body": else_body
        }
    
    def loop(self):
        self.consume("FOR")  
        iterator = self.consume("ID")[1]  
        self.consume("IN")  
        iterable = self.expression()  
        self.consume("COLON")  
        body = self.parse_block()  

        return {
            "type": "for",
            "iterator": iterator,
            "iterable": iterable,
            "body": body,
        }

    def function_call(self):
        func_name = self.consume("ID")[1]  
        self.consume("LPAREN")  
        
        arguments = []
        while self.peek()[0] != "RPAREN":  
            arguments.append(self.expression())  
            if self.peek()[0] == "COMMA":  
                self.consume("COMMA")
        self.consume("RPAREN")  
        
        return {
            "type": "call",
            "name": func_name,
            "arguments": arguments,
        }

