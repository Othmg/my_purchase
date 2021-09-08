from accounts import ExpAcc,InvAcc,LoanAcc,RevAcc,CashAcc
from validation import ValueValidator,ItemValidator,TimeValidator, RateValidator

class Bookings:
    def __init__(self,revenue, exp_input,item,price,start_capital,time_until_purchase,loan,int_rate,maintenance_rate):

        self.revenue = ValueValidator(revenue).validated
        self.exp_input = ValueValidator(exp_input).validated
        self.item = ItemValidator(item).validated
        self.price = ValueValidator(price).validated
        self.start_capital = ValueValidator(start_capital).validated
        self.time_until_purchase = TimeValidator(time_until_purchase).validated
        self.loan = ValueValidator(loan).validated
        self.int_rate = RateValidator(int_rate).validated
        self.maintenance_rate = RateValidator(maintenance_rate).validated
        self.cash_outflow = self.price-self.loan
    
    def inc_acc(self,time:float)->RevAcc:
        return RevAcc(self.revenue,time,'salary')

    def exp_acc(self,time:float)->ExpAcc:
        cat = 'expense'
        if time < self.time_until_purchase:
                return ExpAcc(self.exp_input,time,cat)

        elif time == self.time_until_purchase:
            amnt = self.exp_input + self.cash_outflow
            return ExpAcc(amnt,time,cat)

        elif time > self.time_until_purchase:
            maint = ExpCalc(time).maintenance(self.price,self.int_rate)
            int = ExpCalc(time).interests(self.loan,self.int_rate)
            amnt = maint.amnt + int.amnt + self.exp_input
            return ExpAcc(amnt,time,cat)

    def inv_acc(self,time:float)->InvAcc:
        cat = 'asset'
        if time < self.time_until_purchase:
            return InvAcc(0,time,cat)

        elif time == self.time_until_purchase:
            return InvAcc(self.price,time,cat)
        
        elif time > self.time_until_purchase:
            return InvAcc(self.price,time,cat)

    def loan_acc(self,time:float)->LoanAcc:
        cat = 'liability'
        if time < self.time_until_purchase:
            return LoanAcc(0,time,cat)
        
        if time == self.time_until_purchase:
            return LoanAcc(self.loan,time,cat)

        if time > self.time_until_purchase:
            return LoanAcc(self.loan,time,cat)
            
    def cash_acc(self,time:float)->CashAcc:
        cat = 'asset'
        res = 0
        for t in range (time+1):
            res += self.inc_acc(t).amnt - self.exp_acc(t).amnt
        amnt = res + self.start_capital
        return CashAcc(amnt,time,cat)

class ExpCalc:
    def __init__(self,time:float):
        self.time = time

    def maintenance(self,price:float,rate:float)->ExpAcc:
        amnt = price * rate
        return ExpAcc(amnt,self.time,'maintenance')
    
    def interests(self,loan_value:float, rate:float)->ExpAcc:
        amnt = loan_value * rate
        return ExpAcc(amnt,self.time,'interests')
