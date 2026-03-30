#!/bin/bash
#SBATCH --job-name=small       # Nombre del trabajo
#SBATCH --output=test_%j.log         # Nombre del output (%j se reemplaza por el ID del trabajo)
#SBATCH --error=test_%j.err          # Output de errores (opcional)
#SBATCH --ntasks=1                   # Correr 1 tarea
#SBATCH --cpus-per-task=8          # Numero de cores por tarea
#SBATCH --time=0-04:00:00            # Timpo limite d-hrs:min:sec
#SBATCH --mem=100G         # Memoria por proceso
#SBATCH --mail-type=END,FAIL         # Enviar eventos al mail (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=rodrigo.oportot@cenia.cl    # El mail del usuario
#SBATCH --partition=ialab             # Se tiene que elegir una partición de nodos con GPU
#SBATCH --gres=gpu:1                # Usar 2 GPUs  (se pueden usar N GPUs de marca especifica usando --gres=gpu:marca:N)
#SBATCH --nodelist=antuco

echo $HOME
echo $WORKSPACE
echo $ARCHIVE

source $HOME/archive/miniconda3/bin/activate

conda activate conferencias

which python
which pip

# Define your massive storage path
export HF_HOME="/home/roportot/archive/huggingface_cache"

export HSA_OVERRIDE_GFX_VERSION=9.0.10

export ROCM_PATH=/opt/rocm
export LD_LIBRARY_PATH=$ROCM_PATH/lib:$ROCM_PATH/lib64:$LD_LIBRARY_PATH

export HIP_VISIBLE_DEVICES=0

#conda install -c conda-forge uv -y

#uv pip install git+https://github.com/huggingface/transformers

# Install base PyTorch (adjust cuXXX to your CUDA version, e.g., cu121 or cu124)
#pip install torch --index-url https://download.pytorch.org/whl/cu124

# Install only the necessary text processing libraries
#pip install accelerate mistral_common huggingface_hub

#uv pip install bitsandbytes

#export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH

python inference_script_pypdf.py

#rocm-smi
#ls /opt/rocm*

#/opt/rocm/bin/rocminfo