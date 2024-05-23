#!/bin/bash
#SBATCH --ntasks=1                # Number of tasks (see below)
#SBATCH --cpus-per-task=1         # Number of CPU cores per task
#SBATCH --nodes=1                 # Ensure that all cores are on one machine
#SBATCH --time=0-00:05            # Runtime in D-HH:MM
#SBATCH --partition=gpu-2080ti-dev # Partition to submit to
#SBATCH --gres=gpu:1              # optionally type and number of gpus
#SBATCH --mem=50G                 # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH --output=logs/job_%j.out  # File to which STDOUT will be written
#SBATCH --error=logs/job_%j.err   # File to which STDERR will be written
#SBATCH --mail-type=FAIL           # Type of email notification- BEGIN,END,FAIL,ALL
#SBATCH --mail-user=<your-email>  # Email to which notifications will be sent

# print info about current job
# echo "---------- JOB INFOS ------------"
#scontrol show job $SLURM_JOB_ID 
# echo -e "---------------------------------\n"

export HOME=/home/slurm
# Due to a potential bug, we need to manually load our bash configurations first
source $HOME/.bashrc

# install mini-conda
#curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o ~/miniconda.sh 
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -u -b -p $HOME/miniconda
source ~/miniconda/bin/activate
conda init bash

#create myenv
source $HOME/.bashrc
conda create -y -n myenv
pip install ipdb

# Next activate the conda environment 
conda activate myenv
conda install -y pytorch numpy

# Run our code --no-gpu
echo "-------- PYTHON OUTPUT ----------" 
python3 slurm-helloworld/src/multiply.py --timer_repetitions 10000 --no-gpu
echo "---------------------------------"

# Deactivate environment again
conda deactivate
