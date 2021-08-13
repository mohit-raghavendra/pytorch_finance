import math
import numpy as np
from decimal import Decimal
import torch

class BinomialStockOption(object):
	def __init__(self, 
				initial_price: torch.tensor, 
				strike_price: torch.tensor, 
				r: torch.tensor,
				is_put: torch.tensor,
				time_to_maturity: int, 
				no_timesteps: int, 
				prob_up: torch.tensor, 
				prob_down: torch.tensor, 
				dividiend_yield: float = 0):

		"""
		Initialize the stock option base class.
		"""
		self.initial_price = initial_price
		self.strike_price = strike_price
		self.r = r
		self.time_to_maturity = time_to_maturity
		self.no_timesteps = max(1, no_timesteps)
		self.STs = [] # Declare the stock prices tree
		
		""" Optional parameters used by derived classes """
		self.prob_up, self.prob_down = prob_up, prob_down
		self.dividiend_yield = dividiend_yield
		self.is_call = ~is_put
		
	@property
	def dt(self):
		"""
		:return Single time step, in years
		"""
		return self.time_to_maturity/self.no_timesteps

	@property
	def df(self):
		""" 
		:return The discount factor 
		"""
		return torch.exp(-(self.r-self.dividiend_yield)*self.dt)

class BinomialEuropeanOption(BinomialStockOption):


	def __init__(self, 
				initial_price: torch.tensor, 
				strike_price: torch.tensor, 
				r: torch.tensor, 
				is_put: torch.tensor,
				time_to_maturity: int, 
				no_timesteps: int, 
				prob_up: torch.tensor, 
				prob_down: torch.tensor, 
				dividiend_yield: float = 0):

		"""
		:param initial_price: initial price of each option in the batch
		:param strike_price: strike price of each option in the batch
		:param r: risk-free interest rate
		:param is_put: True for a put option, False for a call option (of each option in the batch)
		:param time_to_maturity: time to maturity 
		:param no_timesteps: number of time steps
		:param prob_up: probability at up state 
		:param prob_down: probability at down state
		:param dividiend_yield: Dividend yield
		"""

		super(BinomialEuropeanOption, self).__init__(initial_price=initial_price, 
													strike_price=strike_price, 
													r=r, 
													is_put=is_put,
													time_to_maturity=time_to_maturity, 
													no_timesteps=no_timesteps, 
													prob_up=prob_up, 
													prob_down=prob_down, 
													dividiend_yield=dividiend_yield)

	def price(self):

		""" 
		Entry point of the pricing implementation

		:return tensor or option prices
		"""

		self.M = self.no_timesteps+1 # Number of terminal nodes of tree
		self.u = 1+self.prob_up # Expected value in the up state
		self.d = 1-self.prob_down # Expected value in the down state
		self.qu = (torch.exp((self.r-self.dividiend_yield)*self.dt)-self.d)/(self.u-self.d)
		self.qd = 1-self.qu

		self.__init_stock_price_tree()
		payoffs = self.__traverse_tree()
		return payoffs[:, 0]

	def __init_stock_price_tree(self):
		# Initialize terminal price nodes to zeros
		self.STs = torch.zeros(self.initial_price.size(0), self.M)
		for i in range(self.M):
			self.STs[:, i] = self.initial_price * (self.u**(self.no_timesteps-i)) * (self.d**i)

	def __traverse_tree(self):
		#Traverse the binomial tree
		
		strike = self.strike_price.clone()
		multiplier = self.is_call * 1
		multiplier[multiplier == 0] = -1
		multiplier = multiplier.unsqueeze(-1).expand(-1, self.STs.size(-1))
		
		payoffs = (self.STs - strike.unsqueeze(-1).expand(-1, self.STs.size(-1)))
		payoffs = payoffs * multiplier
		payoffs = torch.maximum(torch.zeros_like(payoffs), payoffs)

		for i in range(self.no_timesteps):
			payoffs = (payoffs[:, :-1]*self.qu + payoffs[:, 1:]*self.qd)*self.df

		return payoffs

if __name__ == '__main__':
	
	initial_price=torch.tensor([50, 50])
	strike_price=torch.tensor([52, 52])
	r=torch.tensor([0.05, 0.05])
	prob_up=torch.tensor([0.2, 0.2])
	prob_down=torch.tensor([0.2, 0.2]) 
	is_put=torch.tensor([True, False])

	time_to_maturity=2
	no_timesteps=2
	
	eu_option = BinomialEuropeanOption(initial_price=initial_price, 
								   strike_price=strike_price, 
								   r=r, 
								   is_put=is_put,
								   time_to_maturity=time_to_maturity, 
								   no_timesteps=no_timesteps, 
								   prob_up=prob_up, 
								   prob_down=prob_down)

	assert eu_option.price().tolist() == [4.192653179168701, 7.141105651855469]
		