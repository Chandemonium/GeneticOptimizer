# GeneticOptimizer
This code wraps around the Cuby4 parameter optimization procedure. The Template.yaml file 
is the Cuby4 job file that runs in conjunction with this code. This genetic optimization code
was specifically written to paramterize our new SCS-MP2D method. 
The code runs in parallel, so your job submission script must have a core for each population within a generation. 

Python version 3 and also Cuby4 (http://cuby4.molecular.cz/installation.html) are necessary for use of this code.

Run the program as follows:
python Genetic_Optimizer_rewrite.py argv1 argv2 argv3 > Genetic_Optimizer_rewrite.out

Three arguments must be supplied after the python script:
1. Number of generation (integer)
2. Number of populations (parameter sets) in the initial generation (int)
3. Number of populations in each subsequent generation (int)

