import abc
import re
from importlib import import_module
from types import ModuleType
from typing import List, Type

from rest_framework.viewsets import GenericViewSet


class UrlsGeneratorABC(abc.ABC):
    @abc.abstractmethod
    def generate_urls(self, views_module_name: str): ...


class UrlsGenerator(UrlsGeneratorABC):
    def generate_urls(self, views_module_name: str):
        module = import_module(views_module_name)
        views = self._get_views_from_module(module)
        yield 'from django.urls import path, include'
        yield 'from rest_framework import routers'
        yield ''
        yield f'from {views_module_name} import ('

        for view in views:
            yield f'    {view.__name__},'

        yield ')'

        yield ''
        yield 'router = routers.DefaultRouter()'

        for view in views:
            url = self.get_url_by_view_class(view)
            yield f'router.register("{url}", {view.__name__})'

        yield ""
        yield "urlpatterns = router.urls"
        yield ""

    @classmethod
    def _get_views_from_module(cls, module: ModuleType) -> List[Type[GenericViewSet]]:
        return list(
            filter(lambda item: type(item) is type and item.__name__.endswith('ModelViewSet'), module.__dict__.values()),
        )

    @classmethod
    def get_url_by_view_class(cls, view: Type[GenericViewSet]) -> str:
        class_name = view.__name__
        class_name = class_name.replace("ModelViewSet", "")
        return re.sub(r'(?<!^)(?=[A-Z])', '-', class_name).lower()
