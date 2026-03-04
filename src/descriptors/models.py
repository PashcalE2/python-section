from typing import Any, TypeAlias

JSON: TypeAlias = dict[str, Any]


class Model:
    def __init__(self, payload: JSON):
        self.payload = payload


class Field:
    def __init__(self, path: str) -> None:
        self.path = path

    def __get__(self, instance, owner=None):
        paths = self.path.split(".")
        result = instance.payload
        for key in paths:
            if key not in result:
                return None
            result = result[key]
        return result

    def __set__(self, instance, value):
        paths = self.path.split(".")
        target = instance.payload
        for key in paths[:-1]:
            if key not in target:
                return
                # для последнего теста
                # target[key] = {}
            target = target[key]
        target[paths[-1]] = value
