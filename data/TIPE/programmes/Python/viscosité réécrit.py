## This python code is based on the MatLab code orginaly provided by Chris Westbrook
## http://www.met.reading.ac.uk/~sws04cdw/viscosity_calc.html

import numpy
import math

def visco(T, Veau, Vgly):
    #Densité
    DensGly = (1273.3-0.6121*T)/1000 			#densité volumique glycérol (g/cm3) (1 g/cm3 = 1000 kg/m3)
    DensEau = (1-math.pow(((abs(T-4))/622),1.7)) 	#densité of water (g/cm3) (1 g/cm3 = 1000 kg/m3)

    #fraction
    MasseGly = DensGly*Vgly
    MasseEau = DensEau*Veau
    MasseTot = MasseGly + MasseEau
    FractionMasse = MasseGly/MasseTot
    FractionVol = Vgly/(Vgly+Veau)

    print ("Fraction molaire de Glycérol dans le mélange =", round(FractionMasse,5))
    print ("Fraction volumique de Glycérol dans le mélange =", round(FractionVol,5))

    #masse volumique mélange

    contraction_av = 1-math.pow(3.520E-8*((FractionMasse*100)),3)+math.pow(1.027E-6*((FractionMasse*100)),2)+2.5E-4*(FractionMasse*100)-1.691E-4
    contraction = 1+contraction_av/100

    density_mix=(DensGly*FractionVol+DensEau*(1-FractionVol))*contraction*1000

    print ("Masse volumique =",round(density_mix,5),"kg/m3")

    #viscosité
    ViscoGly = 0.001*12100*numpy.exp((-1233+T)*T/(9900+70*T))
    ViscoEau = 0.001*1.790*numpy.exp((-1230-T)*T/(36100+360*T))

    a=0.705-0.0017*T
    b=(4.9+0.036*T)*numpy.power(a,2.5)
    alpha=1-FractionMasse+(a*b*FractionMasse*(1-FractionMasse))/(a*FractionMasse+b*(1-FractionMasse))
    A=numpy.log(ViscoEau/ViscoGly)

    ViscoMelange = ViscoGly*numpy.exp(A*alpha)

    print ("Viscosité du mélange =",round(ViscoMelange,5), "Pa.s | Pl")

"""
visco(25, 0.150, 0.100)
Fraction molaire de Glycérol dans le mélange = 0.45691
Fraction volumique de Glycérol dans le mélange = 0.4
Masse volumique = 1112.44595 kg/m3
Viscosité du mélange = 0.00405 Pa.s | Pl
"""
