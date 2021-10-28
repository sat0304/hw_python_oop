import string
from typing import List, Dict

minutes: int = 60
milli: int = 1000
one: int = 1
step_lenght: float = 0.65
flipper_lenght: float = 1.38
run_coeff_1: int = 18
run_coeff_2: int = 20
walk_coeff_1: float = 0.035
walk_coeff_2: float = 0.029
swim_coeff_1: float = 1.1
swim_coeff_2: int = 2

type_training: List[str] = [
    'Training',
    'Running',
    'SportsWalking',
    'Swimming']


def trunker(number: float) -> float:
    """Функция оставляет только три цифры после запятой."""
    result: float
    result = number * milli // one / milli
    return result


class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __init__(
            self, training_type: str, duration: float, distance: float,
            speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> string:
        text: string
        text = ('Тип тренировки: ' + str(self.training_type) + '; Длительность: '
        + str(self.duration) + ' ч.;  Дистанция: ' + str(self.distance) + ' км; Ср. скорость: '
        + str(self.speed) + ' км/ч; Потрачено ккал: ' + str(self.calories) + '.')
        return text


class Training:
    """Базовый класс тренировки."""
    name: str
    action: int
    duration: float
    weight: float
    weight: float
    M_IN_KM: int = milli
    LEN_STEP: float = step_lenght

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.name = type_training[0]
        self.action = action
        self.duration = duration
        self.weight = weight
        self.M_IN_KM = milli
        self.LEN_STEP = step_lenght

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float
        distance = self.action * Training.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = 0.0
        return spent_calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(
            self.name,
            trunker(self.duration),
            trunker(self.get_distance()),
            trunker(self.get_mean_speed()),
            trunker(self.get_spent_calories()))
        return message


class Running(Training):
    """Тренировка: бег."""
    name: str
    action: int
    duration: float
    weight: float

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
        self.name = type_training[1]

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float
        num1: float
        num2: float
        num1 = run_coeff_1 * self.get_mean_speed() - run_coeff_2
        num2 = self.weight * self.duration * minutes
        spent_calories = num1 * num2 / self.M_IN_KM
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    name: str
    action: int
    duration: float
    weight: float
    height: float

    def __init__(
            self, action: int, duration: float, weight: float,
            height: float) -> None:
        super().__init__(action, duration, weight)
        self.name = type_training[2]
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float
        num1: float
        num2: float
        num3: float
        num1 = walk_coeff_1 * self.weight
        num2 = self.get_mean_speed() ** 2 // self.height
        num3 = walk_coeff_2 * self.weight
        spent_calories = (num1 + num2 * num3) * self.duration * minutes
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    name: str
    action: int
    duration: float
    weight: float
    length_pool: int
    count_pool: int
    LEN_STEP: float = flipper_lenght

    def __init__(
            self, action: int, duration: float, weight: float,
            length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.name = type_training[3]
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.LEN_STEP = flipper_lenght

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float
        distance = self.action * Swimming.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float
        numb1: float
        numb1 = self.length_pool * self.count_pool
        mean_speed = numb1 / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float
        numb2: float
        numb2 = self.get_mean_speed() + swim_coeff_1
        spent_calories = numb2 * swim_coeff_2 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    sports: Dict[str, Training] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming}
    for sport in sports:
        if sport == workout_type:
            training = sports[sport](*data)
            return training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
