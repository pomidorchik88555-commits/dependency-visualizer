class DependencyGraph:
    def __init__(self, dependencies=None):
        self.dependencies = dependencies or {}

    def add_dependency(self, package: str, dependency: str):
        if package not in self.dependencies:
            self.dependencies[package] = []
        if dependency not in self.dependencies[package]:
            self.dependencies[package].append(dependency)

    def get_dependencies(self, package: str):
        return self.dependencies.get(package, [])

    def to_dict(self):
        return self.dependencies