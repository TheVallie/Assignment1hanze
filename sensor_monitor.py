import random
import csv
import numpy as np
import matplotlib.pyplot as plt


def get_user_input():
    while True:
        try:
            sensor = input('Sensor type: ')
            count = int(input('Number of readings: '))
            minimum = float(input('Minimum value: '))
            maximum = float(input('Maximum value: '))
            threshold = float(input('Alert threshold: '))

            if count <= 0:
                print('Number of readings must be positive.')
            elif minimum >= maximum:
                print('Minimum must be smaller than maximum.')
            else:
                return sensor, count, minimum, maximum, threshold
        except ValueError:
            print('Please enter valid numbers.')


def generate_readings(count, minimum, maximum):
    random.seed(25)
    readings = []
    for i in range(count):
        value = random.uniform(minimum, maximum)
        readings.append(value)
    return readings


def find_outliers(readings, threshold):
    outliers = []
    for value in readings:
        if value > threshold:
            outliers.append(value)
    return outliers


def calculate_statistics(readings, threshold):
    outliers = find_outliers(readings, threshold)
    print('Number of readings:', len(readings))
    print('Mean:', round(np.mean(readings), 2))
    print('Minimum:', round(np.min(readings), 2))
    print('Maximum:', round(np.max(readings), 2))
    print('Standard deviation:', round(np.std(readings), 2))
    print('Number above threshold:', len(outliers))
    print('Readings above threshold:')
    for value in outliers:
        print(round(value, 2))


def save_readings(readings, filename):
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Sample number', 'Sensor reading'])
            for i in range(len(readings)):
                writer.writerow([i + 1, readings[i]])
        print('Data saved to', filename)
    except OSError:
        print('Could not save the CSV file.')


def load_readings(filename):
    readings = []
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                readings.append(float(row[1]))
    except (OSError, ValueError, IndexError, csv.Error):
        print('Could not load the CSV file. Check the filename and format.')
        return []
    return readings


def plot_readings(readings, threshold, sensor):
    plt.figure()
    plt.plot(range(1, len(readings) + 1), readings, label='Readings')
    plt.axhline(threshold, color='red', linestyle='--', label='Alert threshold')
    plt.title(sensor + ' readings')
    plt.xlabel('Sample number')
    plt.ylabel(sensor + ' value')
    plt.grid(True)
    plt.legend()


def plot_histogram(readings, sensor):
    plt.figure()
    plt.hist(readings, bins=10, edgecolor='black')
    plt.title(sensor + ' distribution')
    plt.xlabel(sensor + ' value')
    plt.ylabel('Frequency')
    plt.grid(True)


def main():
    print('1. Generate new readings')
    print('2. Load existing CSV file')
    choice = input('Choose 1 or 2: ')

    if choice == '1':
        sensor, count, minimum, maximum, threshold = get_user_input()
        readings = generate_readings(count, minimum, maximum)
        save_readings(readings, 'sensor_data.csv')
    elif choice == '2':
        filename = input('CSV filename: ')
        readings = load_readings(filename)
        if len(readings) == 0:
            print('No readings available.')
            return
        sensor = input('Sensor type: ')
        while True:
            try:
                threshold = float(input('Alert threshold: '))
                break
            except ValueError:
                print('Please enter a valid number.')
    else:
        print('Invalid choice. Please choose 1 or 2.')
        return

    calculate_statistics(readings, threshold)
    plot_readings(readings, threshold, sensor)
    plot_histogram(readings, sensor)
    plt.show()


if __name__ == '__main__':
    main()

