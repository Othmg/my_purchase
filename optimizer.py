from bookings import Bookings
from accounts import RevAcc, ExpAcc,InvAcc
import json
from validation import ValueValidator


class Optimized:
    """
    Returns:
    - optimal value while keeping other user inputs constant (pre-purchase)
    - gap with user input (as opt - user)
    - gap in pct (optimal / user_input)
    """
    def __init__(self,revenue:RevAcc, expense:ExpAcc, start_capital:float, purchase:float,loan:float,time_until_purchase:float):
        self.revenue = revenue.amnt
        self.expense = expense.amnt
        self.start_capital = start_capital
        #purchase is the actual cash outflow (price - loan)
        self.purchase = purchase - loan
        self.time_until_purchase = time_until_purchase
    
    def _expense(self)->float:
        val = ((self.start_capital-self.purchase)/self.time_until_purchase) + self.revenue
        return ValueValidator(val).validated 

    def _time_until_purchase(self)->float:
        val = (self.purchase-self.start_capital)/(self.revenue - self.expense)
        if val < 0:
            val = 0
        return val
        
    def _purchase_price(self)->float:
        val = self.start_capital + self.time_until_purchase*(self.revenue - self.expense)
        return ValueValidator(val).validated 

    def _expense_gap(self)->float:
        opt = self._expense()
        usr = self.expense
        return opt - usr

    def _time_until_purchase_gap(self)->float:
        opt = self._time_until_purchase()
        usr = self.time_until_purchase
        return opt - usr

    def _purchase_gap(self)->float:
        opt = self._purchase_price()
        usr = self.purchase
        return opt - usr

    def _expense_gap_pct(self):
        return self._expense_gap() / self.expense

    def _time_until_purchase_gap_pct(self):
        return self._time_until_purchase_gap() / self.time_until_purchase

    def _purchase_gap_pct(self):
        return self._purchase_gap() / self.purchase

    def is_optimist(self)-> bool:
        if self._expense_gap() < 0:
            return True
        return False

    def _sorted(self)-> dict:
        self.time = 0
        pct_gap_dict = {'expense':self._expense_gap_pct(),'time_until_purchase':self._time_until_purchase_gap_pct(),'price':self._purchase_gap_pct()}
        return dict(sorted(pct_gap_dict.items(), key=lambda item: item[1]))

    def sorted_keys(self)-> dict:
        """
        returns a dict of expense gap, time_until_purchase gap and price gap sorted on their gap in pct.
        sorted dict returns largest gap first when the user was pessimistic (the logic behind is that the user would happily change the largest value in his favor)
        sorted dict returns smallest gap first when user was optimistic (the logic behing is that this is the least painful change)
        """
        sorted = self._sorted()
        k1,k2,k3 = sorted.keys()
        return k1,k2,k3

    def sorted_gap_dict(self)-> dict:

        k1,k2,k3 = self.sorted_keys()
        gap_values_dict = {'expense':self._expense_gap(),'time_until_purchase':self._time_until_purchase_gap(),'price':self._purchase_gap()}

        if self.is_optimist() == True:
            sorted_gap_val_dict = {
                k1:gap_values_dict[k1],
                k2:gap_values_dict[k2],
                k3:gap_values_dict[k3]}
        else:
            sorted_gap_val_dict = {
                k3:gap_values_dict[k3],
                k2:gap_values_dict[k2],
                k1:gap_values_dict[k1]}
        return sorted_gap_val_dict

    def sorted_val_dict(self)-> dict:

        k1,k2,k3 = self.sorted_keys()
        values_dict = {'expense':self._expense(),'time_until_purchase':self._time_until_purchase(),'price':self._purchase_price()}

        if self.is_optimist() == True:
            sorted_gap_val_dict = {
                k1:values_dict[k1],
                k2:values_dict[k2],
                k3:values_dict[k3]}
        else:
            sorted_gap_val_dict = {
                k3:values_dict[k3],
                k2:values_dict[k2],
                k1:values_dict[k1]}
        return sorted_gap_val_dict


    def sorted_json(self,sorted:dict):
        k1,k2,k3 = sorted.keys()
        output_json ={ 
        k1:sorted[k1],
        k2:sorted[k2],
        k3:sorted[k3]
        } 
        # Serializing json  
        json_object = json.dumps(output_json, indent = 4) 
        return json_object

    def get_sorted_gap(self):
        dct = self.sorted_gap_dict()
        return self.sorted_json(dct)

    def get_sorted_val(self):
        dct = self.sorted_val_dict()
        return self.sorted_json(dct)

    




