class Config:
    def __init__(self):
        self.package_name = "WebApp"
        self.repository_url = "test_complex.json"
        self.test_mode = True
        self.ascii_tree_output = False

    def load_from_csv(self, csv_path):
        """Загружает конфигурацию из CSV файла"""
        import os
        if os.path.exists(csv_path):
            try:
                with open(csv_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) >= 2:
                        # Парсим заголовок и данные
                        headers = [h.strip() for h in lines[0].split(',')]
                        values = [v.strip() for v in lines[1].split(',')]

                        for header, value in zip(headers, values):
                            if hasattr(self, header):
                                if header == 'test_mode' or header == 'ascii_tree_output':
                                    setattr(self, header, value.lower() == 'true')
                                else:
                                    setattr(self, header, value)
            except Exception as e:
                print(f"Ошибка загрузки конфигурации: {e}")

    def display_config(self):
        """Выводит текущую конфигурацию"""
        print("Текущая конфигурация:")
        print(f"  package_name: {self.package_name}")
        print(f"  repository_url: {self.repository_url}")
        print(f"  test_mode: {self.test_mode}")
        print(f"  ascii_tree_output: {self.ascii_tree_output}")


def load_config():
    """Загружает конфигурацию (для обратной совместимости)"""
    config = Config()
    config.load_from_csv('config.csv')
    return config


def save_config(config):
    """Сохраняет конфигурацию (для обратной совместимости)"""
    pass