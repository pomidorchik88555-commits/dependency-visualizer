from errors import *


class DependencyGraph:
    def __init__(self):
        self.visited = set()
        self.dependencies = {}
        self.cycle_detected = False

    def build_graph_bfs(self, start_package, get_dependencies_func, max_depth=10):
        """Строит граф зависимостей используя BFS с рекурсией"""
        self.visited = set()
        self.dependencies = {}
        self.cycle_detected = False

        queue = [(start_package, 0)]  # (package, depth)

        while queue:
            current_package, depth = queue.pop(0)

            if depth > max_depth:
                print(f"Достигнута максимальная глубина {max_depth} для {current_package}")
                continue

            if current_package in self.visited:
                if current_package in self.dependencies:
                    print(f"Обнаружен цикл или повтор: {current_package}")
                    self.cycle_detected = True
                continue

            self.visited.add(current_package)
            print(f"Анализируем зависимости: {current_package} (глубина {depth})")

            try:
                # Получаем зависимости текущего пакета
                deps = get_dependencies_func(current_package)
                self.dependencies[current_package] = deps

                # Добавляем зависимости в очередь для дальнейшего анализа
                for dep in deps.keys():
                    if dep not in self.visited:
                        queue.append((dep, depth + 1))

            except Exception as e:
                print(f"Ошибка при анализе {current_package}: {e}")
                self.dependencies[current_package] = {}

    def get_graph(self):
        """Возвращает построенный граф зависимостей"""
        return self.dependencies

    def has_cycles(self):
        """Проверяет наличие циклов в графе"""
        return self.cycle_detected

    def display_graph(self):
        """Выводит граф в читаемом формате"""
        print("\nГРАФ ЗАВИСИМОСТЕЙ")
        for package, deps in self.dependencies.items():
            if deps:
                dep_list = ", ".join(deps.keys())
                print(f" {package} → {dep_list}")
            else:
                print(f" {package} → нет зависимостей")

        if self.cycle_detected:
            print("В графе обнаружены циклы")