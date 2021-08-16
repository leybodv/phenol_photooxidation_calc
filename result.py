# TODO: docs

from experiment import Experiment

class Result():

    def __init__(self, experiment:Experiment, calibrations:list):
        """
        """
        print(f'Result().__init__(self, experiment, calibrations)') #LOG
        self.sample_name = experiment.sample_name
        self.result_points = self.calculate_results(experiment.data_points, calibrations)

    def calculate_results(self, raw_data_points:list, calibrations:list):
        """
        """
        print(f'Result().calculate_results(self, raw_data_points, calibrations)') #LOG
        result_points = list()
        for point in raw_data_points:
            result_points.append(ResultPoint(point, calibrations))
        return result_points
