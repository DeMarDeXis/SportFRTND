import logging
import json
from datetime import datetime
from termcolor import colored

class PrettyFormatter(logging.Formatter):
    def format(self, record):
        level = record.levelname.upper() + ":"
        time_str = datetime.fromtimestamp(record.created).strftime("[%H:%M:%S.%f]")
        msg = colored(record.getMessage(), 'cyan')

        level_color = {
            'DEBUG': 'magenta',
            'INFO': 'blue',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }.get(record.levelname, 'white')

        level = colored(level, level_color)

        fields = {
            'name': record.name,
            'level': record.levelname,
            'pathname': record.pathname,
            'lineno': record.lineno,
            'funcName': record.funcName,
            'created': record.created,
            'msecs': record.msecs,
            'relativeCreated': record.relativeCreated,
            'thread': record.thread,
            'threadName': record.threadName,
            'process': record.process,
            'processName': record.processName,
        }

        if record.exc_info:
            fields['exc_info'] = self.formatException(record.exc_info)

        if record.args:
            fields.update(record.args)

        b = json.dumps(fields, indent=2)

        return f"{time_str} {level} {msg} {colored(b, 'white')}"

def setup_logger(env):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    if env == 'local':
        console_handler.setFormatter(PrettyFormatter())
    else:
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    logger.addHandler(console_handler)

    return logger