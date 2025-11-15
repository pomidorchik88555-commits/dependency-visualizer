def print_ascii_tree(dependency_graph, root_package: str, prefix: str = "", is_last: bool = True):
    connector = "└── " if is_last else "├── "
    print(prefix + connector + root_package)

    if is_last:
        new_prefix = prefix + "    "
    else:
        new_prefix = prefix + "│   "

    deps = []
    if hasattr(dependency_graph, 'get'):
        deps = dependency_graph.get(root_package, [])
    elif hasattr(dependency_graph, 'dependencies'):
        deps = dependency_graph.dependencies.get(root_package, [])

    for i, dep in enumerate(deps):
        is_last_dep = (i == len(deps) - 1)
        if dep != root_package:
            print_ascii_tree(dependency_graph, dep, new_prefix, is_last_dep)


def generate_ascii_tree(dependency_graph, root_package: str) -> str:
    import io
    import contextlib
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        print_ascii_tree(dependency_graph, root_package)
    return output.getvalue()