#!/bin/usr/env python3

# import re


# def filter_datum(fields: list, redaction: str, message: str,
#                  separator: str) -> str:
#     """filter_datum that returns the log message obfuscated"""
#     for field in fields:
#         message = (re.sub(r'{}=.*?{}'.format(field, separator), '{}={}{}'
#                           .format(field, redaction, separator), message))
#     return message

# def filter_datum(fields, redaction, message, separator):
#     """Returns the log message obfuscated"""
#     return re.sub(rf"({'|'.join(fields)})=.*?{re.escape(separator)}",
#                   rf"\1={redaction}{separator}",
#                   message)
