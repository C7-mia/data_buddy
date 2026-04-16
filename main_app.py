import data_buddy

# 1. Choose the file we want to analyze
filename = "expenses.csv"

# 2. Print the text report to the screen
data_buddy.run_no_code_analysis(filename)

# 3. Generate the professional notebook code
data_buddy.generate_notebook_code(filename)

# 4. DRAW THE GRAPH (This creates the 'business_chart.png' file)
data_buddy.create_visual_report(filename)

print("\n✨ All tasks complete! Check your folder for 'business_chart.png'.")

