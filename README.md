# MEND/MEND-R PROJECT (Human Trafficking Network Interdiction)

# LAST UPDATE: JUNE 29, 2023

This repoitory contains codes, instances and results from MEND-R project.
The files are divided into two folders: Human_Trafficking and General. Networks in the "Human_Trafficking" folder were generated according to the methodology proposed in Kosmas et al. (2023) (A 
transdisciplinary approach for generating synthetic but realistic domestic sex trafficking networks. IISE Transactions) and hence elements in these networks represent elements of human-trafficking (HT) networks
(e.g. traffickers and victims). Accordingly, the output of the codes in the "Human_Trafficking" folder reflect these features (e.g., number of traffickers removed, number of victims removed). Networks in the "General"
folder are generated according to the methodology described in our paper (layered networks) and their elements do not have specified meaning. Consequently, the outputs of codes in the "General" folder are more general
(e.g., number of interdictions in the first level, number of interdictions in the second level). 

# JUPTER NOOTEBOOK CODES 
There a jupyter noteebook version of all the codes: optimistic (HT), optimistic (General), pessimistic (HT), pessimistic (General).

# PYHTON (py) CODES
Only the pessimitic-general version of the codes in py file is available at this point. For this version, type "python run.py" in a terminal to run the codes. Parameters such as number of networks and budget levels must
be specified directly in the "run.py" file.
