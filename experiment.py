class Experiment():

    def __init__(self, sample_name, raw_data_path):
        self.sample_name = sample_name
        self.raw_data_path = raw_data_path
        self.data_points = self.parse_uv_vis(raw_data_path)
        print(f'Experiment().__init(self, sample_name, raw_data_path):') #LOG
        print(f'{self.sample_name = }') #LOG
        print(f'{self.raw_data_path = }') #LOG

    def parse_uv_vis(self, raw_data_path):
        print(f'Experiment().parse_uv_vis(self, raw_data_path):') #LOG
        return None
