import torch

class ForwardRates(object):
    
    def __init__(self, periods, spot_rates):
        
        periods, indices = torch.sort(periods)
        spot_rates = spot_rates[indices]
        self.spot_rates = dict(zip(periods.tolist(), spot_rates.tolist()))
        self.forward_rates = []
                
    def get_forward_rates(self):
        
        times = sorted(self.spot_rates.keys())
        
        for T1, T2 in zip(times, times[1:]):
            R1 = self.spot_rates[T1]
            R2 = self.spot_rates[T2]
            forward_rate = (R2*T2-R1*T1)/(T2-T1)
            self.forward_rates.append(forward_rate)
        
        return torch.tensor(self.forward_rates)


if __name__ == '__main__':
	
	periods = torch.tensor([0.25, 0.50, 1.00, 2.00, 1.50,])
	spot_rates = torch.tensor([10.127, 10.469, 10.536, 10.808, 10.681])

	fr = ForwardRates(periods, spot_rates)
	assert fr.get_forward_rates().tolist() == [10.810999870300293, 10.60300064086914, 10.970998764038086, 11.18899917602539]