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

            # Создаем контекст без проверки SSL (для демонстрации)
            context = ssl._create_unverified_context()

            # Делаем запрос с отключенной SSL проверкой
            with urllib.request.urlopen(url, context=context) as response:
                data = json.loads(response.read().decode())
                return data

        except HTTPError as e:
            if e.code == 404:
                raise InvalidPackageNameError(f"Пакет '{package_name}' не найден в npm реестра")
            else:
                raise InvalidURLError(f"Ошибка HTTP {e.code}: {e.reason}")
        except URLError as e:
            raise InvalidURLError(f"Ошибка подключения: {e.reason}")
        except Exception as e:
            raise ConfigError(f"Ошибка при получении данных: {e}")

    def get_dependencies(self, package_name, version="latest"):
        """Получает прямые зависимости пакета"""
        package_info = self.get_package_info(package_name)

        # Получаем информацию о версии
        if version == "latest":
            version = package_info.get("dist-tags", {}).get("latest", "latest")

        version_info = package_info.get("versions", {}).get(version)
        if not version_info:
            raise ConfigError(f"Версия '{version}' не найдена для пакета '{package_name}'")

        # Извлекаем зависимости
        dependencies = version_info.get("dependencies", {})

        return dependencies