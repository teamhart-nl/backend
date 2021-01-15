class Logger:

    @staticmethod
    def log_info(text) -> None:
        print(f"=== LOGGER OUTPUT ===== INFO: {text}")

    @staticmethod
    def log_warning(text) -> None:
        print(f"=== LOGGER OUTPUT ===== WARNING: {text} ===")
