import readfof
import numpy as np

filename = 'ODD_m_310'

# input files
snapdir = '/Users/josueaubert/Documents/Tsinghua2026/delaunay-parity/' + filename #folder hosting the catalogue
snapnum = 1                                            #redshift 0

# determine the redshift of the catalogue
z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
redshift = z_dict[snapnum]
redshift=0.0

# read the halo catalogue
FoF = readfof.FoF_catalog(snapdir, snapnum, long_ids=False,
                          swap=False, SFR=False, read_IDs=False)

# get the properties of the halos
pos_h = FoF.GroupPos/1e3            #Halo positions in Mpc/h
mass  = FoF.GroupMass*1e10          #Halo masses in Msun/h
vel_h = FoF.GroupVel*(1.0+redshift) #Halo peculiar velocities in km/s
Npart = FoF.GroupLen                #Number of CDM particles in the halo

np.savetxt(filename + '.txt', pos_h, fmt='%.6f')
print(f"{len(pos_h)} halos, range {pos_h.min():.1f}–{pos_h.max():.1f} Mpc/h")