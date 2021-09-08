from accounts import RevAcc, ExpAcc,InvAcc

class Optimized:
    """
    Returns:
    - optimal value while keeping other user inputs constant (pre-purchase)
    - gap with user input (as opt - user)
    - gap in pct (optimal / user_input)
    """
    def __init__(self,revenue:RevAcc, expense:ExpAcc, start_capital:float, purchase:float,time_until_purchase:float):
        self.revenue = revenue.amnt
        self.expense = expense.amnt
        self.start_capital = start_capital
        self.purchase = purchase
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





