import abc
from importlib import import_module
from types import ModuleType
from typing import List, Type

from django.db import models
from django.db.models.base import ModelBase


class SerializersGeneratorABC(abc.ABC):
    @abc.abstractmethod
    def generate_serializer(self, models_module_name: str): ...


class SerializersGenerator(SerializersGeneratorABC):
    def generate_serializer(self, models_module_name: str):
        module = import_module(models_module_name)
        db_models = self._get_models_from_module(module)

        yield "from rest_framework import serializers"
        yield ""
        yield f"from {models_module_name} import ("

        for model in db_models:
            yield f"    {model.__name__},"

        yield ")"

        for model in db_models:
            class_name = self.get_serializer_class_name_by_model(model)
            yield ""
            yield ""
            yield f"class {class_name}(serializers.ModelSerializer):"
            yield "    class Meta:"
            yield f"        model = {model.__name__}"
            yield f"        fields = ("

            for field in model._meta.fields:
                yield f"            '{field.name}',"

            yield f"        )"

        yield ""

    @classmethod
    def _get_models_from_module(cls, module: ModuleType) -> List[Type[models.Model]]:
        return list(
            filter(lambda item: type(item) is ModelBase, module.__dict__.values()),
        )

    @classmethod
    def get_serializer_class_name_by_model(cls, model: Type[models.Model]) -> str:
        return f"{model.__name__}Serializer"
