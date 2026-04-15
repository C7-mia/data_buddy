import data_buddy

# Let's imagine this is data from a recent project or game
scores = [85, 90, 78, 92, 88]

# Using our custom package!
average_score = data_buddy.get_average(scores)

print(f"The data you provided is: {scores}")
print(f"The calculated average is: {average_score}")
