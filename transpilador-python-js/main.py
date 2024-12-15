import sys
from lexer import Lexer
from parser import Parser
from code_generator import CodeGenerator

def main(input_file, output_file):
    with open(input_file, 'r') as f:
        source_code = f.read()

    lexer = Lexer(source_code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()
    #print("AST Gerado:", ast)  

    generator = CodeGenerator(ast)
    js_code = generator.generate()
    #print("Código JS Gerado:\n",js_code)  


    with open(output_file, 'w') as f:
        f.write(js_code)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_file> <output_file>")
    else:
        main(sys.argv[1], sys.argv[2])
