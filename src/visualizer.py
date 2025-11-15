import os
import subprocess
from typing import Dict, Set


class DependencyVisualizer:
    def __init__(self, dependency_graph):
        self.graph = dependency_graph

    def generate_plantuml(self, root_package: str) -> str:
        lines = ["@startuml", "skinparam monochrome true", "left to right direction"]

        visited = set()

        def add_dependencies(pkg: str, depth: int = 0):
            if pkg in visited or depth > 10:
                return
            visited.add(pkg)

            if hasattr(self.graph, 'dependencies') and pkg in self.graph.dependencies:
                for dep in self.graph.dependencies[pkg]:
                    lines.append(f'["{pkg}"] --> ["{dep}"]')
                    add_dependencies(dep, depth + 1)
            elif hasattr(self.graph, 'get_graph'):
                deps = self.graph.get_graph().get(pkg, [])
                for dep in deps:
                    lines.append(f'["{pkg}"] --> ["{dep}"]')
                    add_dependencies(dep, depth + 1)

        add_dependencies(root_package)
        lines.append("@enduml")
        return "\n".join(lines)

    def save_plantuml_image(self, root_package: str, output_path: str):
        plantuml_code = self.generate_plantuml(root_package)
        puml_file = output_path.replace('.png', '.puml')
        with open(puml_file, 'w') as f:
            f.write(plantuml_code)
        print(f"PlantUML код сохранен: {puml_file}")
        print("Для создания PNG используйте: https://www.plantuml.com/plantuml/uml/")

    def compare_with_native_tools(self, root_package: str) -> Dict:
        our_deps = set()

        if hasattr(self.graph, 'dependencies') and root_package in self.graph.dependencies:
            our_deps = set(self.graph.dependencies[root_package])
        elif hasattr(self.graph, 'get_graph'):
            graph_data = self.graph.get_graph()
            our_deps = set(graph_data.get(root_package, []))

        return {
            'package': root_package,
            'our_dependencies': our_deps,
            'native_dependencies': set(),
            'differences': {
                'missing_in_native': list(our_deps),
                'missing_in_our': [],
                'version_differences': []
            }
        }