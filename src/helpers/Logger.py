import coloredlogs, logging
coloredlogs.install()


class Logger:
    """
    Logger can be used to log data in a standardized fashion
    """

    @staticmethod
    def log_info(text) -> None:
        logging.info(text)

    @staticmethod
    def log_warning(text) -> None:
        logging.warning(text)

    @staticmethod
    def log_error(text) -> None:
        logging.error(text)
