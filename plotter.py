# TODO: docs

import math
import matplotlib.pyplot as plt

class Plotter():

    def plotrawdata(experiments):
        """
        """
        print(f'Plotter().plotrawdata(experiments):') #LOG
        cols = math.ceil(math.sqrt(len(experiments)))
        rows = math.ceil(len(experiments) / cols)
        fig, axs = plt.subplots(nrows=rows, ncols=cols)
        print(f'{axs = }') #LOG
