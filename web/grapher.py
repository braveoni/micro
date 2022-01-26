from random import randint
import pandas as pd

from web import db


class Graph:
    def __init__(self):
        self.df = pd.read_sql_table('doors', db.session.bind)
        self.colors = []

    @staticmethod
    def __generate_color():
        return f'rgb({randint(0,255)}, {randint(0,255)}, {randint(0,255)}, 0.3)'

    def __get(self, name):
        return self.df[name].unique().tolist()

    def __get_count(self, name):
        return self.df[name].value_counts().tolist()

    def __group(self, key, label, freq='5min'):
        return self.df.set_index(key).groupby(label).resample(freq).count()

    def __get_status(self, location):
        return self.df.loc[(self.df['close'].isnull()
                            & self.df['location'] == location)].empty

    @staticmethod
    def __to_strftime(time):
        return pd.to_datetime(time).strftime('%d-%m-%Y %H:%M')

    def get_doughnut(self):
        return {'labels': self.__get('location'), 'data': self.__get_count('location')}

    def get_line(self, freq='min'):
        data: pd.DataFrame = self.__group(
            'open', 'location', freq=freq).to_dict()['id']

        d = {}
        times = []

        for k, v in data.items():
            if k[0] in d:
                d[k[0]]['time'].append(self.__to_strftime(k[1]))
                d[k[0]]['value'].append(v)
            else:
                d[k[0]] = {'time': [self.__to_strftime(k[1])], 'value': [v]}

            if self.__to_strftime(k[1]) not in times:
                times.append(self.__to_strftime(k[1]))

        return {'data': [{
                'label': k,
                'data': v['value'],
                'backgroundColor': self.__generate_color(),
                'tension': .4,
                } for k, v in d.items()], 'labels': times}

    def get_table(self):
        locations = self.__get('location')

        return [{
            'location': location,
            'status': 'closed' if self.__get_status(location) else 'open'
        } for location in locations]
