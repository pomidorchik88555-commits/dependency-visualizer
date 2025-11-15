import sys
import os
from config import Config
from errors import *
from npm_client import NPMClient
from dependency_graph import DependencyGraph


def main():
    """Основная функция CLI приложения"""
    try:
        config = Config()

        current_dir = os.path.dirname(__file__)
        config_path = os.path.join(current_dir, '..', 'config.csv')

        config.load_from_csv(config_path)

        config.display_config()

        npm_client = NPMClient()
        graph = DependencyGraph()

        if config.test_mode:
            print("\nРЕЖИМ ТЕСТИРОВАНИЯ")
            print(f"Анализируем тестовый пакет: {config.package_name}")
            print(f"Путь к тестовому файлу: {config.repository_url}")

            if os.path.exists(config.repository_url):
                print(f"Файл существует: {config.repository_url}")

                # В ТЕСТОВОМ РЕЖИМЕ: получаем полный граф из файла
                complete_graph = npm_client.get_complete_test_graph(config.repository_url)
                graph.build_graph_from_complete_data(complete_graph, config.package_name)

            else:
                print(f"Файл НЕ существует: {config.repository_url}")
                raise FileNotFoundError(f"Тестовый файл не найден: {config.repository_url}")

        else:
            print("\nРЕЖИМ РАБОТЫ С NPM")
            print(f"Анализируем пакет: {config.package_name}")

            def get_deps_func(pkg):
                return npm_client.get_dependencies_recursive(pkg, test_mode=False)

            print("\nЭТАП 3: ПОСТРОЕНИЕ ГРАФА ЗАВИСИМОСТЕЙ")
            graph.build_graph_bfs(config.package_name, get_deps_func)

        graph.display_graph()

        print("\nЭТАП 4: ПОРЯДОК ЗАГРУЗКИ ЗАВИСИМОСТЕЙ")

        load_order = graph.get_load_order()
        print(f"Порядок загрузки зависимостей:")
        for i, package in enumerate(load_order, 1):
            print(f"  {i}. {package}")

        if not config.test_mode:
            graph.compare_with_npm_behavior(config.package_name)
        else:
            print("\nВ тестовом режиме сравнение с npm не выполняется")
            print("Режим тестирования использует упрощенные данные")

        print(f"\nАнализ завершен!")
        print(f"Проанализировано пакетов: {len(graph.get_graph())}")
        if graph.has_cycles():
            print("Обнаружены циклические зависимости")

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    except ConfigError as e:
        print(f"Ошибка конфигурации: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()