package require topotools

mol new  AF-trim_autopsf.psf
mol addfile AF-trim_autopsf.pdb

set sel [atomselect top "all"]

topo guessatom   element mass

mol new complex.psf
mol addfile complex.pdb

topo guessatom   element mass

set all [atomselect top "all"]
set prot [atomselect top  "resname LIG"]
$all set occupancy 0
$prot set occupancy 1

$all writepdb qmmm.pdb

quit

