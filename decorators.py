

def non_neg(func):
    def wrapper_non_neg(*args):
        if func(*args) < 0:
            return 'NaN'
        else:
            return func(*args)
    return wrapper_non_neg
    
    
        

