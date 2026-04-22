def solve_maji_ndogo_challenge(df):
    """Specific logic for the Maji Ndogo project goals."""
    results = {}
    
    # Task 1: Total population reached
    if 'number_of_people_served' in df.columns:
        results['Total Population'] = df['number_of_people_served'].sum()
    
    # Task 2: Most common source
    if 'type_of_water_source' in df.columns:
        results['Top Source'] = df['type_of_water_source'].value_counts().idxmax()
        
    # Task 3: Quality Check
    if 'water_quality' in df.columns:
        results['Quality Distribution'] = df['water_quality'].value_counts().to_dict()
        
    return results
