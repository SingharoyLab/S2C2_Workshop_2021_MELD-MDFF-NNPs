
proc mkreps { MolID MolName ColoringMethod SelTxt } {
    # Change Current Rep
    mol rename $MolID $MolName
    mol modstyle 0 $MolID NewCartoon
    mol modmaterial 0 $MolID Opaque
    mol modcolor 0 $MolID $ColoringMethod
    mol modselect 0 $MolID all
    # Add Rep
    mol color Name
    mol representation Licorice 0.300000 12.000000 12.000000
    mol selection "$SelTxt"
    mol material Opaque
    mol addrep $MolID
}

mol default style NewCartoon


set count 3
for {set i 0} {$i < 9} {incr i} {
    set sys ligand-model-$i
    mol new $sys/complex.psf
    mol addfile $sys/complex.pdb
    for {set k 1} {$k <= 2} {incr k} {
	mol addfile $sys/mdff-step-$k.dcd waitfor -1
    }
    set myid [molinfo top]
    mkreps $myid $sys "ColorID $count" "not protein and not water and not ion"
    incr count

}

