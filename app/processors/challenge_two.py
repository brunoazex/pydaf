from lib.datasets.flat import FlatDataSet
from lib.drivers.postgres import Postgres
from lib.processor import Processor

class ChallengeTwo(Processor):
    def __init__(self):
        self.dataset = FlatDataSet("ChallengeTwo", self._get_data())
        
    def _get_data(self):
        return Postgres.query("""
            SELECT
                cust.id AS customer_id,
                count(*) AS transactions_count
            FROM
                transactions t
            INNER JOIN
                cards crd ON t.card_number = crd.card_number
            INNER JOIN
                customers cust ON crd.customer_id = cust.id
            WHERE
                cust.segment = 'Diamond'
            GROUP BY
                cust.segment, cust.id
            HAVING
                COUNT(*) >= 40
            ORDER BY
                COUNT(*) DESC
         """)
         
    def run(self):
        self.dataset \
            .to_console() \
            .to_csv()

