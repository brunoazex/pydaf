from .flat import FlatDataSet
import pandas as pd

class PivotDataSet(FlatDataSet):    
    def __init__(self, name, source, options):
        super().__init__(name, source)
        self._data = self._data \
            .pivot_table(index=options.index,
                         values=options.values,
                         aggfunc=options.aggfunc) \
            .rename(columns=options.labels)
    
    def add_group_subtotals(self):
        subtotals = [
            d.append(d.sum().rename((k, 'Subtotal')))
            for k, d in self._data.groupby(level=0)
        ]        
        grand_total = self._data \
            .sum() \
            .rename(('Grand', 'Total'))
            
        self._data = pd \
            .concat(subtotals) \
            .append(grand_total)
        return self   
   
                       
        
    def sort(self, field, ascending=True):
        self._data = self._data \
            .reindex(
                self._data[field] \
                    .sort_values(ascending=ascending)
                    .index
            )
        return self
    
    class Options():
        def __init__(self):
            self.index = []
            self.values = []
            self.aggfunc = {}
            self.labels = {}
    
        def has_aggregate(self, definitions):
            for value in definitions:
                (field, operation) = value            
                self.aggfunc.update({field: operation})
            return self
            
        def has_index(self, *fields):
            for field in fields:
                self.index.append(field)
            return self
        
        def has_values(self, *fields):
            for field in fields:
                self.values.append(field)
            return self
            
        def rename(self, definitions):
            for value in definitions:
                (field, label) = value            
                self.labels.update({field: label})
            return self