addcalibrations file=/home/d/git/phenol_photooxidation_calc/calibrations/calibrations.xml plot=True
#initial concentration of phenol 166.67 and peroxide 8117.65 μM, increased to take into account possible error
addexperiment id=dl100 path=/home/d/yandex-disk/science/6-defBN-phenol-photooxidation/photocatalysis/dl100-2 format=folder phenol=180 peroxide=8130
processexperiments verbose=True
exportresults
