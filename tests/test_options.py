import torch

from torch_finance.markets.options import BinomialEuropeanOption

def test_european_option():
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