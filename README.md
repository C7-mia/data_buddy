# Data Buddy

Data Buddy is a production-ready, extensible Python library for no-code and low-code data analysis workflows.

## Quick Start

```python
from data_buddy import Buddy

buddy = Buddy().load("expenses.csv").clean()
report = buddy.detect()
insights = buddy.insight(target="amount")
fig = buddy.view(mode="auto")
```

## Public API

- `Buddy.load(path_or_url)`
- `Buddy.clean(strategy_override=None)`
- `Buddy.detect(z_threshold=3.0)`
- `Buddy.insight(target=None)`
- `Buddy.view(mode="auto", x=None, y=None)`

## Architecture

```text
src/data_buddy/
  core/
  preprocessing/
  stats/
  viz/
  models/
  utils/
```

## Installation

```bash
pip install data-buddy
pip install data-buddy[viz]
pip install data-buddy[ml]
```

## CLI

```bash
data-buddy expenses.csv --target amount
```
