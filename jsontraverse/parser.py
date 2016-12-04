from __future__ import unicode_literals
import re
import json

class JsonTraverseParser:
    def __init__(self, raw_data):
        if raw_data and not isinstance(raw_data, "".__class__):
            raise TypeError("the 'raw_data' argument must be {}, not '{}'".format("".__class__, type(raw_data)))

        self.data = json.loads(raw_data) if raw_data else None

    def traverse(self, path):
        if not isinstance(path, "".__class__):
            raise TypeError("the 'path' argument must be {}, not '{}'".format("".__class__, type(path)))

        reduced = []

        if self.data:
            reduced.append(self.data)

        if path:
            for item in path.split("."):
                list_reduced = list(reduced)
                if self.is_valid_index(item):
                    list_reduced = self.reduce_list(reduced, item)

                dict_reduced = self.flatten(reduced)
                if not list_reduced or list_reduced == reduced:
                    dict_reduced = self.reduce_dict(dict_reduced, item)

                if list_reduced and list_reduced != reduced:
                    print("item: {}, LIST, list_reduced: {}, reduced: {}".format(item, list_reduced, reduced))
                    reduced = list_reduced
                elif dict_reduced and dict_reduced != self.flatten(reduced):
                    print("item: {}, DICT, dict_reduced: {}, reduced: {}".format(item, dict_reduced, reduced))
                    reduced = dict_reduced
                else:
                    print("item: {}, MISS".format(item))
                    reduced = []

        print("INTERM RESULT: {}".format(reduced))

        if isinstance(reduced, list) and len(reduced) == 1:
            reduced = reduced[0]

        if isinstance(reduced, list) and len(reduced) == 0:
            reduced = None

        print("FINAL RESULT: {}".format(reduced))
        return reduced

    def reduce_list(self, reduced, item):
        outputs = []

        for value in reduced:
            try:
                outputs.append(value[int(item)])
            except (ValueError, IndexError, KeyError, TypeError):
                pass

        return outputs

    def reduce_dict(self, reduced, item):
        outputs = []

        for value in reduced:
            try:
                outputs.append(value[item])
            except (KeyError, TypeError):
                pass

        return outputs

    def flatten(self, reduced):
        flattened = []
        for value_or_sublist in reduced:
            if isinstance(value_or_sublist, list):
                flattened += value_or_sublist
            else:
                flattened.append(value_or_sublist)
        return flattened

    def is_valid_index(self, string):
        return re.match(r"^(0|[1-9][0-9]*)$", string)
