#!/usr/bin/env python3
"""
Демонстрация визуализации для 3 различных пакетов
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.dependency_graph import DependencyGraph
from src.visualizer import DependencyVisualizer
from src.ascii_tree import generate_ascii_tree


def main():
    # Примеры графов для демонстрации
    demo_graphs = {
        "react": {
            "react": ["prop-types", "loose-envify"],
            "prop-types": [],
            "loose-envify": ["js-tokens"],
            "js-tokens": []
        },
        "express": {
            "express": ["accepts", "body-parser", "content-type", "cookie", "debug"],
            "accepts": ["mime-types", "negotiator"],
            "mime-types": ["mime-db"],
            "body-parser": ["bytes", "content-type", "debug", "depd"]
        },
        "webpack": {
            "webpack": ["webpack-cli", "tapable", "schema-utils"],
            "webpack-cli": ["commander", "cross-spawn"],
            "tapable": [],
            "schema-utils": ["ajv"]
        }
    }

    output_dir = "visualization_examples"
    os.makedirs(output_dir, exist_ok=True)

    print("Демонстрация визуализации зависимостей")
    print("=" * 50)

    for package_name, graph_data in demo_graphs.items():
        print(f"\n📦 Пакет: {package_name}")
        print("-" * 30)

        graph = DependencyGraph(graph_data)
        visualizer = DependencyVisualizer(graph)

        # ASCII дерево
        ascii_tree = generate_ascii_tree(graph.dependencies, package_name)
        ascii_file = os.path.join(output_dir, f"{package_name}_ascii.txt")
        with open(ascii_file, 'w', encoding='utf-8') as f:
            f.write(ascii_tree)
        print(f"✓ ASCII дерево: {ascii_file}")

        # PlantUML
        plantuml_code = visualizer.generate_plantuml(package_name)
        plantuml_file = os.path.join(output_dir, f"{package_name}.puml")
        with open(plantuml_file, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)
        print(f"✓ PlantUML код: {plantuml_file}")

        # Изображение
        image_file = os.path.join(output_dir, f"{package_name}.png")
        visualizer.save_plantuml_image(package_name, image_file)

        # Сравнение
        comparison = visualizer.compare_with_native_tools(package_name)
        comparison_file = os.path.join(output_dir, f"{package_name}_comparison.txt")

        with open(comparison_file, 'w', encoding='utf-8') as f:
            f.write(f"Сравнение для {package_name}\n")
            f.write(f"Наши зависимости: {len(comparison['our_dependencies'])}\n")
            f.write(f"Штатные зависимости: {len(comparison['native_dependencies'])}\n")
            f.write(
                f"Расхождения: {len(comparison['differences']['missing_in_native']) + len(comparison['differences']['missing_in_our'])}\n")

        print(f"✓ Сравнение: {comparison_file}")

    print(f"\n🎉 Демонстрация завершена! Результаты в: {output_dir}")


if __name__ == "__main__":
    main()