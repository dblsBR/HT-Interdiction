[![INFORMS Journal on Computing Logo](https://INFORMSJoC.github.io/logos/INFORMS_Journal_on_Computing_Header.jpg)](https://pubsonline.informs.org/journal/ijoc)

# A Bi-level Network Interdiction Problem to Minimize the Number of Active Special Arcs in the Maximum Flow
This archive is distributed in association with the [INFORMS Journal on Computing](https://pubsonline.informs.org/journal/ijoc) under the [MIT License](LICENSE).

The purpose of this repository is to share the codes, instances, and results used in the paper ["A Bi-level Network Interdiction Problem to Minimize the Number of Active Special Arcs in the Maximum Flow"] authored by Daniel B. Lopes da Silva, Thomas C. Sharkey and Yongjia Song

## Dataset 
The "data" folder contains all the datasets used in the paper, separated by type of network according to the computational experiments described in the paper, which includes ten "Type1" networks, ten "Type2" networks, and 10 "HT" (Human Trafficking) networks. MFNIP method uses "Modified Networks" (same topology as the original networks, but special arcs have a capacity of 1 and the remaining arcs have 
an infinite capacity). Although the conversion from an original network to the corresponding "Modified Network" is straightforward, we also provide the corresponding "Modified Network" with respect to each of the original networks (Type1, Type2, and HT). All these networks are provided in CSV (comma separated values) format.
Lastly, for the HT networks, we provide a visual representation in terms of the single trafficker operations in PDF format.


## Results 
The "results" folder contains all the results discussed in the paper including the results of the experiments discussed at the Online Supplement. 
"Type1" and "Type2" folders include individual results from the experiments conducted with "Alternative", "Direct", "MFNIP_Method" and "Optimistic" as well as a folder ("stats") with the average running times. For the general pessimistic approaches 
("Alternative" and "Direct"), we report the individual results files ("InstancesResults"), the logfiles, MIP warm start files with respect to optimistic solutions ("MST_Optimistic_Files"), MIP warm start files with respect to MFNIP solutions ("MST_MFNIP_Files"), and a summary file for each approach with respect to each type of network.
For "HT" experiments, according to the paper, we report the results for "Optimistic" and "MFNIP_Method", as well as a "stats" folder with running time averages. These approaches do not use MIP warm start, so we do not generate "MST" files. Also, because both approaches solved each instance in less than a second, we do not report their logfiles.
Folder "Online Supplement" contains the results from the experiments discussed on "Online Suplement B - Penalty-based Benders Decomposition Approach", "Online Suplement G - Size of Pessimistic Formulations and Initial Gap at the Root Node", and "Online Suplement H - Effects of MIP Warm Start". NOTE: all the information discussed in "Online Suplement F - Gap from Pessimistic Approaches on Layered Networks" can be obtained from the "Summary" files.  



## Replicating
The src folder contains the source code for all the experiments discussed in the paper. All the codes were implemented using Python through the "Jupyter Notebook" platform and therefore all the source codes are in the "ipynb" format. The conversion to pure "py" format can be easily carried out. 

For the approaches ("Optimistic" and "MFNIP_Method") that were used with both layered and HT networks, although the main part of the algorithms are equal, the output is slightly different, so we provide both versions (e.g., "Optimistic" for layered networks and "Optimistic" for HT networks). The "OnlineSupplement" folder contains the "Benders" approach and a version of both "Direct" and "Alternative" that does not use MIP Warm Start.

To run the codes and fully replicate the experiments, you will need a valid "Gurobi" license.


