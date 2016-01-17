""" colored logging """

import logging
from logging import Formatter
from logging import getLogger
from logging import StreamHandler
from datetime import datetime
import sys


class Color(object):
    """
     usage::
         >>> colored = Color()
         >>> colored("text","red")
        '\x1b[31mtext\x1b[0m'
        '\033[44;37;5m hello world\033[0m'
    """
    colors = {
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'white': 37,
        'bgred': 41,
        'bggrey': 100
    }

    prefix = '\033['

    suffix = '\033[0m'

    def __call__(self, text, color):
        return self.colored(text, color)

    def colored(self, text, color=None):
        if color not in self.colors:
            color = 'white'

        clr = self.colors[color]
        return (self.prefix+'%dm%s'+self.suffix) % (clr, text)


colored = Color()


class ColoredFormatter(Formatter):
    """this is colored formatter"""

    def format(self, record):
        message = record.getMessage()

        mapping = {
            'CRITICAL': 'bgred',
            'ERROR': 'red',
            'WARNING': 'yellow',
            'SUCCESS': 'green',
            'INFO': 'cyan',
            'DEBUG': 'bggrey',
        }

        # default color
        color = mapping.get(record.levelname, "write")

        level = colored('%-8s' % record.levelname, color)
        time = colored(datetime.now().strftime("(%H:%M:%S)"), "magenta")
        return " ".join([level, time, message])

logger = getLogger('doge')

# add level 'success'
logging.SUCCESS = 25  # 25 is between WARNING(30) and INFO(20)
logging.addLevelName(logging.SUCCESS, 'SUCCESS')

# stackoverflow told me to use method `_log`,  but the `log` is better
# because, `log` check its level's enablity

logger.success = lambda msg, *args, **kwargs: logger.log(logging.SUCCESS, msg, *args, **kwargs)

# add colored handler
handler = StreamHandler(sys.stdout)  # thread.lock
formatter = ColoredFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    logger.info('info')
    logger.success('success')
    logger.debug('debug')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
