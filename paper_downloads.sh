#!/bin/bash
#SBATCH --job-name=descarga       # Nombre del trabajo
#SBATCH --output=test_%j.log         # Nombre del output (%j se reemplaza por el ID del trabajo)
#SBATCH --error=test_%j.err          # Output de errores (opcional)
#SBATCH --ntasks=1                   # Correr 1 tarea
#SBATCH --cpus-per-task=4          # Numero de cores por tarea
#SBATCH --time=0-16:00:00            # Timpo limite d-hrs:min:sec
#SBATCH --mem=8G         # Memoria por proceso
#SBATCH --mail-type=END,FAIL         # Enviar eventos al mail (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=rodrigo.oportot@cenia.cl    # El mail del usuario
#SBATCH --partition=ialab             # Se tiene que elegir una partición de nodos con GPU
#SBATCH --nodelist=antuco

echo $HOME

source $HOME/archive/miniconda3/bin/activate

conda activate conferencias

which python
which pip

python paper_downloader.py