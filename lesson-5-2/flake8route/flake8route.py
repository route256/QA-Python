from flake8_plugin_utils import Plugin, Visitor, Error


class MissingAllureIdError(Error):
    code = 'FR001'
    message = 'Test must have id tag'


class Flake8RouteAllureVisitor(Visitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def visit_FunctionDef(self, node) -> None:
        if node.name.startswith('test_'):
            decorators = node.decorator_list
            id_present = False
            for decorator in decorators:
                if decorator.func.value.id == 'allure'\
                        and decorator.func.attr == 'id':
                    id_present = True
            if not id_present:
                self.error_from_node(MissingAllureIdError, node)


class Flake8RoutePlugin(Plugin):
    name = 'FlakeRoutePlugin'
    version = '0.0.1'
    visitors = [Flake8RouteAllureVisitor]
