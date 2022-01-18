class SetOfTrains:
    def __init__(self):
        self.trains = set()

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.trains == other.trains

    def __iter__(self):
        return iter(self.trains)

    def add_train(self, train):
        self.trains.add(train)



class Train:
    def __init__(self, origin_station_name, destination_station_name, train_number):
        self.origin_station_name = origin_station_name
        self.destination_station_name = destination_station_name
        self.train_number = train_number
        self.car_groups = set()

    def __hash__(self):
        return hash(self.train_number)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.train_number == other.train_number and self.car_groups == other.car_groups

    def __str__(self):
        return f'{self.train_number} | {self.origin_station_name} - {self.destination_station_name}'

    def add_car_group(self, car_group):
        self.car_groups.add(car_group)


class CarGroup:
    def __init__(self, car_type_name, place_quantity, desc):
        self.car_type_name = car_type_name
        self.place_quantity = place_quantity
        self.desc = desc

    def __hash__(self):
        return hash((self.car_type_name, self.place_quantity, str(self.desc)))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.car_type_name == other.car_type_name and self.place_quantity == other.place_quantity and self.desc == other.desc

    def __str__(self):
        desc = ' '.join([str(i) for i in self.desc if i])
        if desc:
            desc = f'({desc})'
        else:
            desc = ''
        return f'{self.car_type_name}: {self.place_quantity} {desc}'
