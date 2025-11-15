import sys
import os
from config import Config
from errors import *
from npm_client import NPMClient
from dependency_graph import DependencyGraph


def main():
    """Основная функция CLI приложения"""
    try:
        # Создаем и загружаем конфигурацию
        config = Config()

        # Ищем config.csv в правильном месте
        current_dir = os.path.dirname(__file__)
        config_path = os.path.join(current_dir, '..', 'config.csv')

        config.load_from_csv(config_path)

        # Выводим конфигурацию
        config.display_config()

        # Создаем клиент и граф
        npm_client = NPMClient()
        graph = DependencyGraph()

        # Выбираем функцию для получения зависимостей
        if config.test_mode:
            print(f"\nРЕЖИМ ТЕСТИРОВАНИЯ")
            print(f"Анализируем тестовый пакет: {config.package_name}")
            print(f"Путь к тестовому файлу: {config.repository_url}")

            # Проверяем что файл существует
            if os.path.exists(config.repository_url):
                print(f"Файл существует: {config.repository_url}")
            else:
                print(f"Файл НЕ существует: {config.repository_url}")
                print(f"Текущая директория: {os.getcwd()}")
                print(f"Содержимое директории: {os.listdir('.')}")
                raise FileNotFoundError(f"Тестовый файл не найден: {config.repository_url}")

            def get_deps_func(pkg):
                return npm_client.get_dependencies_recursive(
                    pkg, test_mode=True, repo_path=config.repository_url
                )
        else:
            print(f"\nРЕЖИМ РАБОТЫ С NPM")
            print(f"Анализируем пакет: {config.package_name}")

            def get_deps_func(pkg):
                return npm_client.get_dependencies_recursive(pkg, test_mode=False)

        # Строим граф зависимостей
        print(f"\nЭТАП 3: ПОСТРОЕНИЕ ГРАФА ЗАВИСИМОСТЕЙ")
        graph.build_graph_bfs(config.package_name, get_deps_func)

        # Выводим результат
        graph.display_graph()

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