from . import *
#from .. import Waveguide
import numpy as np



def dispersion(model,lmbda1,lmbda2,**kwargs):
	p = kwargs
	if "point" not in p.keys():
		p["point"] = 100
	else:
		if type(p["point"]) != int:
			raise ValueError("The number of point to use have to be an integer")

	lmbda = np.linspace(lmbda1,lmbda2,p["point"])

	if type(model) == types.FunctionType or (str(type(model)) == "<class 'method'>"):
		n = np.zeros(len(lmbda), dtype = object)
		if type(model(lmbda[0])) == list:
			"""In this case n will be an array of n list with each list representing a mode for all the wavelength """
			n_i = [model(i) for i in lmbda]

			z = np.zeros(len(n_i), dtype = int)

			for i in range(len(n_i)):
				z[i] = int(len(n_i[i]))

			n = np.zeros(max(z), dtype = list)
			for i in range(len(n)):
				n[i] = []

			for i in range(len(n_i)):
				while len(n_i[i]) < max(z):
					n_i[i].append(0)
				for j in range(max(z)):
					n[j].append(n_i[i][j])
		else:
			for i in range(len(lmbda)):
				n[i] = model(lmbda[i])
	elif (str(type(model)) == "<class 'awg.material.Material.Material'>") or (str(type(model)) == "<class 'awg.Waveguide.Waveguide'>"):
		n = np.zeros(np.shape(lmbda))
		for i in range(len(lmbda)):
			n[i] = model.index(lmbda[i])
	else:
		raise ValueError("Wrong model provided")
	return n, lmbda

