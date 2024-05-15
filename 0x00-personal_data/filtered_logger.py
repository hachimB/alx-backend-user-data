#!/usr/bin/env python3
"""Regex-ing
"""
import re


# def filter_datum(fields: list,
#                  redaction: str,
#                  message: str,
#                  separator: str) -> str:
#     """filter_datum that returns the log message obfuscated"""
#     for field in fields:
#         if field in message:
#             message = re.sub(r'{}=.*?{}'.format(field, separator),
#                              '{}={}{}'.format(field, redaction, separator),
#                              message)
#     return message

def filter_datum(
        fields: list,
        redaction: str,
        message: str,
        separator: str) -> str:
    """filter_datum that returns the log message obfuscated"""
    return re.sub(
        '|'.join(
            f'{field}=.*?{separator}' for field in fields),
        lambda match: f'{match.group().split("=")[0]}={redaction}{separator}',
        message)
