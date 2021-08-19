# TODO: docs

from experiment import Experiment
from resultpoint import ResultPoint
#from plotter import Plotter

class Result():

    def __init__(self, experiment:Experiment, calibrations:list, verbose=False):
        """
        """
        print(f'Result().__init__(self, experiment, calibrations)') #LOG
        self.sample_name = experiment.sample_name
        self.result_points = self.calculate_results(experiment.data_points, calibrations, verbose)

    def calculate_results(self, raw_data_points:list, calibrations:list, verbose:bool):
        """
        """
        print(f'Result().calculate_results(self, raw_data_points, calibrations)') #LOG
        from plotter import Plotter
        result_points = list()
        for point in raw_data_points:
            resultpoint = ResultPoint(point, calibrations)
            result_points.append(resultpoint)
            if verbose:
                Plotter().plot_result_point(point, resultpoint)
        return result_points

    def get_name(self) -> str:
        """
        """
        print(f'Result().get_name(self):') #LOG
        return self.sample_name

    def get_points(self) -> list:
        """
        """
        print(f'Result().get_points(self):') #LOG
        return self.result_points
