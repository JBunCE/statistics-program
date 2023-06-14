import math

import numpy
import pandas
import statistics
import scipy.stats as stats


def get_range(data):
    min_data = data[0]
    max_data = data[-1]
    return max_data - min_data


class CalculatorUtil:
    def __init__(self):
        self.limit_inf = []
        self.limit_sup = []
        self.class_mark = []
        self.recurrence = []
        self.recurrence_relative = []

        self.median = None
        self.arithmetic_average = 0.0
        self.mean = 0.0
        self.trunc_mean = 0.0
        self.geometric_mean = 0.0
        self.mode = None
        self.skew = 0.0
        self.skew_position = ""

        self.variance = None
        self.standard_deviation = None

    def calculate(self, array_data):
        if type(array_data[0]) == str:
            data = list(set(array_data))
            for value in data:
                recurrence = array_data.tolist().count(str(value))
                self.recurrence.append(recurrence)
                self.recurrence_relative.append(recurrence / len(array_data) * 100)

            sorted_data = sorted(array_data)
            size = len(sorted_data)
            if size % 2 == 1:
                self.median = sorted_data[size // 2]
            else:
                self.median = (sorted_data[size // 2 - 1], sorted_data[size // 2])

            params = {
                "mediana": self.median,
                "moda": statistics.mode(array_data)
            }

            final_data = pandas.DataFrame({
                "marca_de_clase": data,
                "frecuencia": self.recurrence
            })

            return {"recurrence_table": final_data, "params": params}
        else:
            sorted_data = sorted(array_data)

            data_range = get_range(sorted_data)
            classes = round(1 + (3.3 * math.log10(len(array_data))))
            class_width = data_range / classes

            self.__generate_values_for_table(data=sorted_data,
                                             class_num=classes,
                                             class_width=class_width,
                                             last_index=sorted_data[0])
            cumulative_recurrence = numpy.array(self.recurrence).cumsum()

            self.__generate_params(array_data)

            params = {
                "rango": data_range,
                "mediana": self.median,
                "moda": self.mode,
                "media": self.mean,
                "media truncada": self.trunc_mean,
                "media geometrica": self.geometric_mean,
                "varianza": self.variance,
                "desviacion estandar": self.standard_deviation,
                "sesgo": self.skew,
                "posicion del sesgo": self.skew_position
            }

            recurrence_table = pandas.DataFrame({
                "limite_inferior": self.limit_inf,
                "limite_superior": self.limit_sup,
                "marca_de_clase": self.class_mark,
                "frecuencia": self.recurrence,
                "frecuencia_relativa": self.recurrence_relative,
                "frecuencia_acumulada": cumulative_recurrence
            })

            group_params = self.__generate_group_params(array_data)

            return {"recurrence_table": recurrence_table,
                    "params": params,
                    "group_params": group_params}

    def __generate_params(self, data):
        self.mean = statistics.mean(data)
        self.mode = statistics.mode(data)

        self.arithmetic_average = sum(data) / len(data)
        self.trunc_mean = stats.trim_mean(data, 0.2)
        self.geometric_mean = round(statistics.geometric_mean(data), 1)
        self.skew = stats.skew(data)

        sorted_data = sorted(data)
        middle_index = len(data) // 2
        if middle_index % 2 == 0:
            self.median = round((sorted_data[middle_index] + sorted_data[middle_index - 1]) / 2, 4)
        else:
            self.median = sorted_data[middle_index]

        if self.skew < 0:
            self.skew_position = "sesgo a la izquierda"
        else:
            self.skew_position = "sesgo a la derecha"

        summation = 0
        for value in data:
            summation += pow(value - self.arithmetic_average, 2)

        self.variance = summation / len(data)
        self.standard_deviation = math.sqrt(self.variance)

    def __generate_group_params(self, data):
        recurrence = self.recurrence
        class_mark = self.class_mark
        class_number = len(class_mark)

        summ = 0
        for value in range(class_number):
            summ = round(summ + (recurrence[value] * class_mark[value]), 2)

        arithmetic_average = round(summ / len(data), 4)

        middle_index = class_number // 2
        if class_number % 2 == 0:
            middle = round((class_mark[middle_index] + class_mark[middle_index - 1]) / 2, 4)
        else:
            middle = class_mark[middle_index]

        mode = class_mark[numpy.argmax(recurrence)]

        summ = 0
        for x in range(class_number):
            summ += recurrence[x] * pow(class_mark[x], 2)
        variance = round((summ - len(data) * pow(arithmetic_average, 2)) / (len(data) - 1), 4)
        standard_deviation = round(math.sqrt(variance), 4)

        return {
            "mediana": middle,
            "moda": mode,
            "media": arithmetic_average,
            "varianza": variance,
            "desviacion estandar": standard_deviation,
        }

    def __generate_values_for_table(self, data: [], class_num: int, class_width: float, last_index: float):
        if class_num != 0:
            first_limit = last_index
            second_limit = round(first_limit + class_width, 4)
            recurrence = self.__count_recurrence(first_limit, second_limit, data, class_num)
            self.limit_inf.append(first_limit)
            self.limit_sup.append(second_limit)
            self.recurrence.append(recurrence)
            self.recurrence_relative.append(recurrence / len(data))
            self.class_mark.append(round((first_limit + second_limit) / 2, 2))
            self.__generate_values_for_table(data, class_num - 1, class_width, (last_index + class_width))

    def __count_recurrence(self, first_limit, second_limit, data, class_num):
        summ = 0
        for value in data:
            if value >= second_limit and value != class_num != 1:
                break
            if value >= first_limit:
                summ += 1
        return summ
