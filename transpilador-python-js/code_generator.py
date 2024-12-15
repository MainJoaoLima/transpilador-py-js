class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast

    def generate(self):
        js_code = []
        for node in self.ast:
            if node["type"] == "assignment":
                value = self.generate_expression(node["value"])
                js_code.append(f"let {node['name']} = {value};")
            elif node["type"] == "compound_assignment":
                value = self.generate_expression(node["value"])
                js_code.append(f"{node['name']} {node['operator']} {value};")
            elif node["type"] == "function":
                parameters = ", ".join(node["parameters"])
                body = self.generate_block(node["body"], indent="    ")
                js_code.append(f"function {node['name']}({parameters}) {{\n{body}\n}}")
            elif node["type"] == "if":
                condition = self.generate_expression(node["condition"])
                if_body = self.generate_block(node["if_body"], indent="    ")
                js_code.append(f"if ({condition}) {{\n{if_body}\n}}")
                if node["else_body"]:
                    else_body = self.generate_block(node["else_body"], indent="    ")
                    js_code.append(f"else {{\n{else_body}\n}}")
            elif node["type"] == "for":
                iterable = self.generate_expression(node["iterable"])
                body = self.generate_block(node["body"], indent="    ")
                js_code.append(f"for (let {node['iterator']} of {iterable}) {{\n{body}\n}}")
        return "\n".join(js_code)

    def generate_block(self, body, indent=""):
        js_body = []
        for statement in body:
            if statement["type"] == "assignment":
                value = self.generate_expression(statement["value"])
                js_body.append(f"{indent}{statement['name']} = {value};")
            elif statement["type"] == "compound_assignment":
                value = self.generate_expression(statement["value"])
                js_body.append(f"{indent}{statement['name']} {statement['operator']} {value};")
            elif statement["type"] == "return":
                value = self.generate_expression(statement["value"])
                js_body.append(f"{indent}return {value};")
            elif statement["type"] == "if":
                condition = self.generate_expression(statement["condition"])
                if_body = self.generate_block(statement["if_body"], indent + "    ")
                js_body.append(f"{indent}if ({condition}) {{\n{if_body}\n{indent}}}")
                if statement["else_body"]:
                    else_body = self.generate_block(statement["else_body"], indent + "    ")
                    js_body.append(f"{indent}else {{\n{else_body}\n{indent}}}")
            elif statement["type"] == "for":
                iterable = self.generate_expression(statement["iterable"])
                body = self.generate_block(statement["body"], indent + "    ")
                js_body.append(f"{indent}for (let {statement['iterator']} of {iterable}) {{\n{body}\n{indent}}}")
        return "\n".join(js_body)

    def generate_expression(self, expr):
        if expr is None:
            return "null"
        if isinstance(expr, dict):
            if expr["type"] == "literal":
                return str(expr["value"])
            elif expr["type"] == "variable":
                return expr["value"]
            elif expr["type"] == "binary_operation":
                left = self.generate_expression(expr["left"])
                right = self.generate_expression(expr["right"])
                operator = expr["operator"]
                if operator == "and":
                    operator = "&&"
                elif operator == "or":
                    operator = "||"
                return f"({left} {operator} {right})"
            elif expr["type"] == "list":
                elements = ", ".join(self.generate_expression(el) for el in expr["elements"])
                return f"[{elements}]"
        return str(expr)