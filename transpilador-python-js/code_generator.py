class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast

    def generate(self):
        return "\n".join(self._generate_node(node) for node in self.ast)

    def _generate_node(self, node, indent=""):
        node_type = node["type"]
        if node_type == "function":
            parameters = ", ".join(node["parameters"])
            body = self._generate_block(node["body"], indent + "    ")
            return f"{indent}function {node['name']}({parameters}) {{\n{body}\n{indent}}}"
        elif node_type == "for":
            iterable = self._generate_expression(node["iterable"])
            body = self._generate_block(node["body"], indent + "    ")
            return f"{indent}for (let {node['iterator']} of {iterable}) {{\n{body}\n{indent}}}"
        elif node_type == "if":
            condition = self._generate_expression(node["condition"])
            if_body = self._generate_block(node["if_body"], indent + "    ")
            else_body = ""
            if node.get("else_body"):
                else_body = f"{indent}else {{\n{self._generate_block(node['else_body'], indent + '    ')}\n{indent}}}"
            return f"{indent}if ({condition}) {{\n{if_body}\n{indent}}}{else_body}"
        elif node_type == "return":
            value = self._generate_expression(node["value"])
            return f"{indent}return {value};"
        elif node_type in {"assignment", "compound_assignment"}:
            value = self._generate_expression(node["value"])
            operator = node.get("operator", "=")
            return f"{indent}{node['name']} {operator} {value};"
        elif node_type == "call":
            args = ", ".join(self._generate_expression(arg) for arg in node["arguments"])
            return f"{indent}{node['name']}({args});"
        return ""

    def _generate_block(self, body, indent=""):
        return "\n".join(self._generate_node(statement, indent) for statement in body)



    def _generate_expression(self, expr):
        if expr is None:
            return "null"
        if isinstance(expr, dict):
            if expr["type"] == "literal":
                return str(expr["value"])
            elif expr["type"] == "variable":
                return expr["value"]
            elif expr["type"] == "binary_operation":
                left = self._generate_expression(expr["left"])
                right = self._generate_expression(expr["right"])
                operator = {"and": "&&", "or": "||"}.get(expr["operator"], expr["operator"])
                return f"{left} {operator} {right}"
            elif expr["type"] == "call":
                args = ", ".join(self._generate_expression(arg) for arg in expr["arguments"])
                return f"{expr['name']}({args})"
            elif expr["type"] == "list":
                elements = ", ".join(self._generate_expression(el) for el in expr["elements"])
                return f"[{elements}]"

        return str(expr)
