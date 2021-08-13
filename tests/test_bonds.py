import torch

from torch_finance.markets.bonds import ZeroCouponBond

def test_zero_coupn_bond():
    face_value = torch.tensor([100, 200])
    annual_yield = torch.tensor([0.05, 0.1])
    time_to_maturity = torch.tensor([5, 8])

    zero_coupon_bonds = ZeroCouponBond(face_value = face_value, 
                       annual_yield = annual_yield, 
                       time_to_maturity = time_to_maturity)

    assert zero_coupon_bonds.price().tolist() == [78.3526382446289, 93.30146026611328]