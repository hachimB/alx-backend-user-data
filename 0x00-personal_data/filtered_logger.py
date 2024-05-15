#!/usr/bin/env python3
"""Regex-ing"""
import re


# def filter_datum(
#         fields: list,
#         redaction: str,
#         message: str,
#         separator: str) -> str:
#     """filter_datum that returns the log message obfuscated"""
#     for field in fields:
#         message = (re.sub(r'{}=.*?{}'.format(field, separator),
#                    '{}={}{}'.format(field, redaction, separator), message))
#     return message
def filter_datum(fields: list, redaction: str, message: str, separator: str) -> str:
    """Return the log message with specified fields obfuscated."""; return re.sub('|'.join(f'{field}=.*?{separator}' for field in fields), lambda m: f'{m.group().split("=")[0]}={redaction}{separator}', message)
