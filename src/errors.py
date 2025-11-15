class ConfigError(Exception):
    """Базовое исключение для ошибок конфигурации"""
    pass

class InvalidPackageNameError(ConfigError):
    """Ошибка неверного имени пакета"""
    pass

class InvalidURLError(ConfigError):
    """Ошибка неверного URL или пути к файлу"""
    pass

class InvalidModeError(ConfigError):
    """Ошибка неверного режима работы"""
    pass

class CSVFormatError(ConfigError):
    """Ошибка формата CSV файла"""
    pass