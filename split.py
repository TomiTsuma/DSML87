import pandas as pd
import os
import notebook
from pathlib import Path
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
import subprocess


def split_data():
    averaged_spectra = pd.read_csv(
        "/home/tom/DSML125/DSML87/outputFiles/spc.csv", engine="c")
    for col in averaged_spectra.columns:
        if ('Unnamed' in col):
            averaged_spectra = averaged_spectra.drop(col, axis=1)
    averaged_spectra.to_csv("/home/tom/DSML125/DSML87/outputFiles/spc.csv")

    r = robjects.r
    r['source']('/home/tom/DSML125/DSML87/splits.r')
    split = robjects.globalenv['split']
    try:
        os.makedirs("/home/tom/DSML125/DSML87/outputFiles/splits",
                    exist_ok=True)
        os.makedirs("/home/tom/DSML125/DSML87/outputFiles/rds", exist_ok=True)
    except Exception as e:
        print(e)

    pandas2ri.activate()

    split("/home/tom/DSML125/DSML87/outputFiles/spc.csv",
          "/home/tom/DSML125/DSML87/outputFiles/rds", "/home/tom/DSML125/DSML87/outputFiles/splits")
