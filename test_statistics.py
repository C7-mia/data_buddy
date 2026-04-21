import data_buddy


def test_statistical_analyzer_summary_contains_expected_sections():
    scores = [85, 90, 78, 92, 88, 500]
    analyzer = data_buddy.StatisticalAnalyzer(scores)
    report = analyzer.get_summary_report()

    assert "basics" in report
    assert "statistical_rigor" in report
    assert "outliers" in report
    assert report["outliers"]["count"] >= 1
    assert report["data_quality"]["score"] <= 100
