import abc
from importlib import import_module
from types import ModuleType
from typing import Type, List

from rest_framework.serializers import SerializerMetaclass, ModelSerializer


class ViewsGeneratorABC(abc.ABC):
    @abc.abstractmethod
    def generate_views(self, serializers_module_name: str, view_module_name: str): ...


class ViewsGenerator(ViewsGeneratorABC):
    def generate_views(self, serializers_module_name: str, models_module_name: str):
        module = import_module(serializers_module_name)
        serializers = self._get_serializers_from_module(module)

        yield "from rest_framework.viewsets import GenericViewSet"
        yield "from rest_framework.mixins import ("
        yield "    CreateModelMixin,"
        yield "    RetrieveModelMixin,"
        yield "    UpdateModelMixin,"
        yield "    DestroyModelMixin,"
        yield "    ListModelMixin,"
        yield ")"
        yield ""
        yield f"from {serializers_module_name} import ("

        for serializer in serializers:
            yield f"    {serializer.__name__},"

        yield ")"

        yield f"from {models_module_name} import ("

        for serializer in serializers:
            yield f"    {serializer.Meta.model.__name__},"

        yield ")"

        for serializer in serializers:
            yield ""
            yield ""
            view_class = self.get_view_class_name_by_serializer(serializer)
            yield f"class {view_class}(GenericViewSet,"
            left_space_length = len(f"class {view_class}")
            yield left_space_length * " " + " CreateModelMixin,"
            yield left_space_length * " " + " RetrieveModelMixin,"
            yield left_space_length * " " + " UpdateModelMixin,"
            yield left_space_length * " " + " DestroyModelMixin,"
            yield left_space_length * " " + " ListModelMixin):"
            yield f"    queryset = {serializer.Meta.model.__name__}.objects.all()"
            yield f"    serializer_class = {serializer.__name__}"

        yield ""

    @classmethod
    def _get_serializers_from_module(cls, module: ModuleType) -> List[Type[ModelSerializer]]:
        return list(
            filter(lambda item: type(item) is SerializerMetaclass, module.__dict__.values()),
        )

    @classmethod
    def get_view_class_name_by_serializer(cls,
                                          serializer: Type[ModelSerializer]):
        return f"{serializer.Meta.model.__name__}ModelViewSet"
