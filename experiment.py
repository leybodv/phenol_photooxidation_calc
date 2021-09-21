import numpy as np
from pathlib import Path
from uvvisparser import UvVisParser
from datapoint import DataPoint

class Experiment():
    """
    class represents single experiment of phenol photooxidation with information about studied photocatalyst's id, path to experimental data files and all uv-vis spectra obtained at different times of experiment

    instance variables
    ------------------
    sample_name : str
        photocatalyst sample's id
    raw_data_path : Path
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
        self.raw_data_path = Path(raw_data_path)
        self.phenol_init_conc = float(phenol_init_conc)
        self.peroxide_init_conc = float(peroxide_init_conc)
        if data_format == 'file':
            self.data_points = UvVisParser().parse_experimental_from_file(raw_data_path)
        elif data_format == 'folder':
            self.data_points = UvVisParser().parse_experimental_from_folder(raw_data_path)
        else:
            print(f'Cannot recognize experimental data of format {data_format}')
            return

    def get_raw_data_path(self) -> Path:
        """
        getter to obtain raw data path value

        returns
        -------
        raw_data_path : Path
            path to raw data folder|file
        """
        return self.raw_data_path

    def get_sample_name(self) -> str:
        """
        getter to obtain sample's name

        returns
        -------
        sample_name : str
            photocatalyst sample's id
        """
        return self.sample_name

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
