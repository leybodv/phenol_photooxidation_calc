# phenol_photooxidation_calc
Command line program to process experimental data of phenol photooxidation experiment using multicomponent approach described in \[doi: 10.1016/S1386-1425(02)00172-5\] and \[doi: 10.1080/09593331708616383\]. To run program start `phphoxcalc_shell.py`. The program executes commands entered by user. Also there is an option to process commands from file line-by-line ignoring lines which start with '#' symbol.\
\
List of available commands (can be listed inside program by typing 'help' or '?'):\
\
`addexperiment id=<id> path=<path> format=<format> phenol=<phenol concentration> peroxide=<peroxide concentration>`\
&emsp;adds experiment results which are uv-vis spectra obtained from samples collected at different time from the beginning of experiment\
&emsp;&emsp;`<id>`: id of experiment, usually photocatalyst sample's id\
&emsp;&emsp;`<path>`: path to file with experimental data in a format \<wavelength\>\<tab\>\<absorbance@time0\>\<tab\>\<absorbance@time1\>... with single header row in a format \<some-text\>\<tab\>\<time0\>\<tab\>\<time1\>...\
&emsp;&emsp;`<format>`: file|folder, if 'file', program expects experimental data in a single file in a format \<wavelength\>\<tab\>\<absorbance@time0\>\<tab\>\<absorbance@time1\>... with single header row in a format \<some-text\>\<tab\>\<time0\>\<tab\>\<time1\>... if 'folder', program expects experimental data in several files in a format \<wavelength\>\<tab\>\<absorbance\> with single header row and it will ask user for time from the beginning of experiment for each imported file\
&emsp;&emsp;`<phenol concentration>`: initial concentration of phenol in μM\
&emsp;&emsp;`<peroxide concentration>`: initial concentration of peroxide in μM\
\
`addcalibration solute=<solute> solvent=<solvent> path=<path>`\
&emsp;adds uv-vis spectra for absorbance vs. concentration calibration\
&emsp;&emsp;`<solute>`: compound's name which was used for calibration\
&emsp;&emsp;`<solvent>`: solvent used for calibration\
&emsp;&emsp;`<path>`: path to folder with calibration data in a format \<wavelength\>\<tab\>\<absorbance\> with single header row\
\
`processexperiments verbose=<verbosity>`\
&emsp;finds concentrations of phenol oxidation products vs. time based on experimental and calibration data\
&emsp;&emsp;`<verbosity>`: True|False, if True, plots of fitting experimental spectra by reference spectra will be shown\
\
`execute path=<path>`\
&emsp;executes commands in file line-by-line ignoring lines started with '#'\
&emsp;&emsp;`<path>`: path to file with commands\
\
`quit`\
&emsp;quits program\

# TODO
- move experiment.parse_uv_vis method to UvVisParser
- ask user to add calibrations for benzoquinone, catechol, formic acid, hydroquinone, h2o2 and phenol automatically and choose predefined reference spectra to fit experimental data
- add time to the title of plots with fitting of experimental spectrum with references
