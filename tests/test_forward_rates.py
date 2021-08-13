import torch

from torch_finance.markets.forward_rates import ForwardRates

def test_forward_rates():

	periods = torch.tensor([0.25, 0.50, 1.00, 2.00, 1.50,])
	spot_rates = torch.tensor([10.127, 10.469, 10.536, 10.808, 10.681])

	fr = ForwardRates(periods, spot_rates)
	assert fr.get_forward_rates().tolist() == [10.810999870300293, 10.60300064086914, 10.970998764038086, 11.18899917602539]