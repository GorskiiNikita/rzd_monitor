import datetime
import json
import time

import requests

import tg_api

from train import SetOfTrains, Train, CarGroup


URL = 'https://ticket.rzd.ru/apib2b/p/Railway/V1/Search/TrainPricing?service_provider=B2B_RZD'
DATA = {
    "Origin": "2004540",
    "Destination": "2004000",
    "DepartureDate": "2022-01-07T00:00:00",
    "TimeFrom": 0,
    "TimeTo": 24,
    "CarGrouping": "DontGroup",
    "GetByLocalTime": True,
    "SpecialPlacesDemand": "StandardPlacesAndForDisabledPersons"
}


class RZDMonitor:
    def __init__(self, target_date):
        self.set_of_trains = None
        self.target_date = target_date

    def run_loop(self):
        """
        Основной цикл мониторинга ржд.
        :return:
        """
        while True:
            source_trains = self._load_data()
            # Сравнить данные с предыдущим парсингом. Если данные отличаются - вывести их.
            new_set_of_trains = SetOfTrains()
            for source_train in source_trains:
                new_train = Train(origin_station_name=source_train.get('OriginStationName', ''),
                                  destination_station_name=source_train.get('DestinationStationName', ''),
                                  train_number=source_train.get('TrainNumber', ''))
                for source_car_group in source_train['CarGroups']:
                    new_train.add_car_group(CarGroup(car_type_name=source_car_group.get('CarTypeName', ''),
                                                     place_quantity=source_car_group.get('TotalPlaceQuantity', ''),
                                                     desc=source_car_group.get('CarDescriptions', '')))
                new_set_of_trains.add_train(new_train)
            if not self.set_of_trains == new_set_of_trains:
                self._set_trains(new_set_of_trains)
                self._tg_alert()

            time.sleep(3)

    def _load_data(self):
        """
        Загружаем данные от ржд.
        :return:
        """
        for i in range(5):
            try:
                return json.loads(requests.post(URL, json=DATA).text).get('Trains')
            except:
                pass

    def _set_trains(self, set_of_trains):
        self.set_of_trains = set_of_trains

    def _tg_alert(self):
        msg = []
        for train in self.set_of_trains:
            msg.append('---------')
            msg.append(f'{self.target_date.strftime("%d.%m.%Y")} / {train}')
            for car_group in train.car_groups:
                msg.append(
                    str(car_group)
                )
            msg.append('---------')
        tg_api.invoke_telegram('sendMessage', chat_id=742742965, text='\n'.join(msg))


def main():
    rzd_monitor = RZDMonitor(datetime.datetime(year=2021, month=1, day=6))
    rzd_monitor.run_loop()


if __name__ == '__main__':
    main()
