import numpy as np
from scipy.stats import norm


class GARCH:
	'''
	This class defines the GARCH model object which contains, functions
	for estimation and VaR forecasting.
	'''

	def __init__(self, theta=None, mu=None):

		# Initialize parameters
		if(theta != None):
			self.theta = np.array(theta)
		else:	
			self.theta = np.array([1.1822267318573038e-06,0.088,0.86])
		if(mu == None):
			self.mu=0
		else:
			self.mu=mu

		self.omega = self.theta[0] 
		self.alpha = self.theta[1]
		self.beta = self.theta[2]

	def __repr__(self):
		'''
		Function defining what to print when print(model) is called
		on a instance of the model object.
		'''
		return "omega = %s\nalpha = %s\nbeta  = %s" % ( round(self.omega,8),
														round(self.alpha,3),
														round(self.beta,3) )

	def log_likelihood(self, gamma, y, fmin=False):
		'''
		Takes the reparametrized 3X1 numpy array gamma = log((omega,alpha,beta))
		as input (if given or else uses the ones in self namespace).
		And returns either sum of all likelihood contributions that is a 1X1
		numpy array or both the likelihood and the (t_max,) numpy array of estimated conditional variances.
		'''
		self.theta = np.exp(gamma)
		self.omega = self.theta[0]
		self.alpha = self.theta[1]
		self.beta  = self.theta[2]

		t_max = len(y)
		avg_log_like = 0
		sigma2 = np.zeros(t_max+1)
		sigma2[0] = np.var(y)
		for t in range(1, t_max):
			sigma2[t] =  self.omega + self.alpha*y[t-1]**2 + self.beta*sigma2[t-1]
			avg_log_like += (1/2 * (np.log(sigma2[t]) + (y[t]**2)/sigma2[t]))/t_max
		if fmin:
			return avg_log_like
		else:
			return [avg_log_like, sigma2[0:t_max]]

	def VaR(self, y, pct=(0.01, 0.025, 0.05)):
		est_variance = self.log_likelihood(y=y, fmin=False)[1]
		VaR = {}
		for alpha in pct:
			VaR[str(alpha)] = self.mu + norm.ppf(alpha) * np.sqrt(est_variance)
		return VaR
