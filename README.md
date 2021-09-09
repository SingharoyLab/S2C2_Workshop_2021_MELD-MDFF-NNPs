# S2C2 Workshop Sept. 8-10th 2021
Here we a predict protein ligand complex structure from the corresponding amino acid sequcnces using density map. We achieved this using 4 different tools in 6 steps. 

## Outline
Steps:

1. At first we ran AlphaFold prediction on the protein sequence to predict initial structure. AF2 did faily good job in predicting the initial structure except two region which were poorly predicted with wrong topology and do not fit in the map well.

2. Then we run MELD from the AF2 prediction to get correct fold and topology of the overall protein and predicted structure now fits well in the map.

3. We ran MDFF on the MELD predicted to produce structure which fits perfectly to map and has very low RMSD.

4. Then 
## Links
