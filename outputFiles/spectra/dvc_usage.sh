
DO_AWS_ACCESS_KEY_ID=DO00JVCF7VU9NR8R9KUC
DO_AWS_ACCESS_KEY=qw7fwzXbo90pYNVgybQbodide616IklbcR21y6G8EOI 


export AWS_ACCESS_KEY_ID=${DO_AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${DO_AWS_ACCESS_KEY}
# Clone the repositroy containing dvc files
# git clone https://github.com/${DO_GITHUB_USERNAME}/MSSC_DVC_V2.git MSSC_DVC

# Install the dvc python package and the S3 dependencies
sudo wget \
       https://dvc.org/deb/dvc.list \
       -O /etc/apt/sources.list.d/dvc.list
wget -qO - https://dvc.org/deb/iterative.asc | gpg --dearmor > packages.iterative.gpg
sudo install -o root -g root -m 644 packages.iterative.gpg /etc/apt/trusted.gpg.d/
rm -f packages.iterative.gpg
sudo apt update
sudo apt install dvc


# pull files
# cd MSSC_DVC
dvc pull spc.csv
