#!/usr/bin/python3

import cmd
import xml.etree.ElementTree as ET
from experiment import Experiment
from plotter import Plotter
from calibration import Calibration
from result import Result

class PhPhOxCalcShell(cmd.Cmd):
    """
    class is a cmd.Cmd subclass which starts shell and performs all procedures for adding and processing of experimental and calibration data

    class variables
    ---------------
    intro : str
        string that printed first at the begining of the execution
    prompt : str
        prompt which appears at each line when user's input required
    experiments : list[Experiment]
        list of experiments added by the user
    calibrations : list[Calibration]
        list of calibrations added by the user
    results : list[Result]
        list of result obtained by processing of experimental data
    """
    intro = 'Process data of phenol photooxidation experiment. Type help or ? to list commands.\n'
    prompt = '> '
    experiments = list() #experiment space
    calibrations = list() #calibrations space
    results = list()

    def do_addexperiment(self, arg):
        """
        Adds experiment results to the experiment's space.

        Parameters:
        -----------
            arg : str
                arguments provided by user in a form of key=value pairs separated by space. Allowed values:
                    id=id:
                        Id of sample experiment were done with
                    path=path:
                        Path to raw data
                    format=file|folder
                        Format of data. If 'file' program expects single file with data in a format <Wavelength><tab><absorbance@time0><tab><absorbance@time1>... If 'folder' program expects folder with files with data in a format <wavelength><tab><absorbance>. Time of sample collection from the beginning of the experiment is asked from the user.
                    phenol=conc
                        Initial concentration of phenol in μM
                    peroxide=conc
                        Initial concentration of peroxide in μM
        """
        arguments = self.parse_args(arg)
        self.experiments.append(Experiment(sample_name=arguments['id'], raw_data_path=arguments['path'], data_format=arguments['format'], phenol_init_conc=arguments['phenol'], peroxide_init_conc=arguments['peroxide']))
        Plotter().plot_experiments(self.experiments)

    def do_addcalibration(self, arg):
        """
        adds calibration data to program

        parameters
        ----------
        arg : str
            arguments provided by user in a form of key=value pairs separated by space. allowed values:
                solute=solute
                    name of compound used for calibration
                solvent=solvent
                    name of solvent used for calibration
                path=path
                    path to folder with calibration files in a format <wavelength><tab><absorbance> with single header row
        """
        arguments = self.parse_args(arg)
        self.calibrations.append(Calibration(solute=arguments['solute'], solvent=arguments['solvent'], folder=arguments['path']))

    def do_addcalibrations(self, arg):
        """
        """
        arguments = self.parse_args(arg)
        tree = ET.parse(arguments['file'])
        root = tree.getroot()

    def do_processexperiments(self, arg):
        """
        find concentration of phenol oxidation products vs. time and plot results

        parameters
        ----------
        arg : str
            arguments provided by user in a form of key=value pairs separated by space. allowed values:
                verbose=(True|False)
                    if True plots of fitting experimental spectra by reference spectra will be shown
        """
        arguments = self.parse_args(arg)
        for experiment in self.experiments:
            self.results.append(Result(experiment, self.calibrations, verbose=(arguments["verbose"] == "True")))
        Plotter().plot_results(self.results)

    def do_execute(self, arg):
        """
        executes command in file line-by-line

        parameters
        ----------
        arg : str
            arguments provided by user in a form of key=value pairs separated by space. allowed values:
                path=path
                    path to file with valid commands to be executed line-by-line by the program. lines started with # will be ignored
        """
        with open(arg) as f:
            for line in f:
                if not line.startswith('#'):
                    self.cmdqueue.append(line)

    def do_quit(self, arg):
        """
        Quits program

        parameters
        ----------
        arg : str
            not used
        """
        print('bye')
        return True

    def parse_args(self, arg):
        """
        Parse args in the from 'key1=value1[ key2=value2]' and return corresponding dictionary

        Parameters:
        -----------
            arg : str
                arguments as key=value pairs separated by space

        Returns:
        --------
            args_dict : dict
                dictionary of arguments
        """
        args_dict = dict()
        args = arg.split()
        for a in args:
            s = a.split('=')
            args_dict[s[0]] = s[1]
        return args_dict

# start program execution
if __name__ == '__main__':
    PhPhOxCalcShell().cmdloop()
