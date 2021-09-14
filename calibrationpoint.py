from spectrum import Spectrum
import numpy as np

class CalibrationPoint():
    """
    class represents single calibration point which includes information about concentration, used for calibration and uv-vis spectrum obtained

    instance variables
    ------------------
    concentration : float
        concentration of solute used for calibration
    spectrum : Spectrum
        uv-vis spectrum of this calibration point
    isreference : bool or None
        if True, spectrum will be used for experimental spectrum fitting, if None, program will ask whether to use this point for fitting later
    """

    def __init__(self, concentration, wavelength, absorbance, isreference=None):
        """
        assigns parameters to instance variables

        parameters
        ----------
        concentration : float
            concentration of solute used for calibration
        wavelength : numpy.ndarray[float] or list[float]
            array of wavelengths of calibration uv-vis spectrum
        absorbance : numpy.ndarrat[float] or list[float]
            array of absorbances of calibration uv-vis spectrum
        isreference : bool (default:None)
            if True, spectrum will be used for experimental spectrum fitting, if None, program will ask whether to use this point for fitting later
        """
        self.concentration = concentration
        self.spectrum = Spectrum(wavelength=wavelength, absorbance=absorbance)
        self.isreference = isreference

    def get_absorbance_at(self, wavelength):
        """
        returns value of absorbance at specified wavelength. Invokes Spectrum.get_absorbance_at(wavelength) method

        parameters
        ----------
        wavelength : float
            wavelength to get absorbance value at

        returns
        -------
        absorbance : float
            absorbance at specified wavelength
        """
        absorbance = self.spectrum.get_absorbance_at(wavelength)
        return absorbance

    def get_wavelength(self) -> np.ndarray:
        """
        getter to obtain array of wavelengths of calibration spectrum

        returns
        -------
        wavelengths : numpy.ndarray
            wavelengths of calibration spectrum
        """
        return self.spectrum.get_wavelength()

    def get_absorbance(self) -> np.ndarray:
        """
        getter to obtain array of absorbances of calibration spectrum

        returns
        -------
        absorbances : numpy.ndarray
            absorbances of calibration spectrum
        """
        return self.spectrum.get_absorbance()

    def get_concentration(self) -> float:
        """
        getter to obtain concentration used for calibration

        returns
        -------
        concentration : float
            concentration used for calibration
        """
        return self.concentration

    def get_spectrum(self) -> Spectrum:
        """
        getter to get calibration spectrum

        returns
        -------
        spectrum : Spectrum
            calibration spectrum
        """
        return self.spectrum
