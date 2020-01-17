import csv as py_csv

class Csv():    
    def load(self, filename):
        rows = {}
        with open(filename) as csv_file:
            csv_reader = py_csv.reader(csv_file, delimiter=',')
            fields = next(csv_reader, None)
            for f in fields:
                rows[f] = []            
            for row in csv_reader:
                for f, v in zip(fields, row):
                    rows[f].append(v)
                    
        return (fields, rows)