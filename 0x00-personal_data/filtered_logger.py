#!/usr/bin/env python3
"""Regex-ing"""
import re


def filter_datum(fields: list, redaction: str, message: str, separator: str) -> str:
    """filter_datum that returns the log message obfuscated"""
    for field in fields:
        message = (re.sub(r'{}=.*?{}'.format(field, separator), '{}={}{}'.format(field, redaction, separator), message))
    return message
