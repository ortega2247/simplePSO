from pysb.core import *
from pysb.bng import *
from pysb.integrate import *
import matplotlib.pyplot as plt
import numpy as np
from pysb.util import alias_model_components
from pysb.simulator.bng import BngSimulator
from pysb.simulator import ScipyOdeSimulator
from pysb.tools import render_reactions


Model()

model.enable_synth_deg()

Monomer('TNF', ['brec'])
Monomer('TNFR', ['blig', 'brip'])
Monomer('TRADD', ['brec', 'brip'])
Monomer('RIP1', ['bscf', 'bub1', 'bub2','bDD', 'btraf', 'bRHIM','state'], {'state': ['um', 'K63ub', 'deub','ub', 'po4', 'trunc']})
Monomer('TRAF', ['brip', 'bciap'])
Monomer('cIAP', ['btraf'])
Monomer('A20', ['brip'])
Monomer('A20t')
Monomer('CYLD', ['brip','btraf'])
Monomer('FADD', ['bDD', 'bDED1'])
Monomer('proC8', ['bDED'])
Monomer('C8', ['bf', 'flip', 'state'], {'state': ['A', 'I']})
Monomer('flip_L', ['bDED', 'state'], {'state': ['A', 'I']})
Monomer('RIP3', ['bRHIM', 'bDD', 'state'], {'state': ['um', 'po4', 'trunc', 'N']})
Monomer('MLKL', ['bRHIM', 'state'], {'state': ['um', 'active', 'inactive']})
Monomer('TAK1', ['brip', 'bmapk'])
# Monomer('NEMO', ['brip', 'btak', 'bikk', 'state'], {'state': ['I', 'A']})
Monomer('LUBAC', ['brip'])

# Parameter('TNF_0', 23) #698 is 30ng/ml of TNF
# Parameter('TNFR_0', 4800) #0.00246
# Parameter('TRADD_0', 9000) #
# Parameter('RIP1_0', 40000) #47000 0.04
# Parameter('TRAF_0', 9000) # 8.3e-4
# Parameter('cIAP_0', 9000) #10000 8.3e-4
# Parameter('A20_0', 9000) #2256
# Parameter('CYLD_0', 9000) #50000 # 0.004
# Parameter('FADD_0', 8030) # 0.0033
# Parameter('flip_L_0', 3900) # 0.004 # 0.09
# Parameter('Lubac_0', 7226)
# Parameter('C8_0', 9000) #10000 # 0.033 # 0.093 # 0.0107
# Parameter('RIP3_0', 40000) #20000
# # Parameter('NEMO_0', 24000) # 1000000
# Parameter('MLKLa_0', 10000) # 100000 #0.0034

Parameter('TNF_0', 2326)
Parameter('TNFR_0', 4800)
Parameter('TRADD_0', 4696) #4696
Parameter('RIP1_0', 40000)
Parameter('TRAF_0', 11776) #11776
Parameter('cIAP_0', 9000)
Parameter('A20_0', 9000)
Parameter('CYLD_0', 9000)
Parameter('FADD_0', 3109) #3109
Parameter('flip_L_0', 3900)
Parameter('Lubac_0', 7226)
Parameter('C8_0', 3799) #3799
Parameter('RIP3_0', 10654) #10654
Parameter('MLKLa_0', 5544) #5544

# Parameter('TNF_0', 232) # initial condition
# Parameter('TNFR_0', 4800)
# Parameter('TRADD_0', 4696) #9000
# Parameter('RIP1_0', 40000)
# Parameter('TRAF_0', 9000)
# Parameter('cIAP_0', 9000)
# Parameter('A20_0', 9000)
# Parameter('CYLD_0', 9000)
# Parameter('FADD_0', 3109) #8030
# Parameter('flip_L_0', 3900)
# Parameter('Lubac_0', 7226)
# Parameter('C8_0', 3798) #9000
# Parameter('RIP3_0', 10653) #40000
# Parameter('MLKLa_0', 5544) #10000


Initial(TNF(brec=None), TNF_0)
Initial(TNFR(blig=None, brip=None), TNFR_0)
Initial(TRADD(brec=None, brip=None), TRADD_0)
Initial(RIP1(bscf=None, btraf=None, bub1=None, bub2=None, bDD = None, bRHIM = None , state='um'), RIP1_0)
Initial(TRAF(brip=None, bciap=None), TRAF_0)
Initial(cIAP(btraf=None), cIAP_0)
Initial(A20(brip = None), A20_0)
Initial(CYLD(brip=None, btraf = None), CYLD_0)
Initial(FADD(bDD=None, bDED1=None), FADD_0)
Initial(RIP3(bRHIM=None, bDD = None, state='um'), RIP3_0)
Initial(flip_L(bDED=None, state = 'A'), flip_L_0)
Initial(LUBAC(brip=None), Lubac_0)
# Initial(NEMO(brip = None, btak = None, bikk = None, state = 'I'), NEMO_0)
Initial(C8(bf=None, flip = None, state='I'), C8_0)
Initial(MLKL(bRHIM=None, state='um'), MLKLa_0)


#COMPLEX I FORMATION AND RELEASE OF RIP1(K63)
Parameter('bind_TNF_TNFR_kf', 1e-6)
Parameter('bind_TNF_TNFR_kr',1e-3)
Parameter('TNF_deg1', 0.001)
Parameter('bind_TNFRANY_TRADD_kf', 1e-6)
Parameter('bind_TNFRANY_TRADD_kr',1e-3)
Parameter('bind_TNFRANY_RIP1um_kf', 1e-6)
Parameter('bind_TNFRANY_RIP1um_kr', 1e-3)
Parameter('bind_RIP1ANY_TRAFum_kf', 1e-6)
Parameter('bind_RIP1ANY_TRAFum_kr', 1e-3)
Parameter('bind_cIAP_TRAFum_to_cIAPTRAFum_kf', 1e-6)
Parameter('bind_cIAP_TRAFum_to_cIAPTRAFum_kr',1e-3)



Rule('bind_TNF_TNFR', TNF(brec=None) + TNFR(blig=None, brip=None) | TNF(brec=1) % TNFR(blig=1, brip=None), bind_TNF_TNFR_kf, bind_TNF_TNFR_kr)

Rule('TNF_deg', TNF(brec = None) >> None, TNF_deg1)

Rule('bind_TNFRANY_TRADD', TNF(brec=1) % TNFR(blig=1, brip=None) + TRADD(brec = None, brip = None ) |
     TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = None ), bind_TNFRANY_TRADD_kf, bind_TNFRANY_TRADD_kr)

Rule('bind_TNFRANY_RIP1um', TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = None ) + RIP1(bscf=None, btraf=None, bub1=None, bub2=None, bDD = None, bRHIM=None, state='um')
     | TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = None,bRHIM=None, state='um'), bind_TNFRANY_RIP1um_kf, bind_TNFRANY_RIP1um_kr)

Rule('Complex_I_ubiquitylation1', TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = None,bRHIM=None, state='um') + TRAF(brip=None, bciap=None)
     | TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=4, bub1=None, bub2=None,bDD = None,bRHIM=None, state='um') % TRAF(brip=4, bciap=None), bind_RIP1ANY_TRAFum_kf, bind_RIP1ANY_TRAFum_kr)


Rule('Complex_I_ubiquitylation', TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=4, bub1=None, bub2=None,bDD = None,bRHIM=None, state='um') % TRAF(brip=4, bciap=None) + cIAP(btraf = None)
     | TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=4, bub1=None, bub2=None,bDD = None,bRHIM=None, state='um') % TRAF(brip=4, bciap=5) % cIAP(btraf = 5), bind_cIAP_TRAFum_to_cIAPTRAFum_kf, bind_cIAP_TRAFum_to_cIAPTRAFum_kr)


Parameter('CompI_UB2', 1e-1)
Parameter('bind_LUBAC_kf', 1e-6)
Parameter('bind_LUBAC_kr', 1e-3)
Parameter('bind_RIP1K63ubANY_A20_kf', 1e-6)
Parameter('bind_RIP1K63ubANY_A20_kr',1e-3)
Parameter('k_A20_1', 1e-1)
Parameter('bind_RIP1K63ubANY_CYLD_kf', 1e-6)
Parameter('bind_RIP1K63ubANY_CYLD_kr', 1e-3)
Parameter('k_CYLD_1', 1e-1)

Rule('Complex_I_ubiquitylation2', TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=4, bub1=None, bub2=None,bDD = None,bRHIM=None, state='um') % TRAF(brip=4, bciap=5) % cIAP(btraf = 5)
     >> TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=4, bub1=None, bub2=None,bDD = None,bRHIM=None, state='K63ub') % TRAF(brip=4, bciap=5) % cIAP(btraf = 5), CompI_UB2)


Rule('ComplexI_Lubac', TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=4, bub1=None, bub2=None,bDD = None,bRHIM=None, state='K63ub') % TRAF(brip=4, bciap=5) % cIAP(btraf = 5) + LUBAC(brip = None)
     | TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=4, bub1=6, bub2=None,bDD = None,bRHIM=None, state='K63ub') % TRAF(brip=4, bciap=5) % cIAP(btraf = 5) % LUBAC(brip = 6),
     bind_LUBAC_kf, bind_LUBAC_kr)


#RIP1 K63ub to be deub by A20 or CYLD

Rule('bind_RIP1K63ubANY_A20', TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=4, bub1=6, bub2=None,bDD = None,bRHIM=None, state='K63ub') % TRAF(brip=4, bciap=5) % cIAP(btraf = 5) % LUBAC(brip = 6) + A20(brip=None)
     | TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=4, bub1=6, bub2=7,bDD = None,bRHIM=None, state='K63ub') % TRAF(brip=4, bciap=5) % cIAP(btraf = 5) % LUBAC(brip = 6) % A20(brip=7),
     bind_RIP1K63ubANY_A20_kf, bind_RIP1K63ubANY_A20_kr)


Rule('A20_2', TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=4, bub1=6, bub2=7,bDD = None,bRHIM=None, state='K63ub') % TRAF(brip=4, bciap=5) % cIAP(btraf = 5) % LUBAC(brip = 6) % A20(brip=7)
     >>  TNF(brec = None) + TNFR(blig=None, brip=None) + TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = None,bRHIM=None, state='deub') + TRAF(brip=None, bciap=None) + cIAP(btraf = None) + LUBAC(brip = None) + A20(brip=None), k_A20_1)



Rule('bind_RIP1K63ubANY_CYLD', TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=4, bub1=6, bub2=None,bDD = None,bRHIM=None, state='K63ub') % TRAF(brip=4, bciap=5) % cIAP(btraf = 5) % LUBAC(brip = 6) + CYLD(brip=None)
     | TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=4, bub1=6, bub2=7,bDD = None,bRHIM=None, state='K63ub') % TRAF(brip=4, bciap=5) % cIAP(btraf = 5) % LUBAC(brip = 6) % CYLD(brip=7),
     bind_RIP1K63ubANY_CYLD_kf, bind_RIP1K63ubANY_CYLD_kr)

Rule('A20_1', TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=4, bub1=6, bub2=7,bDD = None,bRHIM=None, state='K63ub') % TRAF(brip=4, bciap=5) % cIAP(btraf = 5) % LUBAC(brip = 6) % CYLD(brip=7)
     >> TNF(brec = None) + TNFR(blig=None, brip=None) + TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = None,bRHIM=None, state='deub') + TRAF(brip=None, bciap=None) + cIAP(btraf = None) + LUBAC(brip = None) + CYLD(brip=None),
     k_CYLD_1)

#Initiating Necroptosis
Parameter('bind_TRADDANYRIP1ANY_FADD_kf', 1e-1)
Parameter('bind_TRADDANYRIP1ANY_FADD_kr', 3.11e-7)
Parameter('bind_FADD_proC8_2_kf', 3.27e-06)
Parameter('bind_FADD_proC8_2_kr', 0.018)
Parameter('bind_FADDANY_flip_L_kf',3.27e-06)
Parameter('bind_FADDANY_flip_L_kr', 0.018)
Parameter('bind_C8_flip_L_kf',3.27e-2)
Parameter('bind_C8_flip_L_kr', 0.018) #not used
Parameter('kc_c8_1', 1e-1)
Parameter('bind_FADDANY_RIP3_kf', 1e-6)
Parameter('bind_FADDANY_RIP3_kr', 1e-3)
Parameter('kc_c8_2', 1e-1)

#RIP1 deub and necrosome formation

Rule('bind_TRADDANYRIP1ANY_FADD', TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = None,bRHIM=None, state='deub') + FADD(bDD=None, bDED1 = None)
     | TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = 1,bRHIM=None, state='deub') % FADD(bDD=1,bDED1 = None), bind_TRADDANYRIP1ANY_FADD_kf, bind_TRADDANYRIP1ANY_FADD_kr)


Rule('bind_FADD_proC8_2', TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = 1,bRHIM=None, state='deub') % FADD(bDD=1,bDED1 = None) + C8(bf=None, flip = None, state='I')
     | TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = 1,bRHIM=None, state='deub') % FADD(bDD=1,bDED1 = 2) % C8(bf=2,flip = None, state='I'), bind_FADD_proC8_2_kf, bind_FADD_proC8_2_kr)


Rule('bind_FADDANY_flip_L', TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = 1,bRHIM=None, state='deub') % FADD(bDD=1,bDED1 = 2) % C8(bf=2, flip = None,state='I') + flip_L(bDED=None, state = 'A')
     | TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = 1,bRHIM=None, state='deub') % FADD(bDD=1,bDED1 = 2) % C8(bf=2,flip = 4, state='I') % flip_L(bDED=4, state = 'A'), bind_FADDANY_flip_L_kf, bind_FADDANY_flip_L_kr)

Rule('activate_C8', TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = 1,bRHIM=None, state='deub') % FADD(bDD=1,bDED1 = 2) % C8(bf=2,flip = 4, state='I') % flip_L(bDED=4, state = 'A')
     | TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = 1,bRHIM=None, state='deub') % FADD(bDD=1,bDED1 = 2) % C8(bf=2,flip = 4, state='A') % flip_L(bDED=4, state = 'A'), bind_C8_flip_L_kf,bind_C8_flip_L_kr)

Rule('catalyze_FADDANY_flip_L', TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = 1,bRHIM=None, state='deub') % FADD(bDD=1,bDED1 = 2) % C8(bf=2,flip = 4, state='A') % flip_L(bDED=4, state = 'A') >>
     TRADD(brec = None, brip = None ) + RIP1(bscf=None, btraf=None, bub1=None, bub2=None,bDD = None,bRHIM=None, state='trunc') + FADD(bDD=None,bDED1 = None) + C8(bf=None,flip = None, state='I') + flip_L(bDED=None, state = 'I') , kc_c8_1)



#RIP3 reactions to MLKL

Rule('bind_FADDANY_proC8', TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = 1,bRHIM=None, state='deub') % FADD(bDD=1,bDED1 = None) + RIP3(bRHIM=None, bDD = None, state='um')
     | TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = 1,bRHIM=5, state='deub') % FADD(bDD=1,bDED1 = None) % RIP3(bRHIM=5, bDD = None, state='um'), bind_FADDANY_RIP3_kf, bind_FADDANY_RIP3_kr)

Rule('C8_activation2', TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = 1,bRHIM=5, state='deub') % FADD(bDD=1,bDED1 = None) % RIP3(bRHIM=5, bDD = None, state='um')
     >> TRADD(brec = None, brip = None ) + FADD(bDD=None,bDED1 = None) + RIP1(bscf = None, bub1 = None, bub2 = None, bDD=None, btraf=None , bRHIM = 5, state = 'deub')% RIP3(bRHIM=5, bDD = None, state='um'), kc_c8_2)

Parameter('bind_RIP1_RIP3po4_kf', 1e-2)
Parameter('RIP1po4_RIP3po4_kf', 1e-3)
Parameter('bind_RIP1po4_MLKLum_to_RIP1po4MLKLum_kf', 1e-3)
Parameter('bind_RIP1po4_MLKLum_to_RIP1po4MLKLum_kr', 1e-6)
Parameter('catalyze_RIP1po4MLKLum_to_RIP1po4_MLKLactive_kc', 1)

Rule('bind_FADDANYANYflip_LANYproC8ANY_RIP1um', RIP1(bscf = None, bub1 = None, bub2 = None, bDD=None, btraf=None , bRHIM = 5, state = 'deub')% RIP3(bRHIM=5, bDD = None, state='um')
     >> RIP1(bscf = None, bub1 = None, bub2 = None, bDD=None, btraf=None , bRHIM = 5, state = 'deub')% RIP3(bRHIM=5, bDD = None, state='po4'), bind_RIP1_RIP3po4_kf)

Rule('Rip1_PO4lation', RIP1(bscf = None, bub1 = None, bub2 = None, bDD=None, btraf=None , bRHIM = 5, state = 'deub')% RIP3(bRHIM=5, bDD = None, state='po4')
     >> RIP1(bscf = None, bub1 = None, bub2 = None, bDD=None, btraf=None , bRHIM = 5, state = 'po4')% RIP3(bRHIM=5, bDD = None, state='po4'), RIP1po4_RIP3po4_kf)

Rule('bind_RIP1po4_MLKLum_to_RIP1po4MLKLum', RIP1(bscf = None, bub1 = None, bub2 = None, bDD=None, btraf=None , bRHIM = 5, state = 'po4')% RIP3(bRHIM=5, bDD = None, state='po4') + MLKL(bRHIM=None, state='um')
     | RIP1(bscf = None, bub1 = None, bub2 = None, bDD=None, btraf=None , bRHIM = 5, state = 'po4')% RIP3(bRHIM=5, bDD = 1, state='po4') % MLKL(bRHIM=1, state='um'), bind_RIP1po4_MLKLum_to_RIP1po4MLKLum_kf,bind_RIP1po4_MLKLum_to_RIP1po4MLKLum_kr)

Rule('catalyze_RIP1po4MLKLum_to_RIP1po4_MLKLactive', RIP1(bscf = None, bub1 = None, bub2 = None, bDD=None, btraf=None , bRHIM = 5, state = 'po4')% RIP3(bRHIM=5, bDD = 1, state='po4') % MLKL(bRHIM=1, state='um')
     >>  MLKL(bRHIM=None, state='active') + RIP1(bscf = None, bub1 = None, bub2 = None, bDD=None, btraf=None , bRHIM = 5, state = 'po4')% RIP3(bRHIM=5, bDD = None, state='po4') , catalyze_RIP1po4MLKLum_to_RIP1po4_MLKLactive_kc)



Observable('RIP1_obs',RIP1(state='um'))
Observable('RIP1k63_obs',RIP1(state='K63ub'))
Observable('RIP1deub_obs',RIP1(state='deub'))
Observable('RIP1po4_obs',RIP1(state='po4'))
Observable('RIP3_obs', RIP3(state='um'))
Observable('MLKL_obs', MLKL(bRHIM=None, state='um'))
Observable('MLKLa_obs', MLKL(bRHIM=None, state='active'))
Observable('RIP13_obs', RIP1(bDD=ANY, bRHIM=1, state='deub') % RIP3(bRHIM=1, bDD = None, state='um'))
Observable('RIP13po4_obs', RIP1(bscf = None, bub1 = None, bub2 = None, bDD=None, btraf=None , bRHIM = 5, state = 'po4')% RIP3(bRHIM=5, bDD = None, state='po4'))
Observable('RIP1deub3po4_obs', RIP1(bscf = None, bub1 = None, bub2 = None, bDD=None, btraf=None , bRHIM = 5, state = 'deub')% RIP3(bRHIM=5, bDD = None, state='po4'))
Observable('TNF_obs', TNF(brec = ANY))
Observable('RIPk63_obs',  RIP1(bscf=None, bub1=None, state='K63ub'))
Observable('TNFR_TRADD', TNFR(blig=None, brip=1) % TRADD(brec=1, brip=None))
Observable('CI_k63_obs', TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) %
           RIP1(bscf=3, btraf=4, bub1=None, bub2=None,bDD = None,bRHIM=None, state='K63ub') % TRAF(brip=4, bciap=5) % cIAP(btraf = 5))
Observable('CI', TNF(brec = 1) % TNFR(blig=1, brip=2) % TRADD(brec = 2, brip = 3 ) % RIP1(bscf=3, btraf=4, bub1=None, bub2=None,bDD = None,bRHIM=None, state='um')
           % TRAF(brip=4, bciap=5) % cIAP(btraf = 5))
Observable('C8i_obs', C8(state = 'I'))
Observable('C8a_obs', C8(state = 'A'))
Observable('flip_obs', flip_L(state = 'A'))
Observable('A20_obs', A20(brip = None))
Observable('Fadd_obs', FADD(bDD=None, bDED1=None))
Observable('Tradd_obs', TRADD(brec=None, brip=None))
Observable('c8flip_obs', C8(flip = 4, state='A') % flip_L(bDED=4, state = 'A'))
Observable('CII_c8flp_obs', TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = 1,bRHIM=None, state='deub')
           % FADD(bDD=1,bDED1 = 2) % C8(bf=2,flip = 4, state='A') % flip_L(bDED=4, state = 'A'))
Observable('CII_obs', TRADD(brec = None, brip = 3 ) % RIP1(bscf=3, btraf=None, bub1=None, bub2=None,bDD = 1,bRHIM=5, state='deub')
           % FADD(bDD=1,bDED1 = None) % RIP3(bRHIM=5, bDD = None, state='um'))

generate_equations(model)
#
# params = np.array( [ 233, 4800, 9000, 40000, 9000, 9000, 9000, 9000, 8030, 3900, 7226, 9000, 40000, 5544,
#                     1.02145688e-05, 1.23516885e-03, 2.03754801e-04,7.81094339e-06,
#                      6.47910697e-03, 3.44471059e-06, 5.04179392e-05,1.29894688e-06,
#                      6.80159346e-04, 6.06116951e-06, 1.24025304e-05,3.73538835e-02,
#                      5.24538331e-06, 5.16924040e-04, 2.77489325e-05,9.99328700e-04,
#                      2.58066796e-01, 4.22932335e-07, 1.43821124e-04,5.39103684e-02,
#                      3.66441237e-01, 1.17753133e-06, 9.73005690e-06,2.83901083e-02,
#                      4.59314568e-05, 2.83567301e-03, 1.41058185e-01,2.16293904e-03,
#                      5.41837115e-02, 7.46230611e-07, 3.37655626e-04,7.88608420e-02,
#                      4.46416892e-03, 7.63221454e-04, 1.38301831e-04,5.07970779e-06,
#                      8.39843567e+00])
#
# tnf = [2326, 232, 23, 2]
# color = ['r', 'm', 'g', 'b']
# tspan = np.linspace(0, 1440, 1441)
# sim = ScipyOdeSimulator(model, tspan=tspan)
# # result = sim.run(param_values=params)
# result = sim.run(initials={TNF(brec=None): tnf}, param_values=params)
# df = result.dataframe
#
# pars = np.array([-5.17062017, -4.33539946, -3.82354714, -4.02214654 ,-3.0767188 , -5.51251846 ,
#          -2.97360486, -4.39627439, -3.84698848, -4.23486726 ,-2.78435757, -0.65393034 ,
#          -4.43584446, -1.85019061, -7.44842603, -1.52605512 ,-2.28886612, -6.22432534 ,
#          -2.10866254, -0.5810526 , -1.48580142, -6.88002083 ,-3.67754975, -2.82623357 ,
#          -4.11855817, -1.59155102, -0.46472857, -2.34906927 ,-1.71736511, -5.50864857 ,
#          -2.31736383, -0.15706048, -0.08934569, -1.         ,-4.05324232, -4.57716147 ,
#           1.83560621])

pars = np.array([-6.84706034, -2.08330446, -3.14547009, -6.56929084 ,-1.369488  ,-4.48673505,
        -1.72466745, -4.62106959, -3.28687671, -4.459295   ,-4.24427646, 0.12424465,
        -4.99663706, -2.26283345, -5.18987254, -3.36947399 ,-2.69044424,-5.41360843,
        -3.36114723, -0.38087772, -0.70822244, -6.55721053 ,-4.9452709 ,-2.86436244,
        -7.22755389, -2.61404629, -0.57005562, -1.33805278 ,-0.3711652 ,-4.84190537,
        -4.37686806,  0.28686297, -1.02215434, -1.22347279 ,-3.03682113,-5.59903273,
        1.07088531])
# pars = np.load('optimizer_best_1000_14.npy')
# pars =  np.load('optimizer_best_1000_mar7.npy')
rate_params = model.parameters_rules() # these are only the parameters involved in the rules
param_values = np.array([p.value for p in model.parameters]) # these are all the parameters
rate_mask = np.array([p in rate_params for p in model.parameters])
param_values[rate_mask] = 10 ** pars

fdkd = [3109, 933, 3109, 3109, 3109]
tdkd = [4696, 4696, 1409, 4696, 4696]
a20kd = [9000, 9000, 9000, 2700, 9000]
c8kd = [3799,3799, 3799, 3799,1140]
#
tnf = [2326, 232, 23, 2]
color = ['r', 'm', 'g', 'b', 'c']
tspan = np.linspace(0, 1440, 1441)
sim = ScipyOdeSimulator(model, tspan=tspan)
# result = sim.run(param_values=params)
result = sim.run(param_values=param_values)
# result = sim.run(param_values = param_values, initials={TNF(brec=None): tnf})
df = result.dataframe
t = np.array([0., 30,  60,   120,  180, 270,  480,  960, 1440])
data = np.array([0., 0., 0., 0., 0.01*5544, 0.05*5544, 0.5*5544, 0.99*5544, 1.*5544])


plt.figure()
# for n in range(0,5):
    # plt.plot(tspan, df.loc[n]['MLKLa_obs'].iloc[:], c = color[n],lw =1.5) #fst-pso
plt.plot(tspan/60, result.observables['MLKLa_obs'][:],lw = 1.5) #fppf
plt.scatter(t/60, data, lw = 2.5, color = 'k',marker = '.', zorder = 1)
# plt.plot(t/60, data)
plt.xlabel('Time [hours]', fontsize=14)
plt.ylabel('Phosphorylated MLKL amount [molecules]', fontsize=14)
plt.title('Sensitivity of pMLKL to varying KD Conditions 100 ng/ml TNF')
# plt.title('Sensitivity of pMLKL to varying TNFa doses (WTKD cal)')
# plt.legend([ 'FDKD', 'TDKD', 'A20KD', 'C8KD','WT '] , title = 'KD Conditions', loc='best', fontsize = 8)
plt.legend(['100 ng/ml ', '10 ng/ml', '1 ng/ml', '0.1 ng/ml'] , title = 'TNF FPPF', loc=0, fontsize = 5)
# plt.legend(flipnum, title = 'flip', loc=0, fontsize = 5)
# plt.ylim(ymax = 6000)
# plt.savefig('pMLKL to varying TNFa doses (WTKD cal)')
plt.show()

#
# t = np.array([0., 30,  60,   120,  180, 270,  480,  960, 1440])
#
# data = np.array([0., 0., 0., 0., 0.01*5544, 0.05*5544, 0.5*5544, 0.99*5544, 1.*5544])
# # df.loc[n]['MLKLa_obs'].iloc[:]
# plt.figure()
# for n in range(0,4):
#     plt.plot(tspan / 60, df.loc[0]['MLKLa_obs'].iloc[:], color = 'r', lw=1)
#     plt.plot(tspan / 60, df.loc[1]['MLKLa_obs'].iloc[:], color = 'm', lw=1)
#     plt.plot(tspan / 60, df.loc[2]['MLKLa_obs'].iloc[:], color = 'g', lw=1)
#     plt.plot(tspan / 60, df.loc[3]['MLKLa_obs'].iloc[:], color = 'b', lw=1)
#     # plt.plot(tspan / 60, df.loc[0]['CII_obs'].iloc[:]/df.loc[0]['CII_obs'].iloc[:].max(), color = 'r', lw=1)
#     # plt.plot(tspan / 60, df.loc[1]['CII_obs'].iloc[:]/df.loc[1]['CII_obs'].iloc[:].max(), color = 'm', lw=1)
#     # plt.plot(tspan / 60, df.loc[2]['CII_obs'].iloc[:]/df.loc[2]['CII_obs'].iloc[:].max(), color = 'g', lw=1)
#     # plt.plot(tspan / 60, df.loc[3]['CII_obs'].iloc[:]/df.loc[3]['CII_obs'].iloc[:].max(), color = 'b', lw=1)
#     # plt.plot(tspan / 60, df.loc[0]['CII_k63_obs'].iloc[:]/df.loc[0]['CI_k63_obs'].iloc[:].max(), color = 'r', lw=1)
#     # plt.plot(tspan / 60, df.loc[1]['CII_k63_obs'].iloc[:]/df.loc[1]['CI_k63_obs'].iloc[:].max(), color = 'm', lw=1)
#     # plt.plot(tspan / 60, df.loc[2]['CII_k63_obs'].iloc[:]/df.loc[2]['CI_k63_obs'].iloc[:].max(), color = 'g', lw=1)
#     # plt.plot(tspan / 60, df.loc[3]['CII_obs'].iloc[:]/df.loc[3]['CI_k63_obs'].iloc[:].max(), color = 'b', lw=1)
# plt.scatter(t/60, data, lw = 1.5, color = 'black', zorder = 1)
# plt.xlabel('Time (hours)', fontsize=13)
# plt.ylabel('Phosphorylated MLKL amount (copies/cell)', fontsize=13)
# plt.title('Sensitivity of pMLKL to varying TNFa doses')
# plt.legend(['100 ng/ml ', '10 ng/ml', '1 ng/ml', '0.1 ng/ml'] , title = 'TNF Doses', loc=0, fontsize = 8)
# # plt.savefig('pMLKL under varying TNFa doses')
# plt.show()






# print(render_reactions.run(model))
# # # #
# # # for p in model.parameters:
# # #     print('{},{:e}'.format(p.name,p.value))
# # #
# # #
# #
# # pars = np.load('optimizer_best_5000_all_new_2.npy')
# pars =  np.load('optimizer_best_1000_mar7.npy')
# rate_params = model.parameters_rules() # these are only the parameters involved in the rules
# param_values = np.array([p.value for p in model.parameters]) # these are all the parameters
# rate_mask = np.array([p in rate_params for p in model.parameters])
# param_values[rate_mask] = 10 ** pars
# #
# # #
# # # tspan = np.linspace(0, 1400, 1441)
# # # sim = BngSimulator(model, tspan=tspan)
# # # result = sim.run(method='ode')
# # # #
# # # #
# # # # plt.figure()
# # # # # plt.plot(tspan/60, result.observables['MLKLu'][:])
# # # # plt.plot(tspan/60, result.observables['MLKLa_obs'][:])
# # # # # plt.scatter(x, mlkl)
# # # # plt.xlabel('Time [minutes]', fontsize=16)
# # # # plt.ylabel('Phosphorylated MLKL amount [molecules]', fontsize=16)
# # # # # plt.title('Sensitivity of pMLKL to varying TNFa doses')
# # # # # plt.ylim(ymax = )
# # # # plt.show()
# # # #
# # #
# #
# fdkd = [3109, 933, 3109, 3109, 3109]
# tdkd = [4696, 4696, 1409, 4696, 4696]
# a20kd = [9000, 9000, 9000, 2700, 9000]
# c8kd = [3799,3799, 3799, 3799,1140]
# #
# # tnf = [2326, 232, 23,2]
# color = ['r', 'm', 'g', 'b', 'c']
# color1 = ['r', 'm', 'g', 'b']
# # # lab = ['100 ng/ml', '10 ng/ml', '1 ng/ml', '0.1 ng/ml']
# # #
# tspan = np.linspace(0, 1440, 1441)
# sim = ScipyOdeSimulator(model, tspan=tspan)
# result = sim.run(param_values=param_values,initials= {FADD(bDD=None, bDED1=None, bDED2=None): fdkd, TRADD(brec=None, brip=None, state='um', bDD1 = None, bDD2 = None):tdkd,
#                                                       A20(brip=None): a20kd, C8(bf=None, flip = None, state='I'): c8kd})
# df = result.dataframe
# #
# # tspan = np.linspace(0, 1440, 1441)
# # sim = ScipyOdeSimulator(model, tspan=tspan)
# # result = sim.run(param_values=param_values,initials= {TNF(brec=None): tnf})
# # df = result.dataframe
# # #
# # # # with open('params_cal_kd.txt', 'w') as f:
# # # #     for p, v in zip(model.parameters, result.param_values[0]):
# # # #         f.write('{},{:e}\n'.format(p.name, v))
# # #
# # # x = list([0, 60/60, 120/60, 180/60, 240/60, 300/60, 360/60, 420/60, 480/60, 540/60, 600/60, 660/60, 720/60])
# # # y = [0, 0, 0, 554, 1386, 2772, 4158, 5544, 5544, 5544, 5544, 5544, 5544]
# # #
# # plt.figure()
# # for n in range(0,4):
# #     plt.plot(tspan / 60, df.loc[n]['MLKLa_obs'].iloc[:], c=color[n], lw=1.5)
# # # plt.plot(x, y, lw = 1.5, color = 'black')
# # plt.xlabel('Time (hours)', fontsize=13)
# # plt.ylabel('Phosphorylated MLKL amount (copies/cell)', fontsize=13)
# # plt.title('Sensitivity of pMLKL to varying TNFa doses')
# # plt.legend(['100 ng/ml ', '10 ng/ml', '1 ng/ml', '0.1 ng/ml'] , title = 'TNF Doses', loc=0, fontsize = 8)
# # plt.savefig('pMLKL to varying TNFa doses feb 18')
# # plt.show()
# # quit()
# # #
# # # quit()
# # # mlkl = [0, 170, 900, 4880, 9940, 10000]
# # # x = [0, 60, 120, 240, 360, 480]
# #
# t = np.array([0., 30,  60,   120,  180, 270,  480,  960, 1440])
# data = np.array([0., 0., 0., 0., 0.01*5544, 0.05*5544, 0.5*5544, 0.99*5544, 1.*5544])
# datan = np.array([0., 0., 0., 0., 0.01, 0.05, 0.5, 0.99, 1.])
# plt.figure()
# for n in range(0,5):
#     # plt.plot(tspan, df.loc[n]['MLKLa_obs'].iloc[:], c = color[n],lw =1.5) #fst-pso
#     plt.plot(tspan/60, df.loc[n]['MLKLa_obs'].iloc[:]/df.loc[n]['MLKLa_obs'].iloc[:].max(),  c = color[n],lw = 1.5) #fppf
# plt.scatter(t/60, datan, lw = 2.5, color = 'k',marker = '.', zorder = 1)
# plt.xlabel('Time [hours]', fontsize=14)
# plt.ylabel('Phosphorylated MLKL amount [molecules]', fontsize=14)
# plt.title('Sensitivity of pMLKL to varying KD Conditions 100 ng/ml TNF')
# # plt.title('Sensitivity of pMLKL to varying TNFa doses (WTKD cal)')
# plt.legend([ 'FDKD', 'TDKD', 'A20KD', 'C8KD','WT '] , title = 'KD Conditions', loc='best', fontsize = 8)
# # plt.legend(['100 ng/ml ', '10 ng/ml', '1 ng/ml', '0.1 ng/ml'] , title = 'TNF FPPF', loc=0, fontsize = 5)
# # plt.legend(flipnum, title = 'flip', loc=0, fontsize = 5)
# # plt.ylim(ymax = 6000)
# plt.savefig('pMLKL to varying TNFa doses (WTKD cal)')
# # plt.show()
#
#
# plt.figure()
# for n in range(0,5):
#     # plt.plot(tspan, df.loc[n]['MLKLa_obs'].iloc[:], c = color[n],lw =1.5) #fst-pso
#     plt.plot(tspan/60, df.loc[n]['CI_k63_obs'].iloc[:]/df.loc[n]['CI_k63_obs'].iloc[:].max(), c = color[n],lw = 1.5) #fppf
# # plt.plot(t/60, datan, lw = 1.5, color = 'black',marker = '_', zorder = 1)
# plt.xlabel('Time [hours]', fontsize=14)
# plt.ylabel('Complex I k63 Ub [molecules]', fontsize=14)
# plt.title('Sensitivity of CI to varying KD Conditions 100 ng/ml TNF')
# # plt.title('Sensitivity of CI to varying TNFa doses (WTKD cal)')
# plt.legend(['WT ','FDKD', 'TDKD', 'A20KD', 'C8KD'] , title = 'KD Conditions', loc='best', fontsize = 8)
# # plt.legend(['100 ng/ml ', '10 ng/ml', '1 ng/ml', '0.1 ng/ml'] , title = 'TNF FPPF', loc=0, fontsize = 5)
# # plt.legend(flipnum, title = 'flip', loc=0, fontsize = 5)
# # plt.ylim(ymax = 6000)
# # plt.savefig('CI to varying TNFa doses (WTKD cal)')
# plt.show()
#
# plt.figure()
# for n in range(0,5):
#     # plt.plot(tspan, df.loc[n]['MLKLa_obs'].iloc[:], c = color[n],lw =1.5) #fst-pso
#     plt.plot(tspan/60, df.loc[n]['CII_obs'].iloc[:]/df.loc[n]['CII_obs'].iloc[:].max(), c = color[n],lw = 1.5) #fppf
# # plt.scatter(x, mlkl, color = 'tab:gray', marker = 's')
# plt.xlabel('Time [hours]', fontsize=14)
# plt.ylabel('Complex II [molecules]', fontsize=14)
# plt.title('Sensitivity of CII to varying KD Conditions 100 ng/ml TNF')
# # plt.title('Sensitivity of CII to varying TNFa doses (WTKD cal)')
# plt.legend(['WT ','FDKD', 'TDKD', 'A20KD', 'C8KD'] , title = 'KD Conditions', loc='best', fontsize = 8)
# # plt.legend(['100 ng/ml ', '10 ng/ml', '1 ng/ml', '0.1 ng/ml'] , title = 'TNF FPPF', loc=0, fontsize = 5)
# # plt.legend(flipnum, title = 'flip', loc=0, fontsize = 5)
# # plt.ylim(ymax = 6000)
# # plt.savefig('CII to varying TNFa doses (WTKD cal)')
# plt.show()

