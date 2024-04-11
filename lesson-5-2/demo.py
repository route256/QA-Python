import ast

code = """
@allure.id()
def test_some():
    assert False
"""

print(ast.dump(ast.parse(code), indent=2))
