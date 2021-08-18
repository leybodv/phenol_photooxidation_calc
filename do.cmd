addcalibration solute=benzoquinone solvent=water folder=/home/d/git/phenol_photooxidation_calc/calibrations/benzoquinone
addcalibration solute=catechol solvent=water folder=/home/d/git/phenol_photooxidation_calc/calibrations/catechol
addcalibration solute=formic-acid solvent=water folder=/home/d/git/phenol_photooxidation_calc/calibrations/formic-acid
addcalibration solute=hydroquinone solvent=water folder=/home/d/git/phenol_photooxidation_calc/calibrations/hydroquinone
addcalibration solute=phenol solvent=water folder=/home/d/git/phenol_photooxidation_calc/calibrations/phenol
addexperiment sample_name=dl100 raw_data_path=/home/d/git/phenol_photooxidation_calc/test/dl100_uv-vis_phenol.dat
plotrawdata
processexperiments verbose=True
