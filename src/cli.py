import sys
import os
from config import Config
from errors import *
from npm_client import NPMClient  


def main():
    """Основная функция CLI приложения"""
    try:
        # Создаем и загружаем конфигурацию
        config = Config()

        # Ищем config.csv в правильном месте
        current_dir = os.path.dirname(__file__)
        config_path = os.path.join(current_dir, '..', 'config.csv')

        config.load_from_csv(config_path)

        # Выводим конфигурацию (требование этапа 1)
        config.display_config()

        # ЭТАП 2: Получаем зависимости
        print("\n=== Этап 2: Получение зависимостей ===")

        npm_client = NPMClient()
        dependencies = npm_client.get_dependencies(config.package_name)

        # Выводим прямые зависимости (требование этапа 2)
        if dependencies:
            print(f"Прямые зависимости пакета '{config.package_name}':")
            for dep_name, dep_version in dependencies.items():
                print(f"  - {dep_name}: {dep_version}")
        else:
            print(f"Пакет '{config.package_name}' не имеет зависимостей")

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