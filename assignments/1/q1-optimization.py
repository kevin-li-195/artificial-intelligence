import math
import random
import csv

test_range = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
test_steps = [0.01, 0.02, 0.03, 0.04 ,0.05, 0.06, 0.07, 0.08, 0.09, 0.1]

def prob(prev, next, temp):
    return(math.exp((next - prev)/temp))

def eval_func(x):
    try:
        return((math.sin((math.pow(x,2))/2))/math.sqrt(x))
    except ZeroDivisionError:
        return(0)
    except ValueError as e:
        return(-1)

def hill_climb(start, step, depth=1):
    med = eval_func(start)
    lo = eval_func(start - step)
    hi = eval_func(start + step)
    choice = max([lo, hi])
    if med >= choice:
        return(start, med, depth)
    elif choice == lo:
        return(hill_climb(start - step, step, depth=depth+1))
    else:
        return(hill_climb(start + step, step, depth=depth+1))

def simulated_annealing(start, step, temp, discount):
    epsilon = 0.000001
    depth = 0
    while True:
        depth += 1
        neighbours = [start + step, start - step]
        choice = random.choice(neighbours)
        candidate = eval_func(choice)
        base = eval_func(start)
        if temp < epsilon:
            return(start, base, depth)
        temp = temp * discount
        if base >= candidate:
            r = random.random()
            p = prob(base, candidate, temp)
            if r < p:
                start = choice
                continue
            else:
                continue
        else:
            start = choice
            continue

TEMPERATURE = 150
DISCOUNT = 0.99

hill_file = open("hill_climbing.csv", "wb")
simulated_annealing_file = open("simulated_annealing.csv", "wb")

hill_writer = csv.writer(hill_file, delimiter=",")
simulated_annealing_writer = csv.writer(simulated_annealing_file, delimiter=",")

for val in test_range:
    for step_size in test_steps:
        x, y, d = hill_climb(val, step_size)
        hill_writer.writerow([x, y, d])
        print("Hill Climbing: For the value " +
                str(val) +
                " and the step size " +
                str(step_size) +
                " the peak is at: " +
                str(hill_climb(val, step_size)))
for val in test_range:
    for step_size in test_steps:
        x, y, d = simulated_annealing(val, step_size, TEMPERATURE, DISCOUNT)
        simulated_annealing_writer.writerow([x, y, d])
        print("Simulated Annealing: For the value " +
                str(val) +
                " and the step size " +
                str(step_size) +
                " the peak is at: " +
                str(simulated_annealing(val, step_size, TEMPERATURE, DISCOUNT)))
