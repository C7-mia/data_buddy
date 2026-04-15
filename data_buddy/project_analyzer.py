def get_average(numbers): 
    """Calculates the average of a list of numbers.""" 
    if not numbers: 
        return 0 
 
    total = sum(numbers) 
    count = len(numbers) 
    return total / count 
