from dataclasses import asdict
from bookings import Bookings
from optimizer import Optimized, OptJson
import json 


"""
Values in input dict should all be float (exception for item as string) and no negative values, rates should be <1
- int_rate: only cost of debt, does not include repayment of capital
- maintenance_rate: can be a constant value, is a percentage of purchase price
"""

input_dict = {
            'revenue':4500.0,
            'exp_input':1000.0,
            'item':'house',
            'price':40000.0,
            'start_capital':9000.0,
            'time_until_purchase':6.0,
            'loan':10000.0,
            'int_rate':0.1,
            'maintenance_rate':0.1
            }

input_dict_4 = {
            'revenue':2999,
            'exp_input':1000,
            'item':'car',
            'price':45000,
            'start_capital':4500,
            'time_until_purchase':11,
            'loan':0.1,
            'int_rate':0.1,
            'maintenance_rate':0.1
            }

input_dict_2 = {
            'revenue':10000.0,
            'exp_input':9000.0,
            'item':'car',
            'price':30000.0,
            'start_capital':0.0,
            'time_until_purchase':6.0,
            'loan':0.0,
            'int_rate':0.0,
            'maintenance_rate':0.0
            }

input_dict_3 = {
            'revenue':5000.0,
            'exp_input':3000.0,
            'item':'car',
            'price':30000.0,
            'start_capital':0.0,
            'time_until_purchase':6.0,
            'loan':0.0,
            'int_rate':0.0,
            'maintenance_rate':0.0
            }


"""
use output class for json outputs of user inputs, ranked gap and ranked values
"""

class output:
  def __init__(self, input_dict: dict, time:float) -> None:
      self.input_dict = input_dict
      self.revenue, self.exp_input,self.item,self.price,self.start_capital,self.time_until_purchase,self.loan,self.int_rate,self.maintenance_rate = self.input_dict.values()

      self.book = Bookings(self.revenue, self.exp_input,self.item,self.price,self.start_capital,self.time_until_purchase,self.loan,self.int_rate,self.maintenance_rate)
      self.time = time

  def basic_json(self):
    output_json ={ 
    "income": self.book.inc_acc(self.time).amnt, 
    "expense": self.book.exp_acc(self.time).amnt, 
    "capital": self.book.cash_acc(self.time).amnt
    } 
        
    # Serializing json  
    return json.dumps(output_json, indent = 4) 

  def ranked_gap_json(self):
    ranked_time = 0
    opt = Optimized(self.book.inc_acc(ranked_time), self.book.exp_acc(ranked_time), self.book.cash_acc(ranked_time).amnt,self.price, self.loan,self.time_until_purchase)
    return opt.get_sorted_gap()

  def ranked_val_json(self):
    ranked_time = 0
    opt = OptJson(self.book.inc_acc(ranked_time), self.book.exp_acc(ranked_time), self.book.cash_acc(ranked_time).amnt,self.price, self.loan,self.time_until_purchase)
    return opt.get_sorted_val

    

out_1 = output(input_dict_4,1)
print(out_1.ranked_val_json())


