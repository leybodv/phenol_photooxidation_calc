import numpy as np
from uvvisparser import UvVisParser
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
    phenol_init_conc : float
        initial concentration of phenol in μM
    peroxide_init_conc : float
        initial concentration of peroxide in μM
    """

    def __init__(self, sample_name, raw_data_path, data_format:str, phenol_init_conc:float, peroxide_init_conc:float):
        """
        assigns parameters to instance variables and parses experimental data

        parameters
        ----------
        sample_name : str
            photocatalyst sample's id
        raw_data_path : str or Path
            path to file or folder with experimental data
        data_format : str
            format of experimental data. If 'file', data must be in a single file; if 'folder', data must be in separate files in a folder
        phenol_init_conc : float
            initial concentration of phenol in μM
        peroxide_init_conc : float
            initial concentration of peroxide in μM
        """
        self.sample_name = sample_name
        self.raw_data_path = raw_data_path
        self.phenol_init_conc = float(phenol_init_conc)
        self.peroxide_init_conc = float(peroxide_init_conc)
        if data_format == 'file':
            self.data_points = self.parse_uv_vis(raw_data_path)
        elif data_format == 'folder':
            self.data_points = UvVisParser().parse_experimental_from_folder(raw_data_path)
        else:
            print(f'Cannot recognize experimental data of format {data_format}')
            return

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

    def get_phenol_init_concentration(self) -> float:
        """
        getter to obtain initial concentration of phenol in μM

        returns
        -------
        phenol_init_conc : float
            initial concentration of phenol in μM
        """
        return self.phenol_init_conc

    def get_peroxide_init_concentration(self) -> float:
        """
        getter to obtain initial concentration of peroxide in μM

        returns
        -------
        peroxide_init_conc : float
            initial concentration of peroxide in μM
        """
        return self.peroxide_init_conc
