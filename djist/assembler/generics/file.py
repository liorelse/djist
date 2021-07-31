#!/usr/bin/python3
"""Djist: Generic file functions
"""
__author__ = "llelse"
__version__ = "0.2.0"
__license__ = "GPLv3"


import json
import logging
import os
from io import TextIOWrapper
from os.path import pathsep
from . import core, msg


def path_exists(path: str):
    return os.path.exists(path)


def path_normalize(path: str):
    return os.path.realpath(os.path.normpath(path))


def path_join(*dirs: str):
    return os.path.join("", *dirs)


def path_create(path: str):
    path = path_normalize(path)
    if not path_exists(path):
        drive, path_ = os.path.splitdrive(path)
        path_list = path_.split(os.sep)
        while("" in path_list):
            path_list.remove("")
        current = ""
        for directory in path_list:
            current = path_join(current, directory)
            full_current = f"{drive}{os.sep}{current}"
            if not path_exists(full_current):
                try:
                    os.mkdir(full_current)
                except OSError as error:
                    print(error)  # Future : Log error


def write_file(data, filename: str, path: str = "output", outformat: str = ""):
    full_path = path_join(path, filename)
    full_path = path_normalize(full_path)
    if not os.path.isfile(full_path):
        path_create(full_path.rsplit(os.sep, 1)[0])
    try:
        with open(full_path, "w") as file:
            if outformat == "json":
                json.dump(data, file, indent=4)
            else:
                if isinstance(data, list):
                    file.writelines(data)
                elif isinstance(data, str):
                    file.write(data)
    except OSError as error:
        print(error)  # Future : Log error


def file_to_list(filename):
    return file_to_str(filename).splitlines()


def file_to_str(filename):
    if os.path.isfile(filename):
        with open(filename, "r") as file:
            template_str = file.read()
        file.close()
    else:
        template_str = ""
    return template_str


def json_to_dict(filename):
    if os.path.isfile(filename):
        with open(filename) as json_file:
            try:
                json_dict = json.load(json_file)
            except ValueError as err:
                logging.error(msg.JSON_DECODE_ERROR, f"{filename} - {err}")
                json_dict = {}
        json_file.close()
    else:
        json_dict = {}
    return json_dict


def write_io(file: TextIOWrapper, kind: str, data: str and list and dict):
    try:
        if kind == "template":
            if isinstance(data, list):
                file.writelines(data)
            elif isinstance(data, str):
                file.write(data)
        elif kind == "dataset":
            json.dump(data, file, indent=4)
        elif kind == "scan":
            if isinstance(data, list):
                for line in data:
                    file.write(f"{line}\n")
    except ValueError as err:
        logging.error(msg.JSON_DECODE_ERROR, err)
        core.close()
    except OSError as err:
        logging.error(msg.GENERAL_ERROR, err)
        core.close()
    file.close()


def read_io(file: TextIOWrapper, kind: str):
    read_in = None
    try:
        if kind == "template":
            read_in = file.read()
        elif kind == "dataset":
            read_in = json.load(file)
    except ValueError as err:
        logging.error(msg.JSON_DECODE_ERROR, err)
        core.close()
    except OSError as err:
        logging.error(msg.GENERAL_ERROR, err)
        core.close()
    file.close()
    return read_in


def read_template(file: TextIOWrapper) -> str:
    template_str: str
    try:
        template_str = file.read()
    except OSError as err:
        logging.error(msg.GENERAL_ERROR, err)
        core.close()
    file.close()
    return template_str


def read_json_dataset(file: TextIOWrapper) -> dict:
    json_dict: dict
    try:
        json_dict = json.load(file)
    except ValueError as err:
        logging.error(msg.JSON_DECODE_ERROR, err)
        core.close()
    file.close()
    return json_dict


def open_file(file: str, mode: str) -> TextIOWrapper:
    if os.path.isfile(file) and mode in ("r", "a"):
        return open(file, mode)
    elif mode in ("w", "x"):
        return open(file, mode)


def data_filename(key):
    return str("data." + key + ".txt").lower()


def template_filename(key):
    return str("template." + key + ".txt").lower()
