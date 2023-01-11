# visual data from apple watch

import xml.etree.ElementTree as ET
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# menu to select type of data
def print_menu():
    print('1. Average heartbeat per day')
    print('2. Number of steps per day')
    print('0. Exit')

# return a color based on a linear colormap
def get_color(value,max_value,min_value):
    # normalize the value to a range of 0-1
    norm_value = (float(value) - float(min_value)) / (float(max_value) - float(min_value))
    # create a colormap that maps the normalized value to a color
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["white","black"])
    # return the color
    return cmap(norm_value)

# opens xml
def open_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return root

# take data and 'clean' it 
def open_data(type):
    data = []
    for record in root.findall('./Record'):
        if record.get('type') == type:
            value = float(record.get('value'))
            end_date = record.get('endDate')
            date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S %z')
            formatted_date = date.strftime('%Y-%m-%d')
            data.append((str(formatted_date), int(value)))
    return data


path=input('Path of export.xml file : ')
path=path.replace("'", "")

while True:
    print_menu()
    choice = input('Choose data to visualise: ')
    if choice == '1':
        type='HKQuantityTypeIdentifierHeartRate'
        root=open_xml(path)
        data=open_data(type)
        dates, values = [row[0] for row in data], [row[1] for row in data]
        grouped_values = {}
        for value, date in zip(values, dates):
            if str(date) not in grouped_values:
                grouped_values[date] = []
            grouped_values[date].append(value)
        date_sums = []
        for date, values in grouped_values.items():
            date_sums.append((date, np.mean(values)))
        date_sums = sorted(date_sums, key=lambda x: x[0])
        dates, sums = zip(*date_sums)
        fig, ax = plt.subplots()
        for date, sum_val in zip(dates, sums):
            ax.axvline(date, color=get_color(sum_val,max(sums),min(sums)))
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            ax.yaxis.set_ticks_position('none')
            ax.yaxis.set_ticks([])
        #plt.savefig("PATH", dpi=800)
        plt.show()
    elif choice == '2':
        type='HKQuantityTypeIdentifierStepCount'
        root=open_xml(path)
        data=open_data(type)
        dates, values = [row[0] for row in data], [row[1] for row in data]
        grouped_values = {}
        for value, date in zip(values, dates):
            if str(date) not in grouped_values:
                grouped_values[date] = []
            grouped_values[date].append(value)
        date_sums = []
        for date, values in grouped_values.items():
            date_sums.append((date, sum(values)))
        date_sums = sorted(date_sums, key=lambda x: x[0])
        dates, sums = zip(*date_sums)
        fig, ax = plt.subplots()
        for date, sum_val in zip(dates, sums):
            ax.axvline(date, color=get_color(sum_val,max(sums),min(sums)))
            ax.xaxis.set_visible(False)
            ax.yaxis.set_visible(False)
            ax.yaxis.set_ticks_position('none')
            ax.yaxis.set_ticks([])
        #plt.savefig("PATH", dpi=800)
        plt.show()
    elif choice == '0':
        print('Exiting...')
        break
    else:
        print('Invalid choice. Try again.')
