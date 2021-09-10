# MDFF Receptor
For a general tutorial on running Molecular Dynamics Flexible Fitting (MDFF) Simulations in NAMD please follow the link below.

http://www.ks.uiuc.edu/Training/Tutorials/science/mdff/tutorial_mdff-html/

What follows is a general description of the steps taken to produce the model shown in our demonstration.

## MDFF Steps
MDFF works by converting cryo-EM electrostatic potential maps or x-ray density maps into 3D atomwise potentials to refine atomic structures with low potential energies.

### Map preparation
The maps contained in this directory is a simulated map based off of the crystal structure 2XHX using the mdff sim command in VMD at resolutions 3 and 5 Angstroms.  The maps were then converted to potential maps using the mdff griddx command.

### Step 1 (hsp-step1.namd)
Coupling protein backbone atoms (no H) to the 5 Angstrom potential map at a gscale of 0.3.

### Step 2 (hsp-step2.namd)
Coupling protein backbone and sidechains atoms (no H) to the 3 Angstrom potential map at a gscale of 0.5.
