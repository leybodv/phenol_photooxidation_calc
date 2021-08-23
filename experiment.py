import numpy as np
from datapoint import DataPoint

class Experiment():
    """
    class represents single experiment of phenol photooxidation with information about studied photocatalyst's id, path to experimental data files and all uv-vis spectra obtained at different times of experiment

    instance variables
    ------------------
    sample_name : str
        photocatalyst sample's id
    raw_data_path : str
        path to file with uv-vis spectra
    data_points : list[DataPoint]
        collection of data points with uv-vis spectra and times
    """

    def __init__(self, sample_name, raw_data_path):
        """
        assigns parameters to instance variables and parses experimental data

        parameters
        ----------
        sample_name : str
            photocatalyst sample's id
        raw_data_path : str or Path
            path to file with experimental data
        """
        self.sample_name = sample_name
        self.raw_data_path = raw_data_path
        self.data_points = self.parse_uv_vis(raw_data_path)

    def parse_uv_vis(self, raw_data_path):
        """
        parses uv-vis data. file must be in a format <wavelength><tab><absorbance@time0><tab><absorbance@time1>... file also must contain single row header in a format <some-text><tab><time0><tab><time1>...

        parameters
        ----------
        raw_data_path : str or Path
            path to file with experimental data

        returns
        -------
        data_points : list[DataPoint]
            experimental data points with time and spectrum information
        """
        header = np.loadtxt(fname=raw_data_path, delimiter='\t', dtype='str', encoding='utf-8', max_rows=1, unpack=True)
        data = np.loadtxt(fname=raw_data_path, delimiter='\t', skiprows=1, unpack=True, encoding='utf-8')
        data_points = list()
        for i in range(len(data)):
            if i != 0:
                absorbance = data[i]
                if np.any(data[i] < 0):
                    absorbance = data[i] + abs(data[i].min())
                data_points.append(DataPoint(time=header[i], wavelength=data[0], absorbance=absorbance))
        return data_points
