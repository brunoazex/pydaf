from .core.singleton import Singleton
from .core.environment import Environment
from .processor import Processor
import os, sys

@Singleton
class App(object):    
    def _discover_processors(self):
        processors = []
        for py in [f[:-3] for f in os.listdir('%s/%s' % (self.root_path, self.environment.processors.path)) if f.endswith('.py') and f != '__init__.py']:
            mod = __import__('.'.join(['processors', py]), fromlist=[py])
            classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
            for cls in classes:
                if issubclass(cls, Processor) and cls.__name__ in self.environment.processors.queue:
                    processors.append(cls)
        return processors
    
    def run(self, root_path):
        self.root_path = root_path
        try:            
            self.environment = Environment(root_path)
        except(Exception) as error:
            print('App initialisation error: %s' % error)
            raise
        for processor in self._discover_processors():
            processor().run()
            