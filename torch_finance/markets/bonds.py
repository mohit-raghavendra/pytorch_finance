import torch

class ZeroCouponBond:
    
    def __init__(self,
                face_value: torch.tensor,
                annual_yield: torch.tensor,
                time_to_maturity: torch.tensor):
        """
        :param face_value: face value of the bond.
        :param annual_yield: annual yield or rate of the bond.
        :param time_to_maturity: time to maturity, in years.
        
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


if __name__ == '__main__':

    face_value = torch.tensor([100, 200])
    annual_yield = torch.tensor([0.05, 0.1])
    time_to_maturity = torch.tensor([5, 8])

    zero_coupon_bonds = ZeroCouponBond(face_value = face_value, 
                       annual_yield = annual_yield, 
                       time_to_maturity = time_to_maturity)
 
    assert zero_coupon_bonds.price().tolist() == [78.3526382446289, 93.30146026611328]

