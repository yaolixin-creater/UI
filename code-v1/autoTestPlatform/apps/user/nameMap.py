import base64
import os
import sys
import logging

logger = logging.getLogger('user')

account = {
    "host": "smtp.163.com",
    "port": "465",
    "username": "hh18837292725@163.com",
    "password": base64.b64decode(b'UVlCRERVTEVPR0JST0FWUA==\n'),
    "sender": "hh18837292725@163.com",
}

mail_list = [
    'hh18837292725@163.com',
]

if __name__ == "__main__":
    pass
