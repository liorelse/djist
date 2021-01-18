#!/usr/bin/python3
"""Djist: Generic file functions
"""
__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


import json
import logging
import os
from . import (core, msg)


def evaluate(exp, vars):
    pass
    # parser = expression.Expression_Parser(variables=vars)
    # return parser.parse(exp)


def path_exists(path: str):
    if core.not_none_or_empty(path):
        return os.path.exists(path)


def path_join(*dirs: str):
    return os.path.join('', *dirs).replace('\\', '/')


def path_create(path: str):
    if core.not_none_or_empty(path):
        if not path_exists(path):
            path_list = path.split('/')
            if path_list[-1] == '':
                del path_list[-1]
            current = ''
            for directory in path_list:
                current = path_join(current, directory)
                if not path_exists(current):
                    try:
                        os.mkdir(current)
                    except OSError as error:
                        print(error)  # Future : Log error


def write_file(data, filename: str, path: str = 'output', outformat: str = ''):
    if core.not_none_or_empty(data) and core.not_none_or_empty(filename):
        path_create(path)
        full_path = path_join(path, filename)
        try:
            with open(full_path, 'w') as file:
                if outformat == 'json':
                    json.dump(data, file, indent=4)
                else:
                    if isinstance(data, list):
                        file.writelines(data)
                    elif isinstance(data, str):
                        file.write(data)
        except OSError:
            pass


def file_to_list(filename):
    return file_to_str(filename).splitlines()


def file_to_str(filename):
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            template_str = file.read()
        file.close()
    else:
        template_str = ''
    return template_str


def json_to_dict(filename):
    if os.path.isfile(filename):
        with open(filename) as json_file:
            try:
                json_dict = json.load(json_file)
            except ValueError as err:
                logging.error(msg.JSON_DECODE_ERROR, filename, err)
                json_dict = {}
        json_file.close()
    else:
        json_dict = {}
    return json_dict


def data_filename(key):
    return str('data.' + key + '.txt').lower()


def template_filename(key):
    return str('template.' + key + '.txt').lower()
