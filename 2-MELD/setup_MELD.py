#!/usr/bin/env python
# encoding: utf-8

import numpy as np
from meld.remd import ladder, adaptor, leader
from meld import comm, vault
from meld import system
from meld import parse
import meld.system.montecarlo as mc
from meld.system.restraints import LinearRamp,ConstantRamp
from collections import namedtuple
import glob as glob
import os

N_REPLICAS = 16
N_STEPS = 5000
BLOCK_SIZE = 100



def gen_state_templates(index, templates):                                                                                                                                                                              
    n_templates = len(templates)
    print((index,n_templates,index%n_templates))
    a = system.ProteinMoleculeFromPdbFile(templates[index%n_templates])
    #Note that it does not matter which forcefield we use here to build
    #as that information is not passed on, it is used for all the same as
    #in the setup part of the script
    b = system.SystemBuilder(forcefield="ff14sbside")
    c = b.build_system_from_molecules([a])
    pos = c._coordinates
    c._box_vectors=np.array([0.,0.,0.])
    vel = np.zeros_like(pos)
    alpha = index / (N_REPLICAS - 1.0)
    energy = 0 
    return system.SystemState(pos, vel, alpha, energy,c._box_vectors)
    
# Restraints on Protein CA
def make_cartesian_collections(s, scaler, residues, delta=0.2, k=250.):
    cart = []
    backbone = ['CA']
    #Residues are 1 based
    #index of atoms are 1 base
    for i in residues:
        # print i
        for b in backbone:
            # print b
            atom_index = s.index_of_atom(i,b) - 1
            x,y,z = s.coordinates[atom_index]/10.
            rest = s.restraints.create_restraint('cartesian',scaler, LinearRamp(0,15,0,1),res_index=i, atom_name=b,
                x=x, y=y, z=z, delta=delta,force_const=k)
            cart.append(rest)
    return cart


def setup_system():
    #print "!!!Starting from Templates!!!"
    templates = glob.glob('TEMPLATES/*.pdb')
    
    # build the system
    p = system.ProteinMoleculeFromPdbFile(templates[0])
    b = system.SystemBuilder(forcefield="ff14sbside")
    s = b.build_system_from_molecules([p])
    s.temperature_scaler = system.GeometricTemperatureScaler(0, 0.4, 300, 500.)
    n_res = s.residue_numbers[-1]

    const_scaler = s.restraints.create_scaler('constant')
    pro_res = list(range(26,91)) + list(range(121,151))+list(range(154,163))+list(range(165,193))+list(range(199,209))
    print(pro_res)
    # Keep protein close to starting conformation
    rest = make_cartesian_collections(s, const_scaler, pro_res)
    s.restraints.add_as_always_active_list(rest)
 
    # create the options
    options = system.RunOptions()
    options.implicit_solvent_model = 'gbNeck2'
    options.use_big_timestep = False
    options.use_bigger_timestep = True
    options.cutoff = 1.8

    options.use_amap = False
    options.amap_alpha_bias = 1.0
    options.amap_beta_bias = 1.0
    options.timesteps = 11111
    options.minimize_steps = 20000
    options.min_mc = None
    options.run_mc = None
    for i in range(30):
        #print "!!!DO NOT USE MC MIN!!!"
        print ("Heads up! using MC minimizer!")
    #options.min_mc = sched

    # create a store
    store = vault.DataStore(s.n_atoms, N_REPLICAS, s.get_pdb_writer(), block_size=BLOCK_SIZE)
    store.initialize(mode='w')
    store.save_system(s)
    store.save_run_options(options)

    # create and store the remd_runner
    l = ladder.NearestNeighborLadder(n_trials=100)
    policy = adaptor.AdaptationPolicy(2.0, 50, 50)
    a = adaptor.EqualAcceptanceAdaptor(n_replicas=N_REPLICAS, adaptation_policy=policy)

    remd_runner = leader.LeaderReplicaExchangeRunner(N_REPLICAS, max_steps=N_STEPS, ladder=l, adaptor=a)
    store.save_remd_runner(remd_runner)

    # create and store the communicator
    c = comm.MPICommunicator(s.n_atoms, N_REPLICAS)
    store.save_communicator(c)

    # create and save the initial states
    #states = [gen_state(s, i) for i in range(N_REPLICAS)]
    states = [gen_state_templates(i,templates) for i in range(N_REPLICAS)]
    store.save_states(states, 0)

    # save data_store
    store.save_data_store()

    return s.n_atoms


setup_system()

