
import logging
class LoggingHandler():
    def __init__(self,log_collname='python_25',log_name="log.txt"):
        self.log_collname=log_collname
        self.log_name=log_name

    def my_logger(self,msg,handler_level):
        logger=logging.getLogger(self.log_collname)
        logger.setLevel("DEBUG")

        handler=logging.FileHandler(self.log_name)
        handler.setLevel(handler_level)
        logger.addHandler(handler)

        log_format=logging.Formatter("%(filename)s-%(name)s-%(levelname)s-%(message)s-%(asctime)s")
        handler.setFormatter(log_format)

        if handler_level=="DEBUG":
            logger.debug(msg)
        elif handler_level=="INFO":
            logger.info(msg)
        elif handler_level=="WARNING":
            logger.warning(msg)
        elif handler_level=="ERROR":
            logger.error(msg)
        elif handler_level=="CRITICAL":
            logger.critical(msg)

        logger.removeHandler(handler)
    def play_logger(self,msg,level_handler):
        self.my_logger(msg,level_handler)
if __name__ == '__main__':
    logger_1=LoggingHandler('python25')
    logger_1.play_logger("66666","ERROR")
    logger_1.play_logger("hahahah","INFO")
