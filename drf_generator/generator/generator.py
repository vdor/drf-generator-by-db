import os

from django.db import DEFAULT_DB_ALIAS
from django.conf import settings

from drf_generator.generator.inspect_db import InspectorABC, Inspector
from drf_generator.generator.serializer_generator import SerializersGeneratorABC, SerializersGenerator
from drf_generator.generator.urls_generator import UrlsGeneratorABC, UrlsGenerator
from drf_generator.generator.views_generator import ViewsGeneratorABC, ViewsGenerator


class Generator:
    _application_directory: str
    _inspector: InspectorABC
    _serializers_generator: SerializersGeneratorABC
    _views_generator: ViewsGeneratorABC
    _urls_generator: UrlsGeneratorABC
    _root_dir: str
    _application_directory: str
    _database_alias: str

    def __init__(self,
                 application_directory: str,
                 inspector: InspectorABC = Inspector(),
                 serializers_generator: SerializersGeneratorABC = SerializersGenerator(),
                 views_generator: ViewsGeneratorABC = ViewsGenerator(),
                 urls_generator: UrlsGeneratorABC = UrlsGenerator(),
                 database_alias: str = DEFAULT_DB_ALIAS,
                 root_dir: str = str(settings.BASE_DIR)):
        self._application_directory = application_directory
        self._inspector = inspector
        self._serializers_generator = serializers_generator
        self._views_generator = views_generator
        self._urls_generator = urls_generator
        self._root_dir = root_dir
        self._database_alias = database_alias

    def generate(self):
        self.generate_models()
        self.generate_serializers()
        self.generate_views()
        self.generate_urls()

    @property
    def work_directory(self) -> str:
        return os.path.join(self._root_dir, self._application_directory)

    @property
    def _models_tmp_filename(self) -> str:
        return os.path.join(self.work_directory, 'models.py')

    @property
    def _models_tmp_module(self) -> str:
        return self.get_module_name_by_filepath(self._models_tmp_filename)
    
    @property
    def _serializers_tmp_filename(self) -> str:
        return os.path.join(self.work_directory, 'serializers.py')

    @property
    def _serializers_tmp_module(self):
        return self.get_module_name_by_filepath(self._serializers_tmp_filename)

    @property
    def _views_tmp_filename(self) -> str:
        return os.path.join(self.work_directory, 'views.py')

    @property
    def _views_tmp_module(self):
        return self.get_module_name_by_filepath(self._views_tmp_filename)

    @property
    def _urls_tmp_filename(self) -> str:
        return os.path.join(self.work_directory, 'urls.py')

    @property
    def _urls_tmp_module(self):
        return self.get_module_name_by_filepath(self._urls_tmp_filename)

    def _remove_models_tmp_file(self):
        self._remove_file(self._models_tmp_filename)
        
    def _remove_serializers_tmp_file(self):
        self._remove_file(self._serializers_tmp_filename)

    def _remove_views_tmp_file(self):
        self._remove_file(self._views_tmp_filename)

    def _remove_urls_tmp_file(self):
        self._remove_file(self._urls_tmp_filename)

    def generate_models(self):
        self._remove_models_tmp_file()

        with open(self._models_tmp_filename, 'w+') as f:
            for line in self._inspector.inspect(
                database=self._database_alias,
            ):
                f.write(line + '\n')

    def generate_serializers(self):
        self._remove_serializers_tmp_file()
        with open(self._serializers_tmp_filename, 'w+') as f:
            for line in self._serializers_generator.generate_serializer(self._models_tmp_module):
                f.write(line + '\n')
        
    def generate_views(self):
        self._remove_views_tmp_file()
        with open(self._views_tmp_filename, 'w+') as f:
            for line in self._views_generator.generate_views(self._serializers_tmp_module, self._models_tmp_module):
                f.write(line + '\n')

    def generate_urls(self):
        self._remove_urls_tmp_file()
        with open(self._urls_tmp_filename, 'w+') as f:
            for line in self._urls_generator.generate_urls(self._views_tmp_module):
                f.write(line + '\n')

    def get_module_name_by_filepath(self, filepath: str) -> str:
        module = filepath \
            .replace('.py', '') \
            .replace(self._root_dir, '') \
            .replace('/', '.')

        if module[0] == '.':
            module = module[1:]

        return module

    @classmethod
    def _remove_file(cls, filename: str):
        if os.path.exists(filename):
            os.remove(filename)
