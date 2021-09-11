from dataclasses import asdict
from bookings import Bookings
from optimizer import Optimized
import json 
from datetime import datetime

"""
Values in input dict should all be float (exception for item as string) and no negative values, rates should be <1
- int_rate: only cost of debt, does not include repayment of capital
- maintenance_rate: can be a constant value, is a percentage of purchase price
"""

input_dict = {
            'revenue':10000.0,
            'exp_input':3000.0,
            'item':'car',
            'price':30000.0,
            'start_capital':20000.0,
            'time_until_purchase':6.0,
            'loan':10000.0,
            'int_rate':0.1,
            'maintenance_rate':0.1
            }

"""
All values are passed into the Bookings class which takes care of the accounting manipulation
the methods to retrieve the dicts required a time input. 
- income: method inc_acc
- expense : method exp_acc
- purchase: method inv_acc
- capital: method cash_acc
returns a dictionary type amount,time,category. if you need just the amount you can use .amnt
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

  def ranked_json(self):
    ranked_time = 0
    opt = Optimized(self.book.inc_acc(ranked_time), self.book.exp_acc(ranked_time), self.book.cash_acc(ranked_time).amnt,self.price, self.loan,self.time_until_purchase)
    return opt.sorted_dict_json()


out_1 = output(input_dict,1)
print(out_1.ranked_json())
##TODO if stmt: if user too pessimistic, optimal values should be sorted by largest change first, if user is pessimistic then smallest change first






def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

assert diff_month(datetime(2010,10,1), datetime(2010,9,1)) == 1









