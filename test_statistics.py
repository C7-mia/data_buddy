import data_buddy

# Test with outliers (like your original test)
scores = [85, 90, 78, 92, 88, 500]  # 500 is the outlier

analyzer = data_buddy.StatisticalAnalyzer(scores)

print("\n" + "="*60)
print("TEST: Outlier Detection & Statistical Rigor")
print("="*60)
print(f"Data: {scores}")

# Get summary
report = analyzer.get_summary_report()

print(f"\n📊 Mean: {report['basics']['mean']}")
print(f"📊 Median: {report['basics']['median']}")
print(f"📐 Std Dev: {report['statistical_rigor']['std_dev']}")
print(f"📐 Variance: {report['statistical_rigor']['variance']}")

print(f"\n⚠️  Outliers Detected: {report['outliers']['count']}")
for outlier in report['outliers']['details']:
    print(f"  • Value {outlier['value']} at position {outlier['index']} is {outlier['type']}")

ci = report['statistical_rigor']['confidence_interval_95']
print(f"\n95% Confidence Interval: [{ci['lower']}, {ci['upper']}]")

print(f"\n✅ Data Quality: {report['data_quality']['rating']} ({report['data_quality']['score']}/100)")
