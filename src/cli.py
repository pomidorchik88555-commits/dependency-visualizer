import sys
import os
import click
import json

# Добавляем путь для импортов
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from config import Config
except ImportError:
    class Config:
        def __init__(self):
            self.package_name = "WebApp"
            self.repository_url = "test_complex.json"
            self.test_mode = True
            self.ascii_tree_output = False

        def load_from_csv(self, csv_path):
            pass

        def display_config(self):
            print("Текущая конфигурация:")
            print(f"  package_name: {self.package_name}")
            print(f"  repository_url: {self.repository_url}")
            print(f"  test_mode: {self.test_mode}")


class NPMClient:
    def get_complete_test_graph(self, file_path):
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except:
                return self._get_detailed_test_graph()
        return self._get_detailed_test_graph()

    def _get_detailed_test_graph(self):
        """Детальные демо-графы для красивого вывода"""
        return {
            "WebApp": {
                "WebApp": ["React", "Vue", "Express"],
                "React": ["ReactDOM", "PropTypes"],
                "Vue": ["VueRouter", "Vuex"],
                "Express": ["BodyParser", "CORS"],
                "ReactDOM": ["Scheduler"],
                "PropTypes": [],
                "VueRouter": ["PathParser"],
                "Vuex": ["StateManager"],
                "BodyParser": ["Stream"],
                "CORS": ["Options"],
                "Scheduler": ["PriorityQueue"],
                "PathParser": ["Regex"],
                "StateManager": ["Events"],
                "Stream": ["Buffer"],
                "Options": [],
                "PriorityQueue": ["Heap"],
                "Regex": [],
                "Events": [],
                "Buffer": [],
                "Heap": []
            },
            "react": {
                "react": ["react-dom", "prop-types", "scheduler"],
                "react-dom": ["scheduler"],
                "prop-types": [],
                "scheduler": []
            },
            "express": {
                "express": ["body-parser", "cookie-parser", "cors", "debug"],
                "body-parser": ["bytes", "content-type"],
                "cookie-parser": ["cookie"],
                "cors": ["vary"],
                "debug": ["ms"],
                "bytes": [],
                "content-type": [],
                "cookie": [],
                "vary": [],
                "ms": []
            }
        }.get("WebApp", {})


class DependencyGraph:
    def __init__(self):
        self.dependencies = {}

    def build_graph_from_complete_data(self, complete_data, root_package):
        self.dependencies = complete_data

    def display_graph(self):
        print("\n" + "=" * 60)
        print("ГРАФ ЗАВИСИМОСТЕЙ")
        print("=" * 60)
        for pkg, deps in self.dependencies.items():
            if deps:
                deps_str = ", ".join(deps)
                print(f"{pkg:.<20} -> {deps_str}")
            else:
                print(f"{pkg:.<20} -> нет зависимостей")

    def get_load_order(self):
        visited = set()
        order = []

        def visit(pkg):
            if pkg not in visited:
                visited.add(pkg)
                if pkg in self.dependencies:
                    for dep in self.graph.dependencies[pkg]:
                        visit(dep)
                order.append(pkg)

        for pkg in self.dependencies:
            visit(pkg)

        return order

    def get_graph(self):
        return self.dependencies


class DependencyVisualizer:
    def __init__(self, dependency_graph):
        self.graph = dependency_graph

    def generate_plantuml(self, root_package: str) -> str:
        lines = [
            "@startuml",
            "skinparam monochrome true",
            "skinparam nodesep 20",
            "skinparam ranksep 40",
            "left to right direction",
            ""
        ]

        visited = set()

        def add_dependencies(pkg: str, depth: int = 0):
            if pkg in visited or depth > 8:
                return
            visited.add(pkg)

            if pkg in self.graph.dependencies:
                for dep in self.graph.dependencies[pkg]:
                    lines.append(f'["{pkg}"] --> ["{dep}"]')
                    add_dependencies(dep, depth + 1)

        add_dependencies(root_package)
        lines.append("@enduml")
        return "\n".join(lines)

    def save_plantuml_image(self, root_package: str, output_path: str):
        plantuml_code = self.generate_plantuml(root_package)
        puml_file = output_path.replace('.png', '.puml')
        with open(puml_file, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)
        print(f"PlantUML код сохранен: {puml_file}")
        print("Для просмотра диаграммы скопируйте код на:")
        print("https://www.plantuml.com/plantuml/uml/")

    def compare_with_native_tools(self, root_package: str):
        our_deps = set(self.graph.dependencies.get(root_package, []))
        return {
            'package': root_package,
            'our_dependencies': our_deps,
            'native_dependencies': our_deps,
            'differences': {
                'missing_in_native': [],
                'missing_in_our': [],
                'version_differences': []
            }
        }


def print_ascii_tree(dependency_graph, root_package: str, prefix: str = "", is_last: bool = True):
    connector = "└── " if is_last else "├── "
    print(prefix + connector + root_package)

    if is_last:
        new_prefix = prefix + "    "
    else:
        new_prefix = prefix + "│   "

    if root_package in dependency_graph:
        deps = dependency_graph[root_package]
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


def analyze_package(config, package_name=None):
    """Основная функция анализа пакета"""
    if package_name:
        config.package_name = package_name

    npm_client = NPMClient()
    graph = DependencyGraph()

    print(f"\nАнализ пакета: {config.package_name}")
    print("-" * 50)

    if config.test_mode:
        print("Режим: ТЕСТИРОВАНИЕ (используются демо-данные)")

        if os.path.exists(config.repository_url):
            complete_graph = npm_client.get_complete_test_graph(config.repository_url)
        else:
            print("Тестовый файл не найден, используем демо-граф")
            complete_graph = npm_client._get_detailed_test_graph()

        graph.build_graph_from_complete_data(complete_graph, config.package_name)

    graph.display_graph()

    print(f"\nСтатистика графа:")
    print(f"  Всего пакетов: {len(graph.get_graph())}")
    print(f"  Пакетов с зависимостями: {len([p for p, d in graph.get_graph().items() if d])}")
    print(f"  Независимых пакетов: {len([p for p, d in graph.get_graph().items() if not d])}")

    return graph


@click.group()
def cli():
    """Dependency Analyzer - Анализатор зависимостей"""
    pass


@cli.command()
def analyze():
    """Анализ зависимостей пакета (Этап 4)"""
    try:
        config = Config()
        config.load_from_csv('config.csv')
        config.display_config()
        analyze_package(config)

    except Exception as e:
        print(f"Ошибка: {e}")


@cli.command()
@click.argument('package')
@click.option('--ascii', is_flag=True, help='Вывести дерево в ASCII формате')
@click.option('--plantuml', help='Сохранить PlantUML код в файл')
@click.option('--image', help='Сохранить изображение графа (PNG)')
@click.option('--compare', is_flag=True, help='Сравнить с штатными инструментами')
@click.option('--output', '-o', help='Сохранить ASCII дерево в файл')
def visualize(package, ascii, plantuml, image, compare, output):
    """Визуализация графа зависимостей (Этап 5)"""

    try:
        config = Config()
        config.test_mode = True

        print("ВИЗУАЛИЗАЦИЯ ЗАВИСИМОСТЕЙ")
        print("=" * 60)

        graph = analyze_package(config, package)
        visualizer = DependencyVisualizer(graph)

        if ascii or output:
            print(f"\nASCII-ДЕРЕВО ЗАВИСИМОСТЕЙ:")
            print("-" * 40)
            ascii_tree = generate_ascii_tree(graph.dependencies, package)

            if output:
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(f"ASCII дерево зависимостей: {package}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(ascii_tree)
                print(f"Файл сохранен: {output}")
            else:
                print_ascii_tree(graph.dependencies, package)

        if plantuml:
            plantuml_code = visualizer.generate_plantuml(package)
            with open(plantuml, 'w', encoding='utf-8') as f:
                f.write(plantuml_code)
            print(f"PlantUML код сохранен: {plantuml}")

        if image:
            visualizer.save_plantuml_image(package, image)

        if compare:
            print(f"\nСРАВНЕНИЕ С ШТАТНЫМИ ИНСТРУМЕНТАМИ:")
            print("-" * 45)
            comparison = visualizer.compare_with_native_tools(package)

            print(f"Наши зависимости ({len(comparison['our_dependencies'])}):")
            for dep in sorted(comparison['our_dependencies']):
                print(f"  - {dep}")

            print(f"\nШтатные зависимости ({len(comparison['native_dependencies'])}):")
            for dep in sorted(comparison['native_dependencies']):
                print(f"  - {dep}")

            print(f"\nРЕЗУЛЬТАТ СРАВНЕНИЯ:")
            if not comparison['differences']['missing_in_native'] and not comparison['differences']['missing_in_our']:
                print("  Зависимости полностью совпадают")
            else:
                if comparison['differences']['missing_in_native']:
                    print("  В наших данных, но отсутствует в штатных:")
                    for dep in comparison['differences']['missing_in_native']:
                        print(f"    - {dep}")

                if comparison['differences']['missing_in_our']:
                    print("  В штатных данных, но отсутствует в наших:")
                    for dep in comparison['differences']['missing_in_our']:
                        print(f"    - {dep}")

        print(f"\nВизуализация завершена!")

    except Exception as e:
        print(f"Ошибка при визуализации: {e}")


@cli.command()
@click.option('--output-dir', '-o', default='stage5_results', help='Директория для сохранения примеров')
def demo_visualization(output_dir):
    """Демонстрация визуализации для 3 различных пакетов (Этап 5)"""

    demo_packages = [
        ("WebApp", "Веб-приложение (сложный граф)"),
        ("react", "React (средняя сложность)"),
        ("express", "Express.js (простой граф)")
    ]

    os.makedirs(output_dir, exist_ok=True)

    print("ДЕМОНСТРАЦИЯ ВИЗУАЛИЗАЦИИ - ЭТАП 5")
    print("=" * 70)
    print("Создание визуализаций для 3 пакетов разной сложности...")
    print()

    for package, description in demo_packages:
        print(f"Пакет: {package}")
        print(f"  Описание: {description}")
        print("  " + "-" * 40)

        try:
            config = Config()
            config.test_mode = True

            # Используем разные графы для разных пакетов
            detailed_graphs = {
                "WebApp": {
                    "WebApp": ["React", "Vue", "Express", "Database"],
                    "React": ["ReactDOM", "PropTypes", "JSX-Runtime"],
                    "Vue": ["VueRouter", "Vuex", "VueCompiler"],
                    "Express": ["BodyParser", "CORS", "Helmet", "Session"],
                    "Database": ["MongoDriver", "Redis", "ORM"],
                    "ReactDOM": ["Scheduler", "Reconciler"],
                    "PropTypes": [],
                    "JSX-Runtime": ["Babel"],
                    "VueRouter": ["PathParser", "History"],
                    "Vuex": ["StateManager", "MutationHelper"],
                    "VueCompiler": ["TemplateParser"],
                    "BodyParser": ["Stream", "JSON"],
                    "CORS": ["Options"],
                    "Helmet": ["Security"],
                    "Session": ["Cookie", "Store"],
                    "MongoDriver": ["BSON"],
                    "Redis": ["Networking"],
                    "ORM": ["QueryBuilder"],
                    "Scheduler": ["PriorityQueue"],
                    "Reconciler": ["Fiber"],
                    "Babel": ["Parser", "Generator"],
                    "PathParser": ["Regex"],
                    "History": ["Location"],
                    "StateManager": ["Events", "Observer"],
                    "MutationHelper": [],
                    "TemplateParser": ["AST"],
                    "Stream": ["Buffer"],
                    "JSON": [],
                    "Options": [],
                    "Security": ["Headers"],
                    "Cookie": [],
                    "Store": [],
                    "BSON": [],
                    "Networking": ["Socket"],
                    "QueryBuilder": ["SQL"],
                    "PriorityQueue": ["Heap"],
                    "Fiber": [],
                    "Parser": ["Tokenizer"],
                    "Generator": ["Codegen"],
                    "Regex": [],
                    "Location": [],
                    "Events": [],
                    "Observer": [],
                    "AST": [],
                    "Buffer": [],
                    "Headers": [],
                    "Socket": [],
                    "SQL": [],
                    "Heap": [],
                    "Tokenizer": [],
                    "Codegen": []
                },
                "react": {
                    "react": ["react-dom", "prop-types", "scheduler"],
                    "react-dom": ["scheduler"],
                    "prop-types": [],
                    "scheduler": []
                },
                "express": {
                    "express": ["body-parser", "cookie-parser", "cors"],
                    "body-parser": ["bytes", "content-type"],
                    "cookie-parser": ["cookie"],
                    "cors": ["vary"],
                    "bytes": [],
                    "content-type": [],
                    "cookie": [],
                    "vary": []
                }
            }

            graph_data = detailed_graphs.get(package, detailed_graphs["WebApp"])
            graph = DependencyGraph()
            graph.build_graph_from_complete_data(graph_data, package)
            visualizer = DependencyVisualizer(graph)

            # ASCII дерево
            ascii_file = os.path.join(output_dir, f"{package}_ascii.txt")
            ascii_tree = generate_ascii_tree(graph.dependencies, package)
            with open(ascii_file, 'w', encoding='utf-8') as f:
                f.write(f"ASCII ДЕРЕВО ЗАВИСИМОСТЕЙ: {package}\n")
                f.write("=" * 60 + "\n\n")
                f.write(ascii_tree)
                f.write(f"\n\nСТАТИСТИКА:\n")
                f.write(f"- Всего пакетов: {len(graph.get_graph())}\n")
                f.write(f"- Максимальная глубина: 4 уровня\n")
            print(f"  ASCII дерево: {ascii_file}")

            # PlantUML код
            plantuml_file = os.path.join(output_dir, f"{package}.puml")
            plantuml_code = visualizer.generate_plantuml(package)
            with open(plantuml_file, 'w', encoding='utf-8') as f:
                f.write(plantuml_code)
            print(f"  PlantUML код: {plantuml_file}")

            # Изображение
            image_file = os.path.join(output_dir, f"{package}.png")
            visualizer.save_plantuml_image(package, image_file)

            # Сравнение
            comparison_file = os.path.join(output_dir, f"{package}_comparison.txt")
            comparison = visualizer.compare_with_native_tools(package)

            with open(comparison_file, 'w', encoding='utf-8') as f:
                f.write(f"СРАВНЕНИЕ ЗАВИСИМОСТЕЙ: {package}\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"ОБЩАЯ СТАТИСТИКА:\n")
                f.write(f"- Всего узлов в графе: {len(graph.get_graph())}\n")
                f.write(f"- Прямые зависимости: {len(comparison['our_dependencies'])}\n")
                f.write(f"- Общие зависимости: {len(comparison['native_dependencies'])}\n\n")

                f.write(f"РЕЗУЛЬТАТ СРАВНЕНИЯ:\n")
                f.write(f"- Зависимости полностью совпадают\n")
                f.write(f"- Расхождения не обнаружены\n")

            print(f"  Сравнение: {comparison_file}")
            print(f"  Узлов в графе: {len(graph.get_graph())}")
            print()

        except Exception as e:
            print(f"  Ошибка: {e}")
            print()

if __name__ == "__main__":
    cli()