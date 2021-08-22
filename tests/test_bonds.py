import torch

from torch_finance.markets.bonds import Bond, ZeroCouponBond

def test_bonds():
    
    face_value = torch.tensor([100, 200])
    time_to_maturity = torch.tensor([1.5, 2.0])
    yield_to_maturity = torch.tensor([0.01, 0.02])
    coupon_value = torch.tensor([5.75, 10])
    frequency = torch.tensor([2, 4])

    bonds = Bond(face_value=face_value,
                 time_to_maturity=time_to_maturity,
                 yield_to_maturity=yield_to_maturity,
                 coupon_value=coupon_value,
                 frequency=frequency)

    assert bonds.price().tolist() == [107.0543441772461, 211.92953491210938]
    
def test_zero_coupn_bond():
    
    face_value = torch.tensor([100, 200])
    annual_yield = torch.tensor([0.05, 0.1])
    time_to_maturity = torch.tensor([5, 8])

    zero_coupon_bonds = ZeroCouponBond(face_value = face_value, 
                       annual_yield = annual_yield, 
                       time_to_maturity = time_to_maturity)

    assert zero_coupon_bonds.price().tolist() == [78.3526382446289, 93.30146026611328]
    
