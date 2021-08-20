# phenol_photooxidation_calc
command line program to process experimental data of phenol photooxidation experiment using multicomponent approach described in \[doi: 10.1016/S1386-1425(02)00172-5\] and \[doi: 10.1080/09593331708616383\].

to run program start phphoxcalc_shell.py. the programs executes commands entered by user. also there is an option to process commands from file line-by-line ignoring lines which start with '#' symbol

list of available commands (can be listed inside program by typing 'help' or '?'):

addexperiment id=\<id\> path=\<path\>
        adds experiment results which is uv-vis spectra obtained from samples collected at different time from the beginning of experiment
        \<id\>: id of experiment, usually photocatalyst sample's id
        \<path\>: path to file with experimental data in a format \<wavelength\>\<tab\>\<absorbance@time0\>\<tab\>\<absorbance@time1\>... with single header row in a format \<some-text\>\<tab\>\<time0\>\<tab\>\<time1\>...

addcalibration solute=\<solute\> solvent=\<solvent\> path=\<path\>
        adds uv-vis spectra for absorbance vs. concentration calibration
        \<solute\>: compound's name which was used for calibration
        \<solvent\>: solvent used for calibration
        \<path\>: path to folder with calibration data in a format \<wavelength\>\<tab\>\<absorbance\> with single header row

processexperiments verbose=\<verbosity\>
        finds concentrations of phenol oxidation products vs. time based on experimental and calibration data
        \<verbosity\>: True|False, if True, plots of fitting experimental spectra by reference spectra will be shown

plotrawdata
        plots experimental uv-vis spectra added by addexperiment command

execute path=\<path\>
        executes commands in file line-by-line ignoring lines started with '#'
        \<path\>: path to file with commands

quit
        quits program
