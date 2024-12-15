class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_position = 0

    def parse(self):
        ast = []
        while self.current_position < len(self.tokens):
            token = self.tokens[self.current_position]
            if token[0] == "NEWLINE":
                self.current_position += 1  
                continue
            ast.append(self.statement())
        return ast

    def statement(self):
        token = self.tokens[self.current_position]
        if token[0] == "ID" and self.tokens[self.current_position + 1][0] == "LPAREN":
            return self.function_call()
        elif token[0] == "ID":
            return self.assignment()
        elif token[0] == "DEF":
            return self.function_definition()
        elif token[0] == "IF":
            return self.conditional()
        elif token[0] == "FOR":
            return self.loop()
        elif token[0] == "RETURN":
            self.consume("RETURN")
            value = self.expression()
            return {"type": "return", "value": value}
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def assignment(self):
        var_name = self.consume("ID")[1]
        token = self.tokens[self.current_position]
        if token[0] == "ASSIGN":
            self.consume("ASSIGN")
            expr = self.expression()
            return {"type": "assignment", "name": var_name, "value": expr}
        elif token[0] == "COMPOUND_ASSIGN":
            operator = self.consume("COMPOUND_ASSIGN")[1]
            expr = self.expression()
            return {"type": "compound_assignment", "operator": operator, "name": var_name, "value": expr}
        else:
            raise SyntaxError(f"Unexpected token in assignment: {token}")

    def function_definition(self):
        self.consume("DEF")
        func_name = self.consume("ID")[1]
        self.consume("LPAREN")
        parameters = []
        while self.tokens[self.current_position][0] != "RPAREN":
            param = self.consume("ID")[1]
            parameters.append(param)
            if self.tokens[self.current_position][0] == "COMMA":
                self.consume("COMMA")
        self.consume("RPAREN")
        self.consume("COLON")
        body = self.function_body()
        return {"type": "function", "name": func_name, "parameters": parameters, "body": body}

    def function_body(self):
        statements = []
        while self.current_position < len(self.tokens):
            token = self.tokens[self.current_position]
            if token[0] == "NEWLINE":
                self.current_position += 1  
                continue
            if token[0] in {"ELSE", "END"}:  
                break
            statements.append(self.statement())
        return statements


    def conditional(self):
        self.consume("IF")
        condition = self.expression()
        self.consume("COLON")
        if_body = self.function_body()
        else_body = None
        if self.current_position < len(self.tokens) and self.tokens[self.current_position][0] == "ELSE":
            self.consume("ELSE")
            self.consume("COLON")
            else_body = self.function_body()
        return {"type": "if", "condition": condition, "if_body": if_body, "else_body": else_body}


    def loop(self):
        self.consume("FOR")  
        iterator = self.consume("ID")[1]  
        self.consume("IN")  
        iterable = self.expression()  
        self.consume("COLON")  
        body = self.function_body()  
        return {"type": "for", "iterator": iterator, "iterable": iterable, "body": body}

    def function_call(self):
        func_name = self.consume("ID")[1]
        self.consume("LPAREN")
        args = []
        while self.tokens[self.current_position][0] != "RPAREN":
            args.append(self.expression())
            if self.tokens[self.current_position][0] == "COMMA":
                self.consume("COMMA")
        self.consume("RPAREN")
        return {"type": "call", "name": func_name, "arguments": args}

    def expression(self):
        return self.parse_expression()

    def parse_expression(self):
        left = self.term()
        while self.current_position < len(self.tokens) and self.tokens[self.current_position][0] in {"OP", "LOGICAL_OP", "COMPARISON"}:
            op = self.consume(self.tokens[self.current_position][0])[1]
            right = self.term()
            left = {"type": "binary_operation", "operator": op, "left": left, "right": right}
        return left



    def term(self):
        token = self.tokens[self.current_position]
        if token[0] == "NUMBER":
            return {"type": "literal", "value": self.consume("NUMBER")[1]}
        elif token[0] == "ID":
            if self.tokens[self.current_position + 1][0] == "LPAREN":
                return self.function_call()
            return {"type": "variable", "value": self.consume("ID")[1]}
        elif token[0] == "LBRACKET":
            elements = []
            self.consume("LBRACKET")
            while self.tokens[self.current_position][0] != "RBRACKET":
                elements.append(self.expression())  
                if self.tokens[self.current_position][0] == "COMMA":
                    self.consume("COMMA")
            self.consume("RBRACKET")
            return {"type": "list", "elements": elements}
        elif token[0] == "LPAREN":
            self.consume("LPAREN")
            expr = self.parse_expression()
            self.consume("RPAREN")
            return expr
        else:
            raise SyntaxError(f"Unexpected token in term: {token}")


        
    def parse_list(self):
        self.consume("LBRACKET")  
        elements = []
        while self.tokens[self.current_position][0] != "RBRACKET":
            elements.append(self.expression())  
            if self.tokens[self.current_position][0] == "COMMA":
                self.consume("COMMA")  
        self.consume("RBRACKET")    
        return {"type": "list", "elements": elements}




    def consume(self, expected_type):
        token = self.tokens[self.current_position]
        print(f"Consuming: {token}, Expected: {expected_type}")  
        if token[0] != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {token[0]}")
        self.current_position += 1
        return token
    
    
