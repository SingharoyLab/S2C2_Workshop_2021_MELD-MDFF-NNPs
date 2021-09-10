#!/usr/bin/env python3

from __future__ import print_function
import torchani
import torch
import socket
import os
import sys

def readinput(fname):
    infile = open(fname,"r")

    line = infile.readline()

    numQMatms=int(line.split()[0])
    numMMatms=int(line.split()[1])

    # Gets number of point charges
    numPntChr = int(line.split()[1].replace("\n",""))

    # stores all lines written to ORCA's input file
    outLinesQM = []

    # stores all lines written to ORCA's point charge file
    outLinesPC = []

    # The first line in the point charge file is composed only of the total number
    # of point charges in the file.
    outLinesPC.append(str(numPntChr) + "\n")

    # Identation
    ident = "  "

    lineIndx = 1
    elements=[]
    crd=[]
    charges=[]

    for line in infile:
        if lineIndx <= numQMatms:            
            fields=line.split()
            elements.append(fields[3])
            crd.append([float(fields[0]), float(fields[1]), float(fields[2])])
        else:
            charges.append(0)
            
        lineIndx += 1
    return(elements, crd, charges)

device=None

sock_address = os.environ['SLURM_TMPDIR'] + '/ani_socket'
os.system('rm -f '  + sock_address)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(sock_address)
server.listen(100)

while True:
    conn, _ = server.accept()
    datagram = conn.recv(1024)
    if not datagram:
        break
    else:
        fname=datagram.decode('utf-8')
        (elements, crd, charges)=readinput(fname)
        print(elements)
        print(crd)
        if(device is None):
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            model=torchani.models.ANI2x()
            model=model.to(device)
            species = model.species_to_tensor("".join(elements)).to(device).unsqueeze(0)

        coordinates=torch.tensor([crd], requires_grad=True, device=device).cuda()
        coordinates=coordinates.to(device)
        _, energy = model((species, coordinates))
        derivative = torch.autograd.grad(energy.squeeze(), coordinates)[0]
        d=derivative.squeeze(0).to('cpu').numpy()
        print(d)
        finFile = open(fname + '.result', 'w')
        finFile.write(str(energy.item()*627.509469) + "\n")

        for i in range(len(elements)):
            finFile.write(str(-627.509469*d[i][0].item()) + " " + str(-627.509469*d[i][1].item())  +
                          ' ' + str(str(-627.509469*d[i][2].item()) ) + " " + str(0) + "\n")
        finFile.close()
        conn.send("D\r".encode("utf-8"))

server.close()
os.remove(sock_address)
