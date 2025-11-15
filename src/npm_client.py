import json
import urllib.request
import ssl
from urllib.error import URLError, HTTPError
from errors import *


class NPMClient:
    def __init__(self):
        self.base_url = "https://registry.npmjs.org"

    def get_package_info(self, package_name):
        """Получает информацию о пакете из npm реестра"""
        try:
            url = f"{self.base_url}/{package_name}"
            print(f"Запрос к npm: {url}")

            context = ssl._create_unverified_context()

            with urllib.request.urlopen(url, context=context) as response:
                data = json.loads(response.read().decode())
                return data

        except HTTPError as e:
            if e.code == 404:
                raise InvalidPackageNameError(f"Пакет '{package_name}' не найден в npm реестре")
            else:
                raise InvalidURLError(f"Ошибка HTTP {e.code}: {e.reason}")
        except URLError as e:
            raise InvalidURLError(f"Ошибка подключения: {e.reason}")
        except Exception as e:
            raise ConfigError(f"Ошибка при получении данных: {e}")

    def get_dependencies(self, package_name, version="latest"):
        """Получает прямые зависимости пакета"""
        package_info = self.get_package_info(package_name)

        if version == "latest":
            version = package_info.get("dist-tags", {}).get("latest", "latest")

        version_info = package_info.get("versions", {}).get(version)
        if not version_info:
            raise ConfigError(f"Версия '{version}' не найдена для пакета '{package_name}'")

        dependencies = version_info.get("dependencies", {})

        return dependencies

    def get_dependencies_test_mode(self, package_name, repo_path):
        """Получает зависимости в тестовом режиме (из файла)"""
        try:
            import json
            print(f"Читаем тестовый файл: {repo_path}")

            with open(repo_path, 'r') as f:
                test_data = json.load(f)

            # В тестовом режиме возвращаем ВСЕ зависимости из файла
            # чтобы алгоритм мог построить полный граф
            dependencies = test_data.get(package_name, [])
            print(f"Найдены зависимости для {package_name}: {dependencies}")

            return {dep: "1.0.0" for dep in dependencies}

        except FileNotFoundError:
            raise ConfigError(f"Тестовый файл не найден: {repo_path}")
        except json.JSONDecodeError:
            raise ConfigError(f"Ошибка формата JSON в файле: {repo_path}")
        except Exception as e:
            raise ConfigError(f"Ошибка чтения тестового файла: {e}")

    def get_dependencies_recursive(self, package_name, test_mode=False, repo_path=None):
        """Рекурсивно получает зависимости (основной метод для графа)"""
        if test_mode:
            return self.get_dependencies_test_mode(package_name, repo_path)
        else:
            return self.get_dependencies(package_name)

    def get_complete_test_graph(self, repo_path):
        """Возвращает полный граф зависимостей из тестового файла"""
        try:
            import json
            with open(repo_path, 'r') as f:
                test_data = json.load(f)

            # Преобразуем в формат: {пакет: {зависимость: версия}}
            complete_graph = {}
            for package, deps in test_data.items():
                complete_graph[package] = {dep: "1.0.0" for dep in deps}

            return complete_graph

        except Exception as e:
            raise ConfigError(f"Ошибка чтения тестового файла: {e}")