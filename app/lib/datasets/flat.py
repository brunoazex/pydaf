import pandas as pd
import datetime
from ..app import App

class FlatDataSet(object):
    def __init__(self, name, data):
        (fields, rows) = data
        self._fields = fields
        self.rows = rows
        self._data = pd.DataFrame(rows, columns=fields)
        self._name = name
        
    def to_console(self):       
        print(self._data)
        return self

    def to_csv(self):       
        now = datetime \
            .datetime \
            .now() \
            .strftime('%d-%m-%Y_%H-%M-%S')
        self._data \
            .to_csv('%s%s-%s.csv' % (App.instance().environment.output_dir, self._name, now))
        return self
