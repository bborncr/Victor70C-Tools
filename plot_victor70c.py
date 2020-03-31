import serial
import serial.tools.list_ports
import keyboard
import argparse
import parse_victor70c as vic
import datetime as dt
import csv
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

global ser
ser = serial.Serial()
ser.baudrate = 2400
global data_csv
data_csv = []

def setup():
    print('setup...')
    setup_arguments()
    keyboard.add_hotkey('space', recordData)
    print(f'connecting to port {port}...')
    global ser
    ser.port = port
    try:
        ser.open()
    except Exception as e:
        print('Error:', e)
        exit()
    print(f'connected to port {ser.name}.')

def setup_arguments():
    parser = argparse.ArgumentParser(description='Record data from VictorC Digital Multimeter')
    parser.add_argument('-p', '--port', default='COM2', type=str, help='Select serial port eg. COM2 or /dev/ttyS0')
    parser.add_argument('-f', '--file', default='data.txt', type=str, help='Choose filename for csv file')
    parser.add_argument('--continuous', action='store_true', 
            help='Enable to continuously record data to csv file. If not enabled use spacebar to record data points. ')
    parser.add_argument('--plot', action='store_true', help='Enable to plot data in separate window.')
    parser.add_argument('--ymin', default='0', type=int, help='Y minimum for plot')
    parser.add_argument('--ymax', default='100', type=int, help='Y maximum for plot')

    args = parser.parse_args()
    print('args:', args)
    global port
    port = args.port
    global file_name
    file_name = args.file
    global record_mode_continuous
    record_mode_continuous = args.continuous
    global isPlotting
    isPlotting = args.plot
    if isPlotting: # don't even load in the scope if not plotting
        global fig, ax, scope, yminimum, ymaximum
        yminimum = args.ymin
        ymaximum = args.ymax
        fig, ax = plt.subplots(num = 'VictorC Digital Multimeter')
        scope = Scope(ax, ymin=yminimum, ymax=ymaximum)

def recordData():
    global data_csv
    print('recording datapoint...')
    try:
        save_to_csv(data_csv)
    except Exception as e:
        print('Error:', e)

def save_to_csv(data):
    with open(file_name, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(data)

class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.1, ymin=0, ymax=100):
        self.ymin = ymin
        self.ymax = ymax
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(self.ymin, self.ymax)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,

def Main():
    setup()
    while True:
        try:
            if ser.in_waiting > 0:
                raw_data = ser.readline()
                # print(raw_data)
                data = vic.parse_victor70c(raw_data)
                num = data['NUM']
                units = data['UNITS']
                global data_csv
                data_csv = [dt.datetime.now(), num, units]
                #print('received data', num)
                if record_mode_continuous:
                    recordData()
                    if isPlotting:
                        scope.update(num)
                        plt.draw()
                        plt.pause(0.001)
        except Exception as e:
            print('Error:', e)

if __name__ == "__main__":
    Main()