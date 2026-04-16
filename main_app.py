import data_buddy

# The user 'uploads' or points to their file
filename = "expenses.csv"

# 1. Show them the quick business report
data_buddy.run_no_code_analysis(filename)

# 2. Generate the professional notebook code for them
data_buddy.generate_notebook_code(filename)
