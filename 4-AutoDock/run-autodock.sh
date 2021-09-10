#!/usr/bin/env bash
############################################################## 
# Author:               John Vant 
# Email:              jvant@asu.edu 
# Affiliation:   ASU Biodesign Institute 
# Date Created:          210904
############################################################## 
# Usage: 
############################################################## 
# Notes: 
############################################################## 

cd /shared/MDFF_NNP_All/CryoEM_Workshop_Standford/autodock_output_2
vina_exec="/shared/Programs/AutoDock/autodock_vina_1_1_2_linux_x86/bin/vina"

$vina_exec --config conf.txt --log loggy.log



