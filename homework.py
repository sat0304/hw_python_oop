from typing import List, Dict

minutes: int = 60
step_length: float = 0.65
flipper_length: float = 1.38
milli: int = 1000
one: int = 1
run_coeff_1: int = 18
run_coeff_2: int = 20
walk_coeff_1: float = 0.035
walk_coeff_2: float = 0.029
swim_coeff_1: float = 1.1
swim_coeff_2: int = 2

type_training: List[str] = [
    f"""'Training',
    'Running',
    'SportsWalking',
    'Swimming'"""]

mess: List[str] = [
    f"""'Тип тренировки: ',
    ';',
    ' Длительность: ',
    ' ч.;',
    ' Дистанция: ',
    ' км;',
    ' Ср. скорость: ',
    ' км/ч;',
    ' Потрачено ккал: ',
    '.'"""]


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

    def get_message(self) -> str:
        text: str
        text = f"""{mess[0]}{self.training_type}{mess[1]}
            {mess[2]}{self.duration}{mess[3]}
            {mess[4]}{self.distance}{mess[5]}
            {mess[6]}{self.speed}{mess[7]}
            {mess[8]}{self.calories}{mess[9]}"""
        return text


class Training:
    """Базовый класс тренировки."""
    name: str
    action: int
    duration: float
    weight: float
    weight: float
    M_IN_KM: int
    LEN_STEP: float

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.name = type_training[0]
        self.action = action
        self.duration = duration
        self.weight = weight
        self.M_IN_KM = milli
        self.LEN_STEP = step_length

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return trunker(distance)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float
        mean_speed = self.get_distance() / self.duration
        return trunker(mean_speed)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = 0.0
        return trunker(spent_calories)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(
            self.name,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())
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
        return trunker(spent_calories)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    name: str
    action: int
    duration: float
    weight: float
    height: float

    def __init__(self, action: int, duration: float, weight: float,
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
        return trunker(spent_calories)


class Swimming(Training):
    """Тренировка: плавание."""
    name: str
    action: int
    duration: float
    weight: float
    length_pool: int
    count_pool: int
    LEN_STEP: float

    def __init__(self, action: int, duration: float, weight: float,
                length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.name = type_training[3]
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.LEN_STEP = flipper_length

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float
        numb1: float
        numb1 = self.length_pool * self.count_pool
        mean_speed = numb1 / self.M_IN_KM / self.duration
        return trunker(mean_speed)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float
        numb2: float
        numb2 = self.get_mean_speed() + swim_coeff_1
        spent_calories = numb2 * swim_coeff_2 * self.weight
        return trunker(spent_calories)


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
    info: str
    info = training.show_training_info().get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
