import logging
from logging.handlers import TimedRotatingFileHandler

# Logger
srv_logger = logging.getLogger("srv_log")

# Setup rotating log
# rotate every 1 day (d = day interval=1)
# backups 2 previous log file (backupCount=2)
# file_handler = TimedRotatingFileHandler("./app/app.log", when="d", interval=1, backupCount=2, encoding="utf-8")
file_handler = TimedRotatingFileHandler("app.log", when="d", interval=1, backupCount=2, encoding="utf-8")

# Formatter  (time level logger_name message)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
file_handler.setFormatter(formatter)

srv_logger.addHandler(file_handler)
srv_logger.setLevel(logging.DEBUG)
