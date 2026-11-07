def find_paths(data, target):
    def matches(value):
        if isinstance(value, bool) != isinstance(target, bool):
            return False
        return value == target

    results = []

    def walk(node, path):
        if isinstance(node, dict):
            for key, value in node.items():       
                child = f"{path}.{key}" if path else str(key)
                visit(value, child)
        elif isinstance(node, list):
            for i, value in enumerate(node):      
                visit(value, f"{path}[{i}]")

    def visit(value, path):
        if matches(value):
            results.append(path)
        walk(value, path)                           

    walk(data, "")
    return results