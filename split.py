import pandas as pd
import os
import notebook
from pathlib import Path
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri


averaged_spectra = pd.read_csv("inputFiles/spectraldata.csv", engine="c")
for col in averaged_spectra.columns:
    if ('Unnamed' in col):
        averaged_spectra = averaged_spectra.drop(col, axis=1)
averaged_spectra.to_csv("inputFiles/spectraldata.csv")

r = robjects.r
r['source']('splits.R')
split = robjects.globalenv['split']

try:
    os.mkdir("./outputFiles/splits")
    os.mkdir("./outputFiles/rds")
except:
    print()


pandas2ri.activate()

split("D://CropNutsDocuments/DS-ML87/inputFiles/spectraldata.csv",
      "D://CropNutsDocuments/DS-ML87/outputFiles/rds", "D://CropNutsDocuments/DS-ML87/outputFiles/splits")
