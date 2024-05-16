#!/usr/bin/env python3
"""Module documentation"""
import re
from typing import List
import logging
from mysql.connector import (connection)
import os

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
    user_data = logging.getLogger(__name__)
    user_data.setLevel(logging.INFO)
    user_data.propagate = False
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    user_data.addHandler(stream_handler)
    return user_data


def get_db() -> connection.MySQLConnection:
    """get_db function"""
    db_host = os.getenv('PERSONAL_DATA_DB_HOST')
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    connect = connection.MySQLConnection(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return connect


def main() -> None:
    """main function"""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    logger = get_logger()
    for row in cursor.fetchall():
        message = "; ".join([f"{key}={value}" for key, value in row.items()])
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
