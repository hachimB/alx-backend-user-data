#!/usr/bin/env python3
"""Module documentation"""
import re
from typing import List
import logging


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """filter_datum that returns the log message obfuscated"""
    for field in fields:
        message = (re.sub(r'{}=.*?{}'.format(field, separator), '{}={}{}'
                          .format(field, redaction, separator), message))
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """init constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format method"""
        the_format = super().format(record)
        return filter_datum(self.fields, RedactingFormatter.REDACTION,
                            the_format, RedactingFormatter.SEPARATOR)


def get_logger() -> logging.Logger:
    """get_logger"""
    user_data = logging.getLogger("user_data")
    user_data.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    user_data.addHandler(stream_handler)
    return user_data
