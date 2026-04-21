import project_analyzer


def test_safe_load_and_generate_advanced_stats():
    df, status = project_analyzer.safe_load_and_clean("expenses.csv")
    assert df is not None
    assert isinstance(status, dict)

    stats = project_analyzer.generate_advanced_stats(df)
    assert "summary" in stats
