import logging
import coloredlogs

class CallbackHandler(logging.Handler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def emit(self, record):
        msg = self.format(record)
        self.callback(msg)


logger = logging.getLogger(f'{"main"}:{"loger"}')
fmt = f"🤖 %(asctime)s %(message)s"
coloredlogs.install(
    level=logging.DEBUG, logger=logger, milliseconds=False, datefmt='%m-%d %H:%M:%S', fmt=fmt,
)
formatter = logging.Formatter(fmt = f"🤖%(asctime)s %(message)s" , datefmt='%m-%d %H:%M:%S')

    
def initUvicornLogger():
    LOGGER_NAMES = ("uvicorn", "uvicorn.access",)
    for logger_name in LOGGER_NAMES:
        logging_logger = logging.getLogger(logger_name)
        fmt = f"🌏%(asctime)s %(message)s"  # 📨
        coloredlogs.install(
            level=logging.WARN, logger=logging_logger, milliseconds=False, datefmt='%m-%d %H:%M:%S', fmt=fmt
        )

def addLogCallback(log_callback):
    handler = CallbackHandler(callback=log_callback)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def debug(msg):
    logger.debug(f"DEBUG : {msg}")

def info(msg):
    logger.info(f"INFO  : {msg}")

def warn(msg):
    logger.warning(f"WARN  : {msg}")

def error(msg):
    logger.error(f"ERROR : {msg}")
