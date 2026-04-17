import project_analyzer 
df, status = project_analyzer.safe_load_and_clean('expenses.csv') 
print(status) 
if df is not None: print(project_analyzer.generate_advanced_stats(df)) 
