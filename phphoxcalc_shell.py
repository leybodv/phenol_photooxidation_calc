#!/usr/bin/python3

# TODO: docs

import cmd
from experiment import Experiment
from plotter import Plotter

class PhPhOxCalcShell(cmd.Cmd):
    intro = 'Process data of phenol photooxidation experiment. Type help or ? to list commands.\n'
    prompt = '> '
    experiments = list() #experiment space
    calibrations = list() #calibrations space

    def do_addexperiment(self, arg):
        """
        Adds experiment results to the experiment's space.

        Parameters:
        -----------
            arg : str
                arguments provided by user in a form of key=value pairs separated by space. Allowed values:
                    sample_name=name:
                        Id of sample experiment were done with
                    raw_data_path=path:
                        Path to raw data file in a format <Wavelength>\t<absorbance@time0>\t<absorbance@time1>...
        """
        print(f'PhPhOxCalcShell().do_addexperiment(self, arg):') #LOG
        arguments = self.parse_args(arg)
        self.experiments.append(Experiment(arguments['sample_name'], arguments['raw_data_path']))

    def do_addcalibration(self, arg):
        """
        """
        print(f'PhPhOxCalcShell().do_addcalibraion(self, arg):') #LOG
        arguments = self.parse_args(arg)
        self.calibrations.append(Calibration(arguments['solute'], arguments['solvent'], ...) # TODO i'm here

    def do_plotrawdata(self, arg):
        """
        """
        if not bool(self.experiments):
            print(f'You need to add experiments first. Type help or ? to list commands.')
            return
        Plotter().plotrawdata(self.experiments)

    def do_quit(self, arg):
        """
        Quits program
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
        print(f'PhPhOxCalcShell().parse_args(arg):') #LOG
        args_dict = dict()
        args = arg.split()
        print(f'{args = }') #LOG
        for a in args:
            s = a.split('=')
            args_dict[s[0]] = s[1]
        print(f'{args_dict = }') #LOG
        return args_dict


if __name__ == '__main__':
#    print(f'{dir() = }') #LOG
    PhPhOxCalcShell().cmdloop()
