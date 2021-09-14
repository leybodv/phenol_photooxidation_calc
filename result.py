from experiment import Experiment
from resultpoint import ResultPoint
from datapoint import DataPoint
from calibration import Calibration
import numpy as np

class Result():
    """
    class represents result of experimental data processing with information about photocatalyst sample's name and result points

    instance variables
    ------------------
    sample_name : str
        photocatalyst sample's id
    result_points : list[ResultPoint]
        result points with reference spectra, fitting coefficients and concentrations
    """

    def __init__(self, experiment:Experiment, calibrations:list, verbose=False):
        """
        assigns parameters to instance variables, calculates results

        parameters
        ----------
        experiment : Experiment
            experiment data for single photocatalyst sample
        calibrations : list[Calibration]
            calibration data
        verbose : bool (default: False)
            if True, fitting experimental spectrum with reference spectra plots will be shown
        """
        self.sample_name = experiment.sample_name
        self.result_points = self.calculate_results(raw_data_points=experiment.data_points, calibrations=calibrations, phenol_init_conc=experiment.get_phenol_init_concentration(), peroxide_init_conc=experiment.get_peroxide_init_concentration(), verbose=verbose)

    def calculate_results(self, raw_data_points:list[DataPoint], calibrations:list[Calibration], phenol_init_conc:float, peroxide_init_conc:float, verbose:bool):
        """
        creates list of ResultPoint objects with experimental data processing results

        parameters
        ----------
        raw_data_points : list[DataPoint]
            list of data points with experimental results
        calibrations : list[Calibration]
            list of calibration data
        phenol_init_conc : float
            initial concentration of phenol solution in μM
        peroxide_init_conc : float
            initial concentration of peroxide solution in μM
        verbose : bool
            if True, fitting experimental spectrum with reference spectra plots will be shown

        returns
        -------
        result_points : list[ResultPoint]
            list of ResultPoint objects with experimental data processing results
        """
        from plotter import Plotter
        result_points = list()
        calibration_wavelengths = list()
        calibration_coefficients = list()
        for calibration in calibrations:
            calibration_wavelengths.append(calibration.get_calibration_wavelength())
            calibration_coefficients.append(calibration.get_calibration_coefficient())
        calibration_wavelengths = np.array(calibration_wavelengths)
        calibration_coefficients = np.array(calibration_coefficients)
        reference_spectra, reference_names = self.find_out_spectra(calibrations)
        for point in raw_data_points:
            resultpoint = ResultPoint(experimental_point=point, reference_spectra=reference_spectra, reference_names=reference_names, calibration_coefficients=calibration_coefficients, calibration_wavelengths=calibration_wavelengths, phenol_init_conc=phenol_init_conc, peroxide_init_conc=peroxide_init_conc)
            result_points.append(resultpoint)
            if verbose:
                Plotter().plot_result_point(point, resultpoint)
        return result_points

    def get_name(self) -> str:
        """
        getter to obtain photocatalyst sample's id

        returns
        -------
        id : str
            photocatalyst sample's id
        """
        return self.sample_name

    def get_points(self) -> list:
        """
        getter to obtain result points

        returns
        -------
        result_points : list[ResultPoint]
            objects with experimental data processing results
        """
        return self.result_points

    def find_out_spectra(self, calibrations:list[Calibration]) -> tuple:
        """
        ask user which spectrum from calibration data for compound to use for fitting experimental data

        parameters
        ----------
        calibrations : list[Calibration]
            calibration data

        returns
        -------
        reference_spectra : list[Spectrum]
            list of reference spectra to be used for experimental data fitting
        reference_names : list[str]
            list of reference compounds names
        """
        from plotter import Plotter
        reference_spectra = list()
        reference_names = list()
        get_from_user = False
        for calibration in calibrations:
            if get_from_user:
                break
            for calibration_point in calibration.get_points():
                if calibration_point.is_reference() is None:
                    get_from_user = True
                    break
                if calibration_point.is_reference():
                    reference_spectra.append(calibration_point.get_spectrum())
                    reference_names.append(calibration.get_solute())
        for calibration in calibrations:
            if not get_from_user:
                break
            Plotter().plot_raw_calibration(calibration.calibration_points, calibration.get_solute())
            concentration = input(f'which spectrum to use for fitting data for {calibration.get_solute()} compound? enter concentration: ')
            concentration = float(concentration)
            reference_spectra.append(calibration.get_spectrum_by_concentration(concentration))
            reference_names.append(calibration.get_solute())
        return (reference_spectra, reference_names)
