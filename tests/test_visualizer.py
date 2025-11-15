import unittest
import tempfile
import os
from src.visualizer import DependencyVisualizer
from src.dependency_graph import DependencyGraph
from src.ascii_tree import generate_ascii_tree


class TestVisualizer(unittest.TestCase):
    def setUp(self):
        sample_graph = {
            "react": ["prop-types", "loose-envify"],
            "prop-types": [],
            "loose-envify": ["js-tokens"]
        }
        self.graph = DependencyGraph(sample_graph)
        self.visualizer = DependencyVisualizer(self.graph)

    def test_plantuml_generation(self):
        plantuml_code = self.visualizer.generate_plantuml("react")
        self.assertIn("@startuml", plantuml_code)
        self.assertIn('["react"] --> ["prop-types"]', plantuml_code)
        self.assertIn('["react"] --> ["loose-envify"]', plantuml_code)
        self.assertIn("@enduml", plantuml_code)

    def test_ascii_tree_generation(self):
        ascii_tree = generate_ascii_tree(self.graph.dependencies, "react")
        self.assertIn("react", ascii_tree)
        self.assertIn("prop-types", ascii_tree)
        self.assertIn("loose-envify", ascii_tree)

    def test_comparison_structure(self):
        comparison = self.visualizer.compare_with_native_tools("react")
        self.assertIn('our_dependencies', comparison)
        self.assertIn('native_dependencies', comparison)
        self.assertIn('differences', comparison)


if __name__ == '__main__':
    unittest.main()