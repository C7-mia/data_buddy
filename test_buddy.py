import data_buddy

# Real-world scenario: Most scores are around 80-90, but one is 500 (outlier)
scores = [85, 90, 78, 92, 88, 500]

# Backward Compatibility check: Old function still works!
average_score = data_buddy.get_average(scores)

# New Feature check:
median_score = data_buddy.get_median(scores)

print(f"Data: {scores}")
print(f"The Average (Mean): {average_score:.2f}")
print(f"The Median (Middle): {median_score}")

