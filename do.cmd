#initial concentration of phenol 200 and peroxide 48706 μM, increased to take into account possible error
addexperiment id=dl100 path=/home/d/yandex-disk/science/6-defBN-phenol-photooxidation/photocatalysis/dl100-1 format=folder phenol=210 peroxide=48710
addcalibration solute=benzoquinone solvent=water path=/home/d/git/phenol_photooxidation_calc/calibrations/benzoquinone
addcalibration solute=catechol solvent=water path=/home/d/git/phenol_photooxidation_calc/calibrations/catechol
addcalibration solute=formic-acid solvent=water path=/home/d/git/phenol_photooxidation_calc/calibrations/formic-acid
addcalibration solute=h2o2 solvent=water path=/home/d/git/phenol_photooxidation_calc/calibrations/h2o2
addcalibration solute=hydroquinone solvent=water path=/home/d/git/phenol_photooxidation_calc/calibrations/hydroquinone
addcalibration solute=phenol solvent=water path=/home/d/git/phenol_photooxidation_calc/calibrations/phenol
processexperiments verbose=True
