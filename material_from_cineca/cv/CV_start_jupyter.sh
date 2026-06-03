#!/bin/bash
        
#SBATCH --job-name=jupyter_environ

#SBATCH --account=tra26_bbs
#SBATCH --partition=boost_usr_prod
#SBATCH --time=05:00:00
#SBATCH --reservation=s_tra_bbs4 ### Add here the reservation ###
#SBATCH --nodes=1
#SBATCH --gres=gpu:4
#SBATCH --exclusive

#SBATCH --error logs/jupyter.err
#SBATCH --output logs/jupyter.out

# Enable cuda and load the python module
module load profile/deeplrn
module load cineca-ai

# Get the worker list associated to this slurm job
worker_list=($(scontrol show hostnames "$SLURM_JOB_NODELIST"))

# Set the first worker as the head node and get his ip
head_node=${worker_list[0]}
head_node_ip=$(srun --nodes=1 --ntasks=1 -w "$head_node" hostname --ip-address)

# Print ssh tunnel instruction
jupyter_port=$(($RANDOM%(64511-50000+1)+50000))
jupyter_token=${USER}_${jupyter_port}
echo ===================================================
echo [INFO]: To access the Jupyter server, remember to open a ssh tunnel with: 
echo ssh -L $jupyter_port:$head_node_ip:$jupyter_port ${USER}@login02-ext.leonardo.cineca.it -N
echo then you can connect to the jupyter server at http://127.0.0.1:$jupyter_port/lab?token=$jupyter_token
echo ===================================================

# Start the head node
echo [INFO]: Starting jupyter notebook server on $head_node 

# Note that the jupyter notebook command is available only because we have enabled the venv
command="jupyter lab --ip=0.0.0.0 --port=${jupyter_port} --NotebookApp.token=${jupyter_token}"
echo [INFO]: $command
$command &

echo [INFO]: Your env is up and running.

sleep infinity
