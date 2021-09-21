addcalibrations file=/home/d/git/phenol_photooxidation_calc/calibrations/calibrations.xml plot=False
#initial concentration of phenol 166.67 and peroxide 8117.65 μM, increased to take into account possible error
addexperiment id=dl102 path=/home/d/yandex-disk/science/6-defBN-phenol-photooxidation/photocatalysis/dl102-1 format=folder phenol=180 peroxide=8130
processexperiments verbose=True
exportresults
