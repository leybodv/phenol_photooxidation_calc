import numpy as np
from pathlib import Path
from datapoint import DataPoint
from io import StringIO

class UvVisParser():
    """
    utility class for parsing uv-vis data
    """

    def parse_calibration_from_file(self, file):
        """
        ask user for concentration used for calibration and parse corresponding uv-vis spectrum

        parameters
        ----------
        file : str or Path
            file with calibration spectrum data

        returns
        -------
        concentration : float
            concentration used for calibration
        wavelength : numpy.ndarray[float]
            array of wavelengths parsed from file
        absorbance : numpy.ndarray[float]
            array of absorbances parsed from file
        """
        concentration = input(f'Importing file {file}. Enter concentration of solute [μM]: ')
        concentration = float(concentration)
        wavelength, absorbance = self.parse_uvvis(file)
        return (concentration, wavelength, absorbance)

    def parse_experimental_from_file(self, file:str) -> list[DataPoint]:
        """
        parses uv-vis data. file must be in a format <wavelength><tab><absorbance@time0><tab><absorbance@time1>... file also must contain single row header in a format <some-text><tab><time0><tab><time1>...

        parameters
        ----------
        file : str or Path
            path to file with experimental data

        returns
        -------
        data_points : list[DataPoint]
            experimental data points with time and spectrum information
        """
        header = np.loadtxt(fname=file, delimiter='\t', dtype='str', encoding='utf-8', max_rows=1, unpack=True)
        data = np.loadtxt(fname=file, delimiter='\t', skiprows=1, unpack=True, encoding='utf-8')
        data_points = list()
        for i in range(len(data)):
            if i != 0:
                # absorbance = data[i]
                # if np.any(data[i] < 0):
                #     absorbance = data[i] + abs(data[i].min())
                absorbance = data[i] - data[i].min()
                data_points.append(DataPoint(time=header[i], wavelength=data[0], absorbance=absorbance))
        data_points.sort(key=lambda point: point.get_time())
        return data_points

    def parse_experimental_from_folder(self, folder:str) -> list[DataPoint]:
        """
        import experimental data from folder with files containing data in a format <wavelength><tab><absorbance>. ask user about time of experiment for each file

        parameters
        ----------
        folder : str
            folder with files with experimental uv-vis spectra

        returns
        -------
        datapoints : list[DataPoint]
            list of data points with experimental data
        """
        data_points = list()
        for file in Path(folder).iterdir():
            if file.is_file():
                time = input(f'Importing file {file}. Enter time of experimental point: ')
                time = float(time)
                wavelength, absorbance = self.parse_uvvis(file)
                data_points.append(DataPoint(time, wavelength, absorbance))
        data_points.sort(key=lambda point: point.get_time())
        return data_points

    def parse_uvvis(self, file:Path) -> tuple:
        """
        parse file with uv-vis spectrum in a format <wavelength><tab><absorbance>. raise spectrum to zero if there are negative absorbance values

        parameters
        ----------
        file : Path
            path to file with uv-vis spectrum

        returns
        -------
        wavelength : numpy.ndarray
            array of wavelengths of uv-vis spectrum
        absorbance : numpy.ndarray
            array of absorbances of uv-vis spectrum
        """
        with file.open(mode='r') as f:
            contents = f.read()
            contents = contents.replace(',', '.')
        if contents.split(sep='\n')[0].split(sep='\t')[0].isdigit():
            skiprows = 0
        else:
            skiprows = 1
        wavelength, absorbance = np.loadtxt(fname = StringIO(contents), delimiter='\t', unpack=True, encoding='utf-8', skiprows=skiprows)
        absorbance = absorbance - absorbance.min()
        # if np.any(absorbance < 0):
        #     absorbance = absorbance + abs(absorbance.min())
        return (wavelength, absorbance)
