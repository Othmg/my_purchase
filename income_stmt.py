from bookings import Bookings


class IS:
    def __init__(self, revenue:Bookings.inc_acc, expense:Bookings.exp_acc):
        self.revenue = revenue
        self.expense = expense

    def revenue(self)->float:
        return self.revenue.amnt

    def expense(self)->float:
        return self.expense.amnt

    def saving(self)->float:
        return self.revenue.amnt - self.expense.amnt




        





