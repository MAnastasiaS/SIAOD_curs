import random
import tkinter as tk
from tkinter import Button, END, Text, Label, Entry, Frame, Scrollbar

def is_time_overlap(start1, end1, routes):
    for start2, end2 in routes:
        if start1 <= end2 and start2 <= end1:
            return True
    return False

def is_within_work_hours(start_time, end_time, work_start, work_end):
    return work_start <= start_time < work_end and work_start < end_time <= work_end

def calculate_route_end(start_time, route_duration):
    return start_time + route_duration

def genetic_algorithm(drivers, num_routes, traffic_route_time, work_hours, generations=100, population_size=20):
    def generate_initial_population():
        population = []
        for _ in range(population_size):
            individual = {driver: [] for driver in drivers}
            for _ in range(num_routes):
                start_time = random.choice(route_times)
                end_time = calculate_route_end(start_time, traffic_route_time)
                driver = random.choice(drivers)
                individual[driver].append((start_time, end_time))
            population.append(individual)
        return population

    def fitness(individual):
        score = 0
        for driver, routes in individual.items():
            work_start, work_end = work_hours[driver]
            for i, (start1, end1) in enumerate(routes):
                if not is_within_work_hours(start1, end1, work_start, work_end):
                    score -= 10
                for j, (start2, end2) in enumerate(routes):
                    if i != j and is_time_overlap(start1, end1, [(start2, end2)]):
                        score -= 5
        return score

    def crossover(parent1, parent2):
        child = {driver: [] for driver in drivers}
        for driver in drivers:
            routes1 = parent1[driver]
            routes2 = parent2[driver]
            child[driver] = routes1[:len(routes1)//2] + routes2[len(routes2)//2:]
        return child

    def mutate(individual):
        driver = random.choice(drivers)
        if individual[driver]:
            individual[driver].pop(random.randint(0, len(individual[driver])-1))
        start_time = random.choice(route_times)
        end_time = calculate_route_end(start_time, traffic_route_time)
        individual[driver].append((start_time, end_time))

    def selection(population):
        return sorted(population, key=lambda x: fitness(x), reverse=True)[:population_size//2]

    population = generate_initial_population()
    for generation in range(generations):
        new_population = []
        selected = selection(population)
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected, 2)
            child = crossover(parent1, parent2)
            if random.random() < 0.2:
                mutate(child)
            new_population.append(child)
        population = new_population

    best_solution = max(population, key=lambda x: fitness(x))
    return best_solution

def display_schedule(schedule):
    schedule_text.delete(1.0, END)
    schedule_text.insert(END, f"{'Водитель':<15}{'Маршрут (с - по)'}\n")
    schedule_text.insert(END, "-" * 50 + "\n")
    for driver, routes in schedule.items():
        for start, end in routes:
            schedule_text.insert(END, f"{driver:<15}{start}:00 - {end}:00\n")
        schedule_text.insert(END, "\n")
def generate_schedule_A():
    try:
        num_routes = int(num_routes_entry.get())
        if num_routes <= 0:
            schedule_text.insert(END, "\nОшибка: Количество маршрутов должно быть положительным числом.\n")
            return

        work_hours_A = {driver: (8, 16) for driver in drivers_A}
        schedule = genetic_algorithm(drivers_A, num_routes, traffic_route_time, work_hours_A)
        display_schedule(schedule)
    except ValueError:
        schedule_text.insert(END, "\nОшибка: Введите корректное число маршрутов.\n")
def generate_schedule_В():
    try:
        num_routes = int(num_routes_entry.get())
        if num_routes <= 0:
            schedule_text.insert(END, "\nОшибка: Количество маршрутов должно быть положительным числом.\n")
            return

        work_hours_A = {driver: (0, 24) for driver in drivers_A}
        schedule = genetic_algorithm(drivers_B, num_routes, traffic_route_time, work_hours_A)
        display_schedule(schedule)
    except ValueError:
        schedule_text.insert(END, "\nОшибка: Введите корректное число маршрутов.\n")

route_times = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
traffic_route_time = 1
drivers_A = ["Водитель_A1", "Водитель_A2", "Водитель_A3"]
drivers_B = ["Водитель_B1", "Водитель_B2"]


root = tk.Tk()
root.title("Генетический алгоритм для распределения маршрутов")
root.geometry("800x600")
root.configure(bg="#F0F8FF")
label_font = ("Arial", 12)
button_font = ("Arial", 14, "bold")
input_frame = Frame(root, bg="#F0F8FF")
input_frame.pack(pady=20)
num_routes_label = Label(input_frame, text="Введите количество маршрутов:", bg="#F0F8FF", font=label_font)
num_routes_label.grid(row=0, column=0, padx=10)
num_routes_entry = Entry(input_frame, width=10, font=label_font)
num_routes_entry.grid(row=0, column=1, padx=10)
button_frame = Frame(root, bg="#F0F8FF")
button_frame.pack(pady=20)
generate_button_A = Button(button_frame, text="Создать расписание для типа A", command=generate_schedule_A,
                           bg="#4CAF50", fg="#FFFFFF", font=button_font, width=30, height=2)
generate_button_A.pack()
generate_button_B = Button(button_frame, text="Создать расписание для типа B", command=generate_schedule_B,
                           bg="#4CAF50", fg="#FFFFFF", font=button_font, width=30, height=2)
generate_button_B.pack()
output_frame = Frame(root, bg="#F0F8FF")
output_frame.pack(pady=20)
scrollbar = Scrollbar(output_frame)
schedule_text = Text(output_frame, width=80, height=15, wrap="word", yscrollcommand=scrollbar.set)
scrollbar.config(command=schedule_text.yview)
scrollbar.pack(side="right", fill="y")
schedule_text.pack(side="left", fill="both")

root.mainloop()