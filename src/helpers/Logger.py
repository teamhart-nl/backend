class Logger:
    """
    Logger can be used to log data in a standardized fashion
    """

    @staticmethod
    def log_info(text) -> None:
        print(f"=== LOGGER OUTPUT ===== INFO: {text}")

    @staticmethod
    def log_warning(text) -> None:
        print(f"=== LOGGER OUTPUT ===== WARNING: {text} ===")
