from bookings import Bookings
from accounts import RevAcc, ExpAcc,InvAcc
import json

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
        return ((self.start_capital-self.purchase)/self.time_until_purchase) + self.revenue

    def _time_until_purchase(self)->float:
        return (self.purchase-self.start_capital)/(self.revenue - self.expense)
        
    def _purchase_price(self)->float:
        return self.start_capital + self.time_until_purchase*(self.revenue - self.expense)

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

    def sorted_dict(self):
        """
        returns a dict of expense gap, time_until_purchase gap and price gap sorted on their gap in pct.
        time is set 0 per default
        """
        self.time = 0
        pct_gap_dict = {'expense gap':self._expense_gap_pct(),'time_until_purchase gap':self._time_until_purchase_gap_pct(),'price gap':self._purchase_gap_pct()}
        sorted_gap_pct = dict(sorted(pct_gap_dict.items(), key=lambda item: item[1]))
        val_gap_dict = {'expense gap':self._expense_gap(),'time_until_purchase gap':self._time_until_purchase_gap(),'price gap':self._purchase_gap()}
        k1,k2,k3 = sorted_gap_pct.keys()
        sorted_gap_val_dict = {
            k1:val_gap_dict[k1],
            k2:val_gap_dict[k2],
            k3:val_gap_dict[k3]}
        return sorted_gap_val_dict

    def sorted_dict_json(self):
        sort_dict = self.sorted_dict()
        k1,k2,k3 = sort_dict.keys()
        output_json ={ 
        k1:sort_dict[k1],
        k2:sort_dict[k2],
        k3:sort_dict[k3]
        } 
            
        # Serializing json  
        json_object = json.dumps(output_json, indent = 4) 
        return json_object




