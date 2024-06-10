# source: https://stackoverflow.com/questions/11232230/logging-to-two-files-with-different-settings
import logging

class FileLog:

    loggers: dict[str, logging.Logger] = {}
    __formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    @classmethod
    def init_log(cls, name: str, log_file: str, level=logging.INFO) -> None:
        
        if cls.loggers.get(name) is not None:
            return
        
        handler = logging.FileHandler(log_file, encoding='cp1250')
        handler.setFormatter(cls.__formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        cls.loggers[name] = logger