import ast

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

def parse_code(code_str: str) -> dict:
    """Parses python code using AST and returns structured information."""
    try:
        tree = ast.parse(code_str)
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)
        return {
            "functions": analyzer.functions,
            "classes": analyzer.classes,
            "valid_syntax": True
        }
    except SyntaxError as e:
        return {
            "valid_syntax": False,
            "error": str(e)
        }

def get_ast_dump(code_str: str) -> str:
    try:
        tree = ast.parse(code_str)
        return ast.dump(tree, indent=4)
    except Exception:
        return ""
