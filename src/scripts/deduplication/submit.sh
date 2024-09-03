#!/bin/bash
#SBATCH -p memory
#SBATCH -N 1 -c 128
#SBATCH --ntasks-per-node=1
#SBATCH -t  20:00:00
#SBATCH -A lt200258
#SBATCH -J deduplicate

ml Mamba

conda deactivate
conda activate /project/lt200258-aithai/may/env_data_process

cd /project/lt200258-aithai/may/data-processing

export HF_DATASETS_CACHE="/project/lt200258-aithai/may/.cache"

python ./src/scripts/deduplication/deduplicate.py
# python ./src/data/scripts/decontamination/decontaminate.py