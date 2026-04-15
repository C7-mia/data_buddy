 import data_buddy

# Data set given
scores = [85, 90, 78, 92, 88, 500]

# All functions working together on the SAME data:
avg = data_buddy.get_average(scores)
med = data_buddy.get_median(scores)
low = data_buddy.get_min(scores)
hi  = data_buddy.get_max(scores)

print(f"Data: {scores}")
print("-" * 30)
print(f"Average: {avg:.2f}") # Still works!
print(f"Median:  {med}")      # Still works!
print(f"Minimum: {low}")      # New!
print(f"Maximum: {hi}")       # New!



