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

        queue = [(start_package, 0)]

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
                deps = get_dependencies_func(current_package)
                self.dependencies[current_package] = deps

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
                print(f"{package} -> {dep_list}")
            else:
                print(f"{package} -> нет зависимостей")

        if self.cycle_detected:
            print("В графе обнаружены циклы")

    def get_load_order(self):
        """Возвращает порядок загрузки зависимостей (топологическая сортировка)"""
        if not self.dependencies:
            return []

        # Собираем ВСЕ пакеты из графа
        all_packages = set(self.dependencies.keys())
        for deps in self.dependencies.values():
            all_packages.update(deps.keys())

        # Создаем граф в правильном направлении: зависимость -> пакеты, которые от нее зависят
        reverse_graph = {}
        in_degree = {}

        # Инициализируем все пакеты
        for package in all_packages:
            reverse_graph[package] = set()
            in_degree[package] = 0

        # Заполняем зависимости в ПРАВИЛЬНОМ направлении
        # Если A зависит от B, то B должен быть загружен до A
        for package, deps in self.dependencies.items():
            for dep in deps.keys():
                if dep in reverse_graph:
                    reverse_graph[dep].add(package)  # dep -> package (dep должен быть загружен до package)
                    in_degree[package] += 1

        # Пакеты без входящих зависимостей (те, от которых никто не зависит)
        queue = [pkg for pkg in in_degree if in_degree[pkg] == 0]

        # Топологическая сортировка
        load_order = []
        while queue:
            package = queue.pop(0)
            load_order.append(package)

            # Уменьшаем счетчик входящих зависимостей для всех пакетов, которые зависят от этого
            for dependent in reverse_graph[package]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # Проверяем корректность
        if len(load_order) != len(all_packages):
            print("Предупреждение: в графе есть циклы, порядок загрузки может быть неполным")
            remaining = [pkg for pkg in all_packages if pkg not in load_order]
            load_order.extend(remaining)

        return load_order

    def compare_with_npm_behavior(self, start_package):
        """Сравнивает наш порядок загрузки с ожидаемым поведением npm"""
        our_order = self.get_load_order()

        print("\nСРАВНЕНИЕ С NPM")
        print(f"Наш порядок загрузки: {our_order}")

        npm_like_order = self._simulate_npm_behavior(start_package)
        print(f"Ожидаемый порядок npm: {npm_like_order}")

        differences = []
        for i, pkg in enumerate(our_order):
            if i < len(npm_like_order) and pkg != npm_like_order[i]:
                differences.append(f"Позиция {i + 1}: мы - {pkg}, npm - {npm_like_order[i]}")

        if differences:
            print("Найдены различия:")
            for diff in differences:
                print(f"  - {diff}")
            print("\nПричины различий:")
            print("  - npm может использовать параллельную загрузку")
            print("  - npm оптимизирует порядок для минимизации конфликтов")
            print("  - Разные алгоритмы разрешения зависимостей")
        else:
            print("Порядок загрузки совпадает с ожидаемым поведением npm")

        return our_order, npm_like_order

    def _simulate_npm_behavior(self, start_package):
        """Имитирует поведение npm (упрощенная версия)"""
        visited = set()
        order = []

        def dfs(package):
            if package in visited:
                return
            visited.add(package)

            if package in self.dependencies:
                sorted_deps = sorted(self.dependencies[package].keys())
                for dep in sorted_deps:
                    dfs(dep)

            order.append(package)

        dfs(start_package)
        return order

    def build_graph_from_complete_data(self, complete_graph, start_package):
        """Строит граф из полных данных (для тестового режима)"""
        self.dependencies = complete_graph
        self.visited = set(complete_graph.keys())  # Помечаем все пакеты как посещенные
        self.cycle_detected = False

        # Проверяем наличие циклов
        self._check_for_cycles()

        print(f"Построен граф из {len(complete_graph)} пакетов")

    def _check_for_cycles(self):
        """Проверяет граф на наличие циклов"""
        visited = set()
        recursion_stack = set()

        def has_cycle(package):
            if package not in visited:
                visited.add(package)
                recursion_stack.add(package)

                if package in self.dependencies:
                    for dep in self.dependencies[package]:
                        if dep not in visited and has_cycle(dep):
                            return True
                        elif dep in recursion_stack:
                            print(f"Обнаружен цикл: {package} -> {dep}")
                            self.cycle_detected = True
                            return True

            recursion_stack.remove(package)
            return False

        for package in self.dependencies:
            if package not in visited:
                if has_cycle(package):
                    self.cycle_detected = True