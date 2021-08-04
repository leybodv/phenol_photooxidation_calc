# TODO: docs

import numpy as np
from datapoint import DataPoint

class Experiment():
    """
    """

    def __init__(self, sample_name, raw_data_path):
        self.sample_name = sample_name
        self.raw_data_path = raw_data_path
        self.data_points = self.parse_uv_vis(raw_data_path)
        print(f'Experiment().__init__(self, sample_name, raw_data_path):') #LOG
        print(f'{self.sample_name = }') #LOG
        print(f'{self.raw_data_path = }') #LOG

    def parse_uv_vis(self, raw_data_path):
        """
        """
        print(f'Experiment().parse_uv_vis(self, raw_data_path):') #LOG
        header = np.loadtxt(fname=raw_data_path, delimiter='\t', dtype='str', encoding='utf-8', max_rows=1, unpack=True)
        print(f'{header = }') #LOG
        data = np.loadtxt(fname=raw_data_path, delimiter='\t', skiprows=1, unpack=True, encoding='utf-8')
        print(f'{data = }') #LOG
        data_points = list()
        for i in range(len(data)):
            if i != 0:
                data_points.append(DataPoint(time=header[i], wavelength=data[0], absorbance=data[i]))
        print(f'{data_points = }') #LOG
        return data_points
