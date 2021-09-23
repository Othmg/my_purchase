from bookings import Bookings
from accounts import RevAcc, ExpAcc,InvAcc
import json
from validation import ValueValidator
from decorators import non_neg



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
    
    @property
    def opt_expense(self)->float:
        val = ((self.start_capital-self.purchase)/self.time_until_purchase) + self.revenue
        return val

    @property
    def opt_time_until_purchase(self)->float:
        val = (self.purchase-self.start_capital)/(self.revenue - self.expense)
        if val < 0:
            val = 0
        return val
        
    @property
    def opt_purchase_price(self)->float:
        val = self.start_capital + self.time_until_purchase*(self.revenue - self.expense)
        return ValueValidator(val).validated 


class OptGap(Optimized):
    def __init__(self, revenue: RevAcc, expense: ExpAcc, start_capital: float, purchase: float, loan: float, time_until_purchase: float):
        super().__init__(revenue, expense, start_capital, purchase, loan, time_until_purchase)

    def _gap(self,opt,usr)->float:
        return opt-usr

    def _gap_pct(self,opt_gap,usr_gap):
        return opt_gap / usr_gap

    @property
    def expense_gap(self)->float:
        return self._gap(self.opt_expense,self.expense)

    @property
    def time_until_purchase_gap(self)->float:
        return self._gap(self.opt_time_until_purchase,self.time_until_purchase)

    @property
    def purchase_gap(self)->float:
        return (self._gap(self.opt_purchase_price,self.purchase))

    @property
    def expense_gap_pct(self):
        return self._gap_pct(self.expense_gap,self.expense)

    @property
    def time_until_purchase_gap_pct(self):
        return self._gap_pct(self.time_until_purchase_gap,self.time_until_purchase)

    @property
    def purchase_gap_pct(self):
        return self._gap_pct(self.purchase_gap,self.purchase)
        

class OptJson(OptGap):
    def __init__(self, revenue: RevAcc, expense: ExpAcc, start_capital: float, purchase: float, loan: float, time_until_purchase: float):
        super().__init__(revenue, expense, start_capital, purchase, loan, time_until_purchase)

    def is_optimist(self)-> bool:
        if self.expense_gap < 0:
            return True
        return False

    def exp_validator(self,exp):
        if exp < 0:
            return 'NaN'
        else:
            return exp

    def _sorted(self)->dict:
        self.time = 0
        pct_gap_dict = {'expense':self.expense_gap_pct,'time_until_purchase':self.time_until_purchase_gap_pct,'price':self.purchase_gap_pct}
        return dict(sorted(pct_gap_dict.items(), key=lambda item: item[1]))

    def _sorted_keys(self):
        """
        returns a dict of expense gap, time_until_purchase gap and price gap sorted on their gap in pct.
        sorted dict returns largest gap first when the user was pessimistic (the logic behind is that the user would happily change the largest value in his favor)
        sorted dict returns smallest gap first when user was optimistic (the logic behing is that this is the least painful change)
        """
        sorted = self._sorted()
        k1,k2,k3 = sorted.keys()
        return k1,k2,k3

    def _sorted_gap_dict(self)-> dict:

        k1,k2,k3 = self._sorted_keys()

        gap_values_dict = {'expense':self.expense_gap,'time_until_purchase':self.time_until_purchase_gap,'price':self.purchase_gap}

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
 
    def _sorted_val_dict(self)-> dict:

        k1,k2,k3 = self._sorted_keys()
        values_dict = {'expense':self.exp_validator(self.opt_expense),'time_until_purchase':self.opt_time_until_purchase,'price':self.opt_purchase_price}

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

    def _sorted_json(self,sorted:dict):
        k1,k2,k3 = sorted.keys()
        output_json ={ 
        k1:sorted[k1],
        k2:sorted[k2],
        k3:sorted[k3]
        } 
        # Serializing json  
        json_object = json.dumps(output_json, indent = 4) 
        return json_object

    @property
    def get_sorted_gap(self):
        dct = self._sorted_gap_dict()
        return self._sorted_json(dct)

    @property
    def get_sorted_val(self):
        dct = self._sorted_val_dict()
        return self._sorted_json(dct)


