import torch

import scipy.optimize as optimize

class ZeroCouponBond:
    
    def __init__(self,
                face_value: torch.tensor,
                annual_yield: torch.tensor,
                time_to_maturity: torch.tensor):
        """
        :param face_value: face values of the bonds.
        :param annual_yield: annual yields or rates of the bonds.
        :param time_to_maturity: time to maturities of the bonds, in years.
        
        """
        
        self.face_value = face_value
        self.annual_yield = annual_yield
        self.time_to_maturity = time_to_maturity
        
    def price(self):
        
        """
        Calculates the values of all the Zero Coupon Bond 

        :returns A tensor of prices of the zero coupon bonds
        """
        return self.face_value/((1+self.annual_yield)**self.time_to_maturity)

    
class Bond:
    
    def __init__(self,
                 face_value: torch.tensor,
                 time_to_maturity: torch.tensor,
                 yield_to_maturity: torch.tensor,
                 coupon_value: torch.tensor,
                 frequency: torch.tensor):
        """
        :param face_value: face values of the bonds.
        :param time_to_maturity: time to maturities of the bonds, in years.
        :param yield_to_maturity: yield to maturity of the bonds.
        :param coupon_value: Value of coupon payments of the bonds.
        :param frequency: frequency of payments.
        
        """
        
        self.face_value = face_value
        self.time_to_maturity = time_to_maturity
        self.yield_to_maturity = yield_to_maturity
        self.coupon_value = coupon_value
        self.frequency = frequency
    
    def price(self):
        
        """
        Calculates the values of all the Bonds

        :returns A tensor of prices of the bonds.
        """
        
        periods = self.time_to_maturity*2
        coupon = self.coupon_value/100.*self.face_value
        prices = []
        
        for bond in range(len(self.face_value)):
            
            dt = [(i+1)/self.frequency[bond] for i in range(int(periods[bond]))]
            coupon_price = sum([coupon[bond]/self.frequency[bond]/ \
                                (1+self.yield_to_maturity[bond]/self.frequency[bond])\
                                **(self.frequency[bond]*t) for t in dt])
            
            face_value_price = self.face_value[bond]/(1+self.yield_to_maturity[bond]/self.frequency[bond]) \
                                **(self.frequency[bond]*self.time_to_maturity[bond])
            prices.append(coupon_price + face_value_price)
            
        return torch.tensor(prices) 
    
    
if __name__ == '__main__':

    face_value = torch.tensor([100, 200])
    annual_yield = torch.tensor([0.05, 0.1])
    time_to_maturity = torch.tensor([5, 8])

    zero_coupon_bonds = ZeroCouponBond(face_value = face_value, 
                                       annual_yield = annual_yield, 
                                       time_to_maturity = time_to_maturity)
     
    face_value = torch.tensor([100, 200])
    time_to_maturity = torch.tensor([1.5, 2.0])
    yield_to_maturity = torch.tensor([0.01, 0.02])
    coupon_value = torch.tensor([5.75, 10])
    frequency = torch.tensor([2, 4])

    bonds = Bond(face_value, time_to_maturity, yield_to_maturity, coupon_value, frequency)

    assert zero_coupon_bonds.price().tolist() == [78.3526382446289, 93.30146026611328]
    assert bonds.price().tolist() == [107.0543441772461, 211.92953491210938]

    
    
