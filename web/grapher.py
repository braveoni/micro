import pandas as pd

from web import db
from web.models import Doors


class Graph:
    def __init__(self):
        self.df = pd.read_sql_table('doors', db.session.bind)

    def __get(self, name):
        return self.df[name].unique().tolist()

    def __get_count(self, name):
        return self.df[name].value_counts().tolist()

    def __group(self, key, freq='5min'):
        return self.df.groupby(pd.Grouper(key=key, freq=freq)).count()

    def get_doughnut(self):
        return {'labels': self.__get('location'), 'data': self.__get_count('location')}

    def get_line(self, freq='min') -> dict:
        data = self.__group('open', freq=freq)

        open_ = [pd.to_datetime(item).strftime('%d-%m-%Y %H:%M')
                 for item in data.index.tolist()]

        return {'labels': open_, 'data': data.values.tolist()}


if __name__ == '__main__':
    g = Graph()
    print(g.get('location'))
