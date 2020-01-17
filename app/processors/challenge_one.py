from lib.drivers.postgres import Postgres
from lib.datasets.pivot import PivotDataSet
from lib.processor import Processor
import pandas as pd

class ChallengeOne(Processor):
    def __init__(self):
        data = self._get_data()
        options = self._build_pivot_options()
        self.dataset = PivotDataSet("ChallengeOne", data, options) \
            .add_group_subtotals()
        
    def _get_data(self):
        return Postgres.query("""
            SELECT
                c.card_family,
                c.card_number,
                t.id AS transaction_id,
                t.value,
                f.fraud_flag
            FROM
                cards c
            LEFT JOIN
                transactions t on c.card_number = t.card_number
            LEFT JOIN
                frauds f on t.id = f.transaction_id
        """)
        
    def _build_pivot_options(self):
        return PivotDataSet.Options() \
            .has_index('card_family', 'card_number') \
            .has_values('transaction_id', 'fraud_flag', 'value') \
            .has_aggregate([
                ('transaction_id', 'count'),
                ('fraud_flag', 'sum'),
                ('value', 'sum')]) \
            .rename([
                ('transaction_id', 'transactions'),
                ('fraud_flag', 'frauds'),
                ('value', 'amount')
            ])
            
    def run(self):
        self.dataset \
            .to_console() \
            .to_csv()

   



