from dataclasses import asdict
from bookings import Bookings
from optimizer import Optimized
import json 
from datetime import datetime

### to build: checks + optimizer output ####
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


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

assert diff_month(datetime(2010,10,1), datetime(2010,9,1)) == 1

revenue, exp_input,item,price,start_capital,time_until_purchase,loan,int_rate,maintenance_rate = input_dict.values()

book = Bookings(revenue, exp_input,item,price,start_capital,time_until_purchase,loan,int_rate,maintenance_rate)

time = 3
income = book.inc_acc(time)
expense = book.exp_acc(time)

#in json
output_json ={ 
  "income": book.inc_acc(time).amnt, 
  "expense": book.exp_acc(time).amnt, 
  "capital": book.cash_acc(time).amnt
} 
      
# Serializing json  
json_object = json.dumps(output_json, indent = 4) 
print(json_object)

"""
The Optimized function returns optimised expense level, time_until_purchase and purchase price
as well as the gap with the user input.
use 0 as default time values
"""
opt = Optimized(book.inc_acc(0),book.exp_acc(0),start_capital,price,time_until_purchase)
#exemple
# print(opt._expense())
# print(opt._expense_gap())
# print(opt._expense_gap_pct())

gap_list = [opt._expense_gap_pct(),opt._time_until_purchase_gap_pct(),opt._purchase_gap_pct()]
gap_list = sorted(gap_list)
print(gap_list)

##TODO have json output for optimised including new values ordered by pct change?





