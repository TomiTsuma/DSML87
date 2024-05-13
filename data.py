import pandas as pd
import numpy as np


def get_spc():
    spc = pd.read_csv(
        '/home/tom/19_8_2022_global_spectra_datav2dot2_with_rw.csv', index_col=0, engine='c')
    uncleaned_wetchem_df = pd.read_csv(
        "/home/tom/DSML125/DSML87/inputFiles/cleaned_wetchem.csv")
    uncleaned_wetchem_df = uncleaned_wetchem_df.rename(
        columns={"Unnamed: 0": "sample_code"})

    spc = spc.loc[spc.index.isin(uncleaned_wetchem_df['sample_code'])]
    spc.to_csv('outputFiles/spectra.csv')


def load_residual_outliers():
    redbooth_outliers = {'boron': [-5, 5], 'phosphorus': [-250, 450], 'zinc': [-25, 100], 'sulphur': [-100, 400], 'sodium': [-1000, 2500],
                         'magnesium': [-500, 1000], 'potassium': [-800, 1600], 'calcium': [-5000, 5000], 'copper': [-100, 300], 'ec_salts': [-1000, 2000], 'organic_carbon': [-2, 2]}
    redbooth_properties = [i for i in redbooth_outliers.keys()]

    pcc_classes_dict = pd.read_csv(
        "/home/tom/DSML125/DSML87/element_managemet_thresholds.csv", index_col=0).T.to_dict()
    pcc_elements = [i for i in pcc_classes_dict.keys()
                    if i not in redbooth_properties]
    pcc_classes_dict = {key: pcc_classes_dict[key]
                        for key in pcc_classes_dict.keys() if key in pcc_elements}

    all_chemicals = ['aluminium',
                     'phosphorus', 'ph', 'exchangeable_acidity', 'calcium', 'magnesium',
                     'sulphur', 'sodium', 'iron', 'manganese', 'boron', 'copper', 'zinc', 'total_nitrogen', 'potassium',
                     'ec_salts', 'organic_carbon', 'cec', 'sand', 'silt', 'clay']

    undefined_chems = [i for i in all_chemicals if (
        i not in pcc_elements and i not in redbooth_properties)]

    uncleaned_wetchem_df = pd.read_csv(
        "/home/tom/DSML125/inputFiles/uncleaned_wetchem.csv")

    uncleaned_wetchem_df = uncleaned_wetchem_df.rename(
        columns={"Unnamed: 0": "sample_code"})
    uncleaned_wetchem_df.set_index("sample_code")
    for column in uncleaned_wetchem_df.columns:
        if (column != 'sample_code'):
            vals = []
            for value in uncleaned_wetchem_df[column].values:
                if (value is not None):
                    value = str(value)
                    value = value.replace(">", "").replace(
                        "<", "").replace("...", "").strip()
                    value = float(value)
                vals.append(value)
            uncleaned_wetchem_df[column] = vals
    wetchem_df = uncleaned_wetchem_df.copy(deep=True)
    wetchem_df.set_index("sample_code")

    quartiles_dict = {}
    for chem in undefined_chems:
        if (chem not in uncleaned_wetchem_df.columns):
            continue
        quartiles_dict[chem] = {}
        upper_quartile = wetchem_df[chem].quantile(0.75)
        median = wetchem_df[chem].quantile(0.50)
        lower_quartile = wetchem_df[chem].quantile(0.25)
        quartiles_dict[chem]['Value_1'] = lower_quartile
        quartiles_dict[chem]['Value_2'] = median
        quartiles_dict[chem]['Value_3'] = upper_quartile

    pcc_dict = {**pcc_classes_dict, **quartiles_dict}
    pd.DataFrame(pcc_dict).T.to_csv('/home/tom/DSML125/DSML87/outputFiles/pcc_sumnmnary_statistics.csv')

    return redbooth_outliers, pcc_dict


