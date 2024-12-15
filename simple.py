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

def schedule_routes(driver_list, num_routes, traffic_route_time, work_hours):
    schedule = {driver: [] for driver in driver_list}
    all_routes = []

    for _ in range(num_routes):
        start_time = random.choice(route_times)
        end_time = calculate_route_end(start_time, traffic_route_time)
        all_routes.append((start_time, end_time))

    driver_index = 0
    for route in all_routes:
        assigned = False
        attempts = 0
        while not assigned and attempts < len(driver_list):
            driver = driver_list[driver_index]
            work_start, work_end = work_hours[driver]
            if (
                not is_time_overlap(route[0], route[1], schedule[driver]) and
                is_within_work_hours(route[0], route[1], work_start, work_end)
            ):
                schedule[driver].append(route)
                assigned = True
            driver_index = (driver_index + 1) % len(driver_list)
            attempts += 1
        if not assigned:
            schedule_text.insert(END, f"Маршрут с {route[0]} до {route[1]} невозможно распределить!\n")

    return schedule

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
        if not drivers_A:
            schedule_text.insert(END, "\nНе назначено водителей типа A для создания расписания.\n")
            return

        work_hours_A = {driver: (8, 16) for driver in drivers_A}  # 8:00 до 16:00
        schedule = schedule_routes(drivers_A, num_routes, traffic_route_time, work_hours_A)
        display_schedule(schedule)
    except ValueError:
        schedule_text.insert(END, "\nОшибка: Введите корректное число маршрутов.\n")

def generate_schedule_B():
    try:
        num_routes = int(num_routes_entry.get())
        if num_routes <= 0:
            schedule_text.insert(END, "\nОшибка: Количество маршрутов должно быть положительным числом.\n")
            return
        if not drivers_B:
            schedule_text.insert(END, "\nНе назначено водителей типа B для создания расписания.\n")
            return

        work_hours_B = {driver: (0, 24) for driver in drivers_B}  # 24 часа
        schedule = schedule_routes(drivers_B, num_routes, traffic_route_time, work_hours_B)
        display_schedule(schedule)
    except ValueError:
        schedule_text.insert(END, "\nОшибка: Введите корректное число маршрутов.\n")


route_times = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
traffic_route_time = 1
drivers_A = ["Водитель_A1", "Водитель_A2", "Водитель_A3"]
drivers_B = ["Водитель_B1", "Водитель_B2"]
root = tk.Tk()
root.title("Распределение маршрутов")
root.geometry("800x600")
root.configure(bg="#F0F8FF")

label_font = ("Arial", 12)
button_font = ("Arial", 14, "bold")
entry_font = ("Arial", 12)

input_frame = Frame(root, bg="#F0F8FF")
input_frame.pack(pady=20)

num_routes_label = Label(input_frame, text="Введите количество маршрутов:", bg="#F0F8FF", font=label_font)
num_routes_label.grid(row=0, column=0, padx=10)
num_routes_entry = Entry(input_frame, width=10, font=entry_font)
num_routes_entry.grid(row=0, column=1, padx=10)

button_frame = Frame(root, bg="#F0F8FF")
button_frame.pack(pady=20)

generate_button_A = Button(button_frame, text="Создать расписание для типа A", command=generate_schedule_A,
                           bg="#4CAF50", fg="#FFFFFF", font=button_font, relief="raised", bd=3,
                           width=30, height=2)
generate_button_A.pack(side="left", padx=10)

generate_button_B = Button(button_frame, text="Создать расписание для типа B", command=generate_schedule_B,
                           bg="#FF5722", fg="#FFFFFF", font=button_font, relief="raised", bd=3,
                           width=30, height=2)
generate_button_B.pack(side="left", padx=10)

output_frame = Frame(root, bg="#F0F8FF")
output_frame.pack(pady=20)

scrollbar = Scrollbar(output_frame)
schedule_text = Text(output_frame, width=80, height=15, font=("Courier", 11), wrap="word", bg="#FFFFFF", fg="#000000",
                     yscrollcommand=scrollbar.set)
scrollbar.config(command=schedule_text.yview)
scrollbar.pack(side="right", fill="y")
schedule_text.pack(side="left", fill="both")

root.mainloop()