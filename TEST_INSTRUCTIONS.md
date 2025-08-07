# Test Instructions

## Install dependencies
```bash
pip install -r requirements.txt
```

## Run all tests
```bash
python -m pytest tests/ -v
```

## Run specific test file
```bash
python -m pytest tests/test_timestamp_generator.py -v
```

## Run specific test function
```bash
python -m pytest tests/test_timestamp_generator.py::test_generate_timestamp -v
```

## Manual test
```python
from generators.timestamp_generator import generate_timestamp, generate_timestamps

# Single timestamp
print(generate_timestamp())

# Multiple timestamps
print(generate_timestamps(5))
``` 