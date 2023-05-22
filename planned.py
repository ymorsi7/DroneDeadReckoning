import time
import numpy as np
import matplotlib.pyplot as plt
from rktellolib import Tello

# Constants
ORIGIN = 0

class DroneSimulator:

    def __init__(self):
        self.fig, self.ax = plt.subplots(subplot_kw={'projection': '3d'})
        self.drone_info = []
        self.timestamps = np.array([ORIGIN])
        self.x_data = np.array([ORIGIN])
        self.y_data = np.array([ORIGIN])
        self.z_data = np.array([ORIGIN])
        self.start_time = time.time()
        self.index = 0

    def record_data(self, data: str) -> None:
        data_dictionary = {}
        for d in data.split(";"):
            if d:
                tag, value = d.split(":")
                data_dictionary[tag] = value
        data_dictionary["real_time"] = time.time() - self.start_time
        self.drone_info.append(data_dictionary)

    def process_data(self):
        for info in self.drone_info:
            delta_t = info["real_time"] - self.timestamps[self.index]
            self.timestamps = np.append(self.timestamps, float(info["real_time"]))
            self.x_data = np.append(self.x_data, self.x_data[self.index] + delta_t * float(info["vgx"]))
            self.y_data = np.append(self.y_data, self.y_data[self.index] + delta_t * float(info["vgy"]))
            self.z_data = np.append(self.z_data, self.z_data[self.index] + delta_t * float(info["vgz"]))
            self.index += 1

    def plot_data(self):
        self.ax.stem(self.x_data, self.y_data, self.z_data)
        plt.show()

    def run(self):
        drone = Tello(debug=True, has_video=False, state_callback=self.record_data)
        drone.connect()
        drone.takeoff()
        for _ in range(4):
            drone.forward(100)
            drone.cw(90)
        drone.land()
        drone.disconnect()
        self.process_data()
        self.plot_data()

if __name__ == "__main__":
    DroneSimulator().run()
