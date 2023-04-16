#!/bin/bash
# Run these commands in a bash terminal (Supply the Access credentials and github username first)
# pip install dvc --user
# pip install "dvc[s3]" --user
DO_AWS_ACCESS_KEY_ID=DO00JVCF7VU9NR8R9KUC
DO_AWS_ACCESS_KEY=qw7fwzXbo90pYNVgybQbodide616IklbcR21y6G8EOI   

# cd D://CropNutsDocuments/MSSC_DVC
python -m dvc init
python -m dvc remote add --default storage s3://spectral-models -f
python -m dvc remote modify storage endpointurl https://ams3.digitaloceanspaces.com


export AWS_ACCESS_KEY_ID=${DO_AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${DO_AWS_ACCESS_KEY}

python -m dvc add spc.csv
python -m dvc push spc.csv



