#!/bin/bash
#SBATCH --gres=gpu:2
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --output std.out
#SBATCH --mem-per-cpu=1024M 
#SBATCH --account=rrg-crowley-ac
#SBATCH --job-name=mdff-nnp
#SBATCH --time=24:00:00

cd /project/6007501/crowley/mdff/mdff_2xhx_lig-receptor/ligand-model-0

export LD_LIBRARY_PATH=/home/crowley/programs/namd/NAMD_2.14_Linux-x86_64-multicore:$LD_LIBRARY_PATH
export PATH=/home/crowley/programs/namd/NAMD_2.14_Linux-x86_64-multicore:$PATH
module purge
module load StdEnv/2020
export SLURM_TMPDIR=/dev/shm
nohup python /home/crowley/projects/rrg-crowley-ac/crowley/mdff/mdff_2xhx_lig-receptor/server_ani2x.py > server.log&


namd2  +p32  mdff-nnp.conf > mdff-nnp.out

sleep 10000

