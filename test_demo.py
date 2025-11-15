#!/usr/bin/env python3
"""
Демонстрационный скрипт для тестирования функциональности
"""

import os
import tempfile
import csv
from src.config import Config
from src.errors import *


def create_test_config(package_name, repo_url, test_mode, ascii_tree):
    """Создает временный конфигурационный файл"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(['package_name', 'repository_url', 'test_mode', 'ascii_tree_output'])
        writer.writerow([package_name, repo_url, test_mode, ascii_tree])
        return f.name


def test_valid_config():
    """Тест валидной конфигурации"""
    print("=== Тест валидной конфигурации ===")

    config_file = create_test_config(
        'numpy',
        'https://github.com/numpy/numpy',
        'false',
        'true'
    )

    try:
        config = Config()
        config.load_from_csv(config_file)
        config.display_config()
        print("✅ Тест пройден успешно")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        os.unlink(config_file)


def test_invalid_package():
    """Тест с неверным именем пакета"""
    print("\n=== Тест с пустым именем пакета ===")

    config_file = create_test_config('', 'https://example.com', 'false', 'true')

    try:
        config = Config()
        config.load_from_csv(config_file)
        print("❌ Тест не прошел: ожидалась ошибка")
    except InvalidPackageNameError as e:
        print(f"✅ Ожидаемая ошибка: {e}")
    finally:
        os.unlink(config_file)


def test_invalid_url():
    """Тест с неверным URL"""
    print("\n=== Тест с неверным URL ===")

    config_file = create_test_config('numpy', 'invalid-url', 'false', 'true')

    try:
        config = Config()
        config.load_from_csv(config_file)
        print("❌ Тест не прошел: ожидалась ошибка")
    except InvalidURLError as e:
        print(f"✅ Ожидаемая ошибка: {e}")
    finally:
        os.unlink(config_file)


def test_invalid_mode():
    """Тест с неверным режимом"""
    print("\n=== Тест с неверным режимом ===")

    config_file = create_test_config('numpy', 'https://example.com', 'invalid', 'true')

    try:
        config = Config()
        config.load_from_csv(config_file)
        print("❌ Тест не прошел: ожидалась ошибка")
    except InvalidModeError as e:
        print(f"✅ Ожидаемая ошибка: {e}")
    finally:
        os.unlink(config_file)


if __name__ == "__main__":
    test_valid_config()
    test_invalid_package()
    test_invalid_url()
    test_invalid_mode()