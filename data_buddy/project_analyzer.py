def get_average(numbers): 
    """Calculates the average of a list of numbers.""" 
    if not numbers: 
        return 0 
 
    total = sum(numbers) 
    count = len(numbers) 
    return total / count 

import statistics

def get_average(numbers):
    """Calculates the average of a list of numbers."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def get_median(numbers):
    """Calculates the median (the middle value) of a list of numbers."""
    if not numbers:
        return 0
    return statistics.median(numbers)

