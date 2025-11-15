import sys
import os
from config import Config
from errors import *


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

        # Здесь в будущих этапах будет логика анализа зависимостей
        print("\nКонфигурация успешно загружена. Готов к анализу зависимостей.")

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