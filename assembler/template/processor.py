#!/usr/bin/python3
"""Djist: Processor for prepped template
"""
__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


import logging
from ..generics import core, file, msg
from . import context as mcontext
from . import tag as mtag
from . import token as mtoken
from . import token_filter as tf


class Processor:
    def __init__(self, context_level: int):
        self.context_level = context_level
        self.processed_template = []
        self.dataset = {}
        self.dataset_keyset = {}
        self.tagselect = {
            "comment": self.tag_comment,
            "copy": self.tag_copy,
            "filter": self.tag_filter,
            "firstof": self.tag_firstof,
            "for": self.tag_for,
            "if": self.tag_if,
            "ignore": self.tag_ignore,
            "length": self.tag_length,
            "replace": self.tag_replace,
            "usedataset": self.tag_usedataset,
            "usetemplate": self.tag_usetemplate,
        }

    def generate_dot_keys(self, obj: dict or list, current_key: str = ""):
        valid_set = set()
        if isinstance(obj, list):
            object_items = enumerate(obj)
        else:
            object_items = obj.items()
        for key, value in object_items:
            key = str(key)
            # Array
            if isinstance(value, list):
                if core.not_empty(current_key) and not current_key.endswith("."):
                    current_key += "."
                valid_set.add(current_key + key)
                item_index = 0
                for item in value:
                    index_added_key = f"{current_key + key}.{item_index}"
                    valid_set.add(index_added_key)
                    if isinstance(item, (dict, list)):
                        valid_set.update(
                            self.generate_dot_keys(item, current_key + key)
                        )
                        valid_set.update(self.generate_dot_keys(item, index_added_key))
                    item_index += 1
            # Dictionary
            elif isinstance(value, dict):
                if core.not_empty(current_key) and not current_key.endswith("."):
                    current_key += "."
                valid_set.add(current_key + key)
                valid_set.update(self.generate_dot_keys(value, current_key + key))
            # Value
            else:
                if core.not_empty(current_key) and not current_key.endswith("."):
                    current_key += "."
                valid_set.add(current_key + key)
        return valid_set

    def key_in_dataset(self, key: str, dataset: dict = None):
        if core.not_empty(key):
            if dataset is None:
                return key in self.dataset_keyset
            else:
                return key in self.generate_dot_keys(dataset)

    def get_data(self, return_type: str = "copy", key: str = "", dataset: dict = None):
        return_value = key
        return_type = return_type.lower()
        if return_type == "copy":
            return self.dataset.copy()
        if self.key_in_dataset(key) and return_type in (
            "type",
            "any",
            "dict",
            "list",
            "str",
            "bool",
            "number",
            "int",
            "float",
        ):
            if dataset is None:
                return_value = self.dataset.copy()
            else:
                return_value = dataset.copy()
            key = key.split(".")
            for step in key:
                if isinstance(return_value, dict):
                    return_value = return_value.get(step)
                elif isinstance(return_value, list):
                    try:
                        step = int(step)
                        return_value = return_value[step]
                    except (ValueError, IndexError):
                        logging.error(msg.INVALID_LIST_INDEX, step)
                        return_value = None
                        break
                else:
                    logging.error(msg.UNEXPECTED_TYPE, core.types(return_value))
                    return_value = None
                    break
            actual_type = type(return_value)
            if return_type == "type":
                return actual_type
            elif return_type == "any":
                return return_value
            elif return_type in (
                "dict",
                "list",
                "str",
                "bool",
                "number",
                "int",
                "float",
            ):
                if core.type_match(actual_type, return_type):
                    return return_value
                logging.error(msg.UNEXPECTED_TYPE, actual_type)
                logging.error(msg.KEY_VALUE, key, return_value)
                return None
            logging.warning(msg.PROC_GETDATA_INVALID_RETURN, return_type)
            return None
        elif not self.key_in_dataset(key):
            try:
                if "." in key:
                    return_value = float(return_value)
                else:
                    return_value = int(return_value)
                actual_type = type(return_value)
            except ValueError:
                logging.error(msg.PROC_GETDATA_ERROR_NONKEY, key)
                return None
            if core.type_match(actual_type, return_type):
                return return_value
            elif return_type == "str":
                return str(return_value)
        logging.warning(msg.PROC_GETDATA_INVALID_RETURN, return_type)
        return None

    def update_dataset(self, newdata: dict):
        if core.not_empty(newdata):
            self.dataset.update(newdata)
            self.dataset_keyset = self.generate_dot_keys(self.get_data("copy"))

    def apply_filter(
        self, token_value: str or bool, filter_value: str, filter_argument: list
    ) -> str or bool:
        filtered_value = token_value
        tfilter = filter_value
        argument = filter_argument
        if tfilter in tf.filter_select.keys():
            selected_filter = tf.filter_select[tfilter]
            filtered_value = selected_filter(filtered_value, argument)
        return filtered_value

    def resolve_filter(self, token, resolved_token) -> str or bool:
        filtered_token = resolved_token
        if token.is_filtered():  # and resolved_token is not None:
            while token.has_next_filter():
                token.load_next_filter()
                filter_value = token.get_filter_value()
                filter_argument_list = []
                filter_argument = ""
                while token.has_next_filter_argument():
                    token.load_next_filter_argument()
                    # filter_argument = token.get_filter_argument()
                    if token.is_filter_argument_literal():
                        filter_argument = token.get_filter_argument()
                    elif token.is_filter_argument_name():
                        filter_argument = self.get_data(
                            "any", token.get_filter_argument()
                        )
                    filter_argument_list.append(filter_argument)
                filtered_token = self.apply_filter(
                    filtered_token, filter_value, filter_argument_list
                )
        return filtered_token

    def resolve_token(self, token):
        resolved_token = ""
        token_value = token.get_value()
        key_in_dataset = self.key_in_dataset(token_value)
        if token.is_literal() or token.is_verbatim():
            resolved_token = token_value
        elif token.is_name():
            if token.is_expression() and token.is_operator():
                resolved_token = token_value
            elif token.is_expression() and token_value.count(".") > 0:
                try:
                    resolved_token = str(float(token_value))
                except (ValueError, TypeError):
                    resolved_token = self.get_data("any", token_value)
            else:
                resolved_token = self.get_data("any", token_value)
        resolved_token = self.resolve_filter(token, resolved_token)
        if isinstance(resolved_token, bool):
            resolved_token = str(resolved_token)
        if (
            token.is_expression()
            and not token.is_filter_boolean()
            and (token.is_literal() or (token.is_name() and key_in_dataset))
        ):
            resolved_token = '"' + resolved_token + '"'
        if resolved_token is None:
            resolved_token = ""
        return resolved_token

    def evaluate(self, expression: tuple or str, eval_dataset: dict):
        unpacked_expression, evaluated = (None,) * 2
        if isinstance(expression, tuple):
            if isinstance(expression[0], mtoken.Token):
                expression = tuple(self.resolve_token(token) for token in expression)
            unpacked_expression = " ".join(expression)
        elif isinstance(expression, str):
            unpacked_expression = expression
        else:
            unpacked_expression = str(expression)
        if core.not_empty(unpacked_expression):
            # Future: Alternative to eval()
            try:
                evaluated = eval(unpacked_expression, eval_dataset)
            except NameError as err:
                logging.error(msg.EVAL_ATTEMPT, unpacked_expression)
                logging.error(msg.EVAL_ERROR, err)
            if isinstance(evaluated, str):
                evaluated = core.not_empty(evaluated)
        return evaluated

    def new_context(self, template_segment: str, add_dataset: dict, source: str = ""):
        newcontext = mcontext.Context(self.context_level, source)
        newcontext.set_dataset(self.get_data("copy"))
        newcontext.set_dataset(add_dataset)
        newcontext.set_template(template_segment)
        context_result = newcontext.process()
        del newcontext
        return context_result

    def process_action(self, action: mtag.Action) -> str:
        if action.get_action() in self.tagselect.keys():
            selected_tag = self.tagselect[action.get_action()]
        else:
            selected_tag = self.tag_ignore
        processed_action = selected_tag(action)
        try:
            processed_action = str(processed_action)
            logging.debug(msg.PROC_ACTION_SUCCESS, action.get_action())
        except (ValueError, TypeError) as err:
            logging.error(msg.GENERAL_ERROR, err)
            core.close()
        return processed_action

    def tag_comment(self, action: mtag.Action):
        return ""

    def tag_copy(self, action: mtag.Action):
        return action.get_content()

    def tag_filter(self, action: mtag.Action):
        filtered_content = self.new_context(action.get_content(), {}, source="filter")
        for token in action.get_argument():
            if token.is_name():
                filter_value = token.get_value()
                filter_argument = token.get_argument()
                if token.is_argument_name():
                    filter_argument = self.get_data("any", filter_argument)
                filtered_content = self.apply_filter(
                    filtered_content, filter_value, filter_argument
                )
                filtered_content = self.resolve_filter(token, filtered_content)
        return filtered_content

    def tag_firstof(self, action: mtag.Action):
        first_result = ""
        for argument in action.get_argument():
            first_result = self.resolve_token(argument)
            if first_result not in ("", None):
                return first_result
        return first_result

    def tag_for(self, action: mtag.Action):
        for_result = ""
        loop_key, assigner, dataset_name = (None,) * 3
        arguments, content = action.get()
        if len(arguments) == 3:
            loop_key = arguments[0].get_value()
            assigner = arguments[1].get_value()
            dataset_name = arguments[2].get_value()
        if assigner == "in" and dataset_name:
            for_dataset = self.resolve_token(arguments[2])
            if isinstance(for_dataset, list):
                try:
                    for item in for_dataset:
                        # if isinstance(item, (dict, list)):
                        for_result += self.new_context(
                            content, {loop_key: item}, source="for"
                        )
                except TypeError:
                    logging.error(msg.UNEXPECTED_TYPE, core.types(for_dataset))
        return for_result

    def tag_if(self, action: mtag.Action):
        def if_eval():
            ev = self.evaluate(argument, self.get_data("copy"))
            if not isinstance(ev, bool):
                ev = False
            return ev

        if_result = ""
        argument, content = action.get()
        evaluated = if_eval()
        if evaluated:
            if_result += self.new_context(content, {})
        elif not evaluated and action.has_next():
            while action.has_next():
                action.next()
                multiblock_action, argument, content = action.get_all()
                if multiblock_action == "elif":
                    evaluated = if_eval()
                    if evaluated:
                        if_result += self.new_context(content, {})
                        break
                elif multiblock_action == "else":
                    if_result += self.new_context(content, {})
                    break
        return if_result

    def tag_ignore(self, action: mtag.Action):
        return ""

    def tag_length(self, action: mtag.Action):
        length = ""
        arguments = action.get_argument()
        first_token = arguments[0]
        length = str(len(self.resolve_token(first_token)))
        if length == "0":
            data_type = self.get_data("type", first_token.get_value())
            if data_type in ("dict", "list"):
                length = str(len(self.get_data(data_type, first_token.get_value())))
        return length

    def tag_replace(self, action: mtag.Action):
        replace_value = self.resolve_token(action.get_argument()[0])
        return replace_value

    def tag_usedataset(self, action: mtag.Action):
        filename = ""
        dataset_content = {}
        source_token = action.get_argument()[0]
        if source_token.is_literal():
            filename = source_token.get_value()
        elif source_token.is_name():
            filename = self.get_data("str", source_token.get_value())
        if core.not_empty(filename):
            # Future: path lookup by keyword
            # filename = core.locate_path('dataset', filename)
            dataset_content = file.json_to_dict(filename)
            self.update_dataset(dataset_content)
        return ""

    def tag_usetemplate(self, action: mtag.Action):
        template = ""
        filename = self.resolve_token(action.get_argument()[0])
        source_token = action.get_argument()[0]
        if source_token.is_literal():
            filename = source_token.get_value()
        elif source_token.is_name():
            filename = self.get_data("str", source_token.get_value())
        if filename:
            # Future: path lookup by keyword
            # filename = core.locate_path('dataset', filename)
            template_segment = file.file_to_str(filename)
            return self.new_context(template_segment, {}, source="usetemplate")
        return template

    def run(self, prepped_template: list, dataset: dict) -> str:
        logging.debug("start processing prepped template (segment)")
        self.update_dataset(dataset)
        for action in prepped_template:
            self.processed_template.append(self.process_action(action))
        self.processed_template = "".join(self.processed_template)
        logging.debug("completed processing prepped template (segment)")
        return self.processed_template
