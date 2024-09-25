import numpy as np
import math
import matplotlib.pyplot as plt

# Параметры
income_per_hour = {'crane': 2500, 'bulldozer': 2300}
cost_per_hour = {'crane': 2500, 'bulldozer': 2300}
repair_cost_per_hour = {6: 2100, 3: 1600, 'overhead': 400}
mean_working_time = {'crane': 4, 'bulldozer': 6}  # in hours
mean_repair_time = {('crane', 3): 2, ('crane', 6): 1, ('crane', 'both'): 0.25,
                    ('bulldozer', 6): 2, ('bulldozer', 'both'): 1.5}

num_of_days = input("Введите кол-во дней (итераций) расчёта: ")

class table:
    def __init__(self, xTable, xMatrix):
        self.table = xTable
        self.matrix = xMatrix

# Функция для генерации времени до отказа
def generate_failure_time(machine):
    return np.random.exponential(mean_working_time[machine] * 60)

# Функция для генерации времени ремонта
def generate_repair_time(machine, team):
    return np.random.exponential(mean_repair_time[(machine, team)] * 60)

def define_status(element, status):
    if element == 'crane' or element == 'bulldozer':
        if status == 'Работа':
            return 1
        elif status == 'Простой':
            return 0
        elif status == 'Ремонт':
            return -1
    else:
        if status == 'Занята краном' or status == 'Занята бульдозером':
            return 1
        elif status == 'Свободна':
            return 0


def simulate_one_day(with_third_class, need_to_display = False):
    total_income = 0
    total_cost = 0
    working_minutes = {'crane': 0, 'bulldozer': 0}
    repair_minutes = {'6': 0, '3': 0}

    crane_time = math.ceil(generate_failure_time('crane'))
    bulldozer_time = math.ceil(generate_failure_time('bulldozer'))
    status = {'crane':'Работа', 'bulldozer':'Работа', '3': 'Свободна', '6': 'Свободна'}

    y_crane = []
    y_bulldozer = []
    y_6 = []
    y_3 = []

    if crane_time >= 16*60:
        working_minutes['crane'] = 16*60
    if bulldozer_time >= 16*60:
        working_minutes['bulldozer'] = 16*60
    else:
        for i in range(1, 16*60+1):

            if status['crane'] == 'Работа':
                working_minutes['crane'] += 1
            if status['bulldozer'] == 'Работа':
                working_minutes['bulldozer'] += 1
            if status['3'] == 'Занята краном' or status['3'] == 'Занята бульдозером':
                repair_minutes['3'] += 1
            if status['6'] == 'Занята краном' or status['6'] == 'Занята бульдозером':
                repair_minutes['6'] += 1

            y_crane.append(define_status('crane', status['crane']))
            y_bulldozer.append(define_status('bulldozer', status['bulldozer']) + 3)
            y_6.append(define_status('6', status['6']) + 5)
            y_3.append(define_status('3', status['3']) + 7)

            priority = [crane_time if crane_time < bulldozer_time else bulldozer_time,'crane' if crane_time < bulldozer_time else 'bulldozer']

            if i == priority[0]:
                if priority[1] == 'crane':
                    if status['crane'] == 'Работа' or status['crane'] == 'Простой':
                        if with_third_class:
                            if status['3'] == 'Свободна' and status['6'] == 'Свободна':
                                status['crane'] = 'Ремонт'
                                status['3'] = 'Занята краном'
                                status['6'] = 'Занята краном'
                                repair = math.ceil(generate_repair_time('crane', 'both'))
                                if crane_time + repair <= 16 * 60:
                                    crane_time += repair
                                else: crane_time = 16 * 60
                            elif status['3'] == 'Свободна':
                                status['crane'] = 'Ремонт'
                                status['3'] = 'Занята краном'
                                repair = math.ceil(generate_repair_time('crane', 3))
                                if crane_time + repair <= 16 * 60:
                                    crane_time += repair
                                else: crane_time = 16 * 60
                            elif status['6'] == 'Свободна':
                                status['crane'] = 'Ремонт'
                                status['6'] = 'Занята краном'
                                repair = math.ceil(generate_repair_time('crane', 6))
                                if crane_time + repair <= 16 * 60:
                                    crane_time += repair
                                else: crane_time = 16 * 60
                            elif status['3'] == 'Занята бульдозером' and status['6'] == 'Занята бульдозером':
                                status['crane'] = 'Простой'
                                crane_time += 1
                        else:
                            if status['6'] == 'Занята бульдозером':
                                status['crane'] = 'Простой'
                                crane_time += 1
                            elif status['6'] == 'Свободна':
                                status['crane'] = 'Ремонт'
                                status['6'] = 'Занята краном'
                                repair = math.ceil(generate_repair_time('crane', 6))
                                if crane_time + repair <= 16 * 60:
                                    crane_time += repair
                                else: crane_time = 16 * 60
                        
                    elif status['crane'] == 'Ремонт':
                        status['crane'] = 'Работа'
                        if status['3'] == 'Занята краном' and with_third_class:
                            status['3'] = 'Свободна'
                        if status['6'] == 'Занята краном':
                            status['6'] = 'Свободна'
                        repair = math.ceil(generate_failure_time('crane'))
                        if crane_time + repair <= 16 * 60:
                            crane_time += repair
                        else: crane_time = 16 * 60

                if priority[1] == 'bulldozer':
                    if status['bulldozer'] == 'Работа' or status['bulldozer'] == 'Простой':
                        if status['6'] == 'Свободна' and status['3'] == 'Свободна' and with_third_class:
                            status['bulldozer'] = 'Ремонт'
                            status['3'] = 'Занята бульдозером'
                            status['6'] = 'Занята бульдозером'
                            repair = math.ceil(generate_repair_time('bulldozer', 'both'))
                            if bulldozer_time + repair <= 16 * 60:
                                    bulldozer_time += repair
                            else: bulldozer_time = 16 * 60
                        elif status['6'] == 'Свободна':
                            status['bulldozer'] = 'Ремонт'
                            status['6'] = 'Занята бульдозером'
                            repair = math.ceil(generate_repair_time('bulldozer', 6))
                            if bulldozer_time + repair <= 16 * 60:
                                    bulldozer_time += repair
                            else: bulldozer_time = 16 * 60
                        else:
                            status['bolldozer'] = 'Простой'
                            bulldozer_time += 1 
                    elif status['bulldozer'] == 'Ремонт':
                        status['bulldozer'] = 'Работа'
                        if status['3'] == 'Занята бульдозером' and with_third_class:
                            status['3'] = 'Свободна'
                        if status['6'] == 'Занята бульдозером':
                            status['6'] = 'Свободна'
                        repair = math.ceil(generate_failure_time('bulldozer'))
                        if bulldozer_time + repair <= 16 * 60:
                            bulldozer_time += repair
                        else: bulldozer_time = 16 * 60
                        if status['crane'] == 'Простой':
                            crane_time += 1
                
    # Рассчитываем доход и расходы
    for machine in ['crane', 'bulldozer']:
        total_income += working_minutes[machine] * income_per_hour[machine]

    total_cost += repair_minutes['6']/60 * repair_cost_per_hour[6] + repair_minutes['3']/60 * (repair_cost_per_hour[3] if with_third_class else 0) + (repair_minutes['3'] + repair_minutes['6']) * repair_cost_per_hour['overhead']

    if need_to_display:
        title = "С 3 бригадой" if with_third_class else "Без 3 бригады"
        print (title)
        print (f"Работа бульдозера: {working_minutes['bulldozer']}\nРабота крана: {working_minutes['crane']}")
        if with_third_class:
            print (f"Работа 3 бригады: {repair_minutes['3']}")
        print (f"Работа 6 бригады: {repair_minutes['6']}")

        x = np.arange(960)
        plt.step(x, y_crane, where='post', label='Кран')
        plt.step(x, y_bulldozer, where='post', label='Бульдозер')
        plt.step(x, y_6, where='post', label='6 бригада')
        if with_third_class:
            plt.step(x, y_3, where='post', label='3 бригада')
            plt.plot(x, [7]*960, color='grey', alpha=0.5)
        plt.plot(x, [0]*960, color='grey', alpha=0.5)
        plt.plot(x, [3]*960, color='grey', alpha=0.5)
        plt.plot(x, [5]*960, color='grey', alpha=0.5)
        plt.grid(axis='x', color='0.95')
        plt.legend()
        plt.title(title)
        plt.show()
        print (total_income, total_cost)

    return np.round(float(total_income), 2), np.round(float(total_cost), 2)


# Симулируем работу на протяжении многих дней для статистики
def simulate_days(days, with_third_class, show_day):
    total_income = 0
    total_cost = 0
    print ("День ", show_day)
    for day in range(days):
        if day == int(show_day):
            income, cost = simulate_one_day(with_third_class, True)
        else: income, cost = simulate_one_day(with_third_class)
        total_income += income
        total_cost += cost
    return total_income, total_cost

# Расчет и вывод итогов
def make_decision(days_to_simulate):
    show_day = input("Введите день для проверки: ")

    income_with_both, cost_with_both = simulate_days(days_to_simulate, True, show_day)
    profit_with_both = income_with_both - cost_with_both

    income_with_sixth_only, cost_with_sixth_only = simulate_days(days_to_simulate, False, show_day)
    profit_with_sixth_only = income_with_sixth_only - cost_with_sixth_only

    print(f"С обоими слесарями: Доход = {np.round(income_with_both,2)}, Расход = {np.round(cost_with_both,2)}, Прибыль = {np.round(profit_with_both,2)}")
    print(f"Только со слесарем 6-го разряда: Доход = {np.round(income_with_sixth_only,2)}, Расход = {np.round(cost_with_sixth_only,2)}, Прибыль = {np.round(profit_with_sixth_only,2)}")

    if profit_with_sixth_only > profit_with_both:
        print("Увольнение слесаря 3-го разряда экономически целесообразно.")
    else:
        print("Увольнение слесаря 3-го разряда нецелесообразно с экономической точки зрения.")

# Применяем функцию для итогового решения
make_decision(int(num_of_days))