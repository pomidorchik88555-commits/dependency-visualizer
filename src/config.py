import os
import csv
from urllib.parse import urlparse
from errors import *


class Config:
    def __init__(self):
        self.package_name = None
        self.repository_url = None
        self.test_mode = False
        self.ascii_tree_output = False

    def load_from_csv(self, csv_path="config.csv"):
        """Загружает конфигурацию из CSV файла"""
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Конфигурационный файл {csv_path} не найден")

        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

                if not rows:
                    raise CSVFormatError("CSV файл пуст")

                # Берем первую строку для конфигурации
                config_row = rows[0]

                self._validate_and_set_config(config_row)

        except csv.Error as e:
            raise CSVFormatError(f"Ошибка чтения CSV файла: {e}")

    def _validate_and_set_config(self, config_row):
        """Валидирует и устанавливает параметры конфигурации"""

        # Валидация имени пакета
        package_name = config_row.get('package_name', '').strip()
        if not package_name:
            raise InvalidPackageNameError("Имя пакета не может быть пустым")
        self.package_name = package_name

        # Валидация URL/пути репозитория
        repository_url = config_row.get('repository_url', '').strip()
        if not repository_url:
            raise InvalidURLError("URL репозитория не может быть пустым")

        # Проверяем, является ли это URL или локальным путем
        if repository_url.startswith(('http://', 'https://')):
            parsed = urlparse(repository_url)
            if not parsed.scheme or not parsed.netloc:
                raise InvalidURLError(f"Некорректный URL: {repository_url}")
        elif not os.path.exists(repository_url):
            raise InvalidURLError(f"Локальный путь не существует: {repository_url}")

        self.repository_url = repository_url

        # Валидация режима тестового репозитория
        test_mode = config_row.get('test_mode', 'false').strip().lower()
        if test_mode not in ('true', 'false', '1', '0', 'yes', 'no'):
            raise InvalidModeError("Режим test_mode должен быть true/false, 1/0, yes/no")
        self.test_mode = test_mode in ('true', '1', 'yes')

        # Валидация режима вывода ASCII-дерева
        ascii_tree = config_row.get('ascii_tree_output', 'false').strip().lower()
        if ascii_tree not in ('true', 'false', '1', '0', 'yes', 'no'):
            raise InvalidModeError("Режим ascii_tree_output должен быть true/false, 1/0, yes/no")
        self.ascii_tree_output = ascii_tree in ('true', '1', 'yes')

    def display_config(self):
        """Выводит конфигурацию в формате ключ-значение"""
        print("Текущая конфигурация:")
        print(f"  package_name: {self.package_name}")
        print(f"  repository_url: {self.repository_url}")
        print(f"  test_mode: {self.test_mode}")
        print(f"  ascii_tree_output: {self.ascii_tree_output}")