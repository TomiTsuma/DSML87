import pandas as pd
import os
import numpy as np
from DSML87.data import load_residual_outliers

# import rpy2.robjects as robjects
# r = robjects.r
# r['source']('pcc_V1.7.r')
# pcc = robjects.globalenv['pcc']
# from rpy2.robjects import pandas2ri, numpy2ri
# pandas2ri.activate()
# numpy2ri.activate()

# data = pd.read_csv('outputFiles/PCC_Classes/boron.csv', index_col=0)
# pcc(
#     "boron",
#     numpy2ri.py2rpy(np.array([0.5,0.8,1])),
#     pandas2ri.py2rpy(data),
#     1,
#     2
#     )


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

wetchem_df.to_csv("/home/tom/DSML125/DSML87/inputFiles/cleaned_wetchem.csv")


def residual_outliers(chemicals, version):
    print("Getting residual outliers")
    spectra = pd.read_csv(
        '/home/tom/DSML125/outputFiles/spectraldata.csv', index_col=0, engine='c')
    wetchem_df = pd.read_csv(
        "/home/tom/DSML125/DSML87/inputFiles/uncleaned_wetchem.csv")

    redbooth_outliers_dict, pcc_classes_dict = load_residual_outliers()

    os.makedirs('/home/tom/DSML125/DSML87/outputFiles/PCC1', exist_ok=True)
    os.makedirs('/home/tom/DSML125/DSML87/outputFiles/PCC2', exist_ok=True)
    os.makedirs('/home/tom/DSML125/DSML87/outputFiles/PCC3', exist_ok=True)
    os.makedirs('/home/tom/DSML125/DSML87/outputFiles/PCC_Classes',
                exist_ok=True)
    for chem in chemicals:
        wet = wetchem_df.loc[wetchem_df[chem].notnull()]
        df = pd.read_csv(
            f"/home/tom/DSML125/DSML87/outputFiles/preds/{version}/{chem}_preds.csv")

        df = df.rename(columns={'Unnamed: 0': 'sample_code'})
        if ('sample_code' not in df.columns):
            df = df.rename(columns={'sample_id': 'sample_code'})

        print(chem, "------------------------------>")
        print(df.loc[df['sample_code'].isin(wet['sample_code'])])
        df = pd.merge(df, wet, on='sample_code', how="inner")
        print(df, "After merge")
        df = df.loc[df[chem].notnull()]
        df = df[['sample_code', chem, '0']]
        df['Difference'] = df['0'] - df[chem]

        df.to_csv(
            f"/home/tom/DSML125/DSML87/outputFiles/PCC_Classes/{chem}.csv")
        if (chem in redbooth_outliers_dict.keys()):
            print(chem, "In Redbooth Outliers")
            lower = redbooth_outliers_dict[chem][0]
            upper = redbooth_outliers_dict[chem][1]
            print(upper)
            print(lower)
            df.loc[df['Difference'] > upper, 'PCC_Class'] = 3
            df.loc[df['Difference'] < lower, 'PCC_Class'] = 3

            df.loc[((df['Difference'] < upper) & (
                df['Difference'] > lower)), 'PCC_Class'] = 1

            df.to_csv(
                f"/home/tom/DSML125/DSML87/outputFiles/PCC_Classes/{chem}.csv")
            spectra.loc[spectra.index.isin(df.loc[(df['Difference'] > lower) | (
                df['Difference'] < upper)]['sample_code'])].to_csv(f'/home/tom/DSML125/DSML87/outputFiles/PCC1/{chem}.csv')
            spectra.loc[spectra.index.isin(df.loc[(df['Difference'] < lower) | (
                df['Difference'] > upper)]['sample_code'])].to_csv(f'/home/tom/DSML125/DSML87/outputFiles/PCC3/{chem}.csv')
        elif (chem in pcc_classes_dict.keys()):
            lower = None
            mid = None
            upper = None
            print(chem)
            lower = pcc_classes_dict[chem]['Value_1']
            mid = pcc_classes_dict[chem]['Value_2']
            upper = pcc_classes_dict[chem]['Value_3']
            if (chem in df.columns):
                print("THIS is lower", lower)
                print("THIS is the chemical column", df[chem].values)
                df.loc[df[chem] < lower, 'Actual_PCC'] = 1
                df.loc[df['0'] < lower, 'Predicted_PCC'] = 1

                df.loc[(df[chem] > lower) & (df[chem] < mid), 'Actual_PCC'] = 2
                df.loc[(df['0'] > lower) & (
                    df[chem] < mid), 'Predicted_PCC'] = 2

                df.loc[(df[chem] > mid) & (df[chem] < upper), 'Actual_PCC'] = 3
                df.loc[(df['0'] > mid) & (df[chem] < upper),
                       'Predicted_PCC'] = 3

                df.loc[df[chem] > upper, 'Actual_PCC'] = 4
                df.loc[df['0'] > upper, 'Predicted_PCC'] = 4

                df['PCC_Class'] = (df['Actual_PCC'] -
                                   df['Predicted_PCC']).abs()

                df.to_csv(
                    f"/home/tom/DSML125/DSML87/outputFiles/PCC_Classes/{chem}.csv")
                spectra.loc[spectra.index.isin(df.loc[df['PCC_Class'] <= 1]['sample_code'])].to_csv(
                    f'/home/tom/DSML125/DSML87/outputFiles/PCC1/{chem}.csv')
                spectra.loc[spectra.index.isin(df.loc[df['PCC_Class'] == 2]['sample_code'])].to_csv(
                    f'/home/tom/DSML125/DSML87/outputFiles/PCC2/{chem}.csv')
                spectra.loc[spectra.index.isin(df.loc[df['PCC_Class'] >= 3]['sample_code'])].to_csv(
                    f'/home/tom/DSML125/DSML87/outputFiles/PCC3/{chem}.csv')

        else:
            continue

    pcc_sample_codes = []
    res_df = pd.DataFrame()
    for chem in chemicals:
        print("Chemical", chem)
        classes = pd.read_csv(
            f"/home/tom/DSML125/DSML87/outputFiles/PCC_Classes/{chem}.csv")
        outliers = classes.loc[classes['PCC_Class'] > 1]
        # res_df[chem] = outliers['sample_code'].values
        outliers = outliers[['sample_code']].rename(columns={"sample_code":chem})
        # print(outliers)
        res_df = pd.concat([res_df, outliers[chem] ], axis =1 )
        # print(res_df)
        pcc_sample_codes.extend([i for i in outliers[chem]])

    print(pcc_sample_codes)
    res_df.to_csv(
        "/home/tom/DSML125/DSML87/outputFiles/residual_outliers.csv")
    spectra = spectra.loc[~(spectra.index.isin(pcc_sample_codes))]
    print(spectra.index)
    spectra.to_csv(
        "/home/tom/DSML125/DSML87/outputFiles/spc_no_residual_outliers.csv")
    wetchem = pd.read_csv(
        "/home/tom/DSML125/DSML87/inputFiles/uncleaned_wetchem.csv")
    wetchem = wetchem.set_index("sample_code")
    print(wetchem.index)
    wetchem = wetchem.loc[wetchem.index.isin(spectra.index)]
    wetchem.to_csv('/home/tom/DSML125/DSML87/inputFiles/wetchem.csv')
