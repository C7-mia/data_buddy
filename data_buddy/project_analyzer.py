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

def get_min(numbers):
    """Returns the smallest number in the list."""
    if not numbers:
        return 0
    return min(numbers)

def get_max(numbers):
    """Returns the largest number in the list."""
    if not numbers:
        return 0
    return max(numbers)
