# Contributing to Fake Log Generator

Thank you for your interest in contributing to Fake Log Generator! This project is designed to help developers learn GraphQL by providing realistic log data for testing and development.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the [Issues](https://github.com/yourusername/fake_log_generator/issues) section
2. Create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (Python version, OS)

### Suggesting Features

1. Check if the feature has already been requested
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Implementation suggestions (if any)

### Code Contributions

#### Setting Up Development Environment

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/fake_log_generator.git
   cd fake_log_generator
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run tests to ensure everything works:
   ```bash
   python -m pytest
   ```

#### Making Changes

1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the project's coding standards:
   - Use type hints
   - Follow the existing naming conventions
   - Keep functions simple and focused
   - Add docstrings for new functions

3. Add tests for new functionality:
   - Test both success and error cases
   - Test edge cases
   - Ensure realistic data generation

4. Run the test suite:
   ```bash
   python -m pytest
   ```

5. Test the CLI functionality:
   ```bash
   python generate_logs.py 10 --format json
   python generate_logs.py 10 --format csv --output test.csv
   ```

#### Submitting Changes

1. Commit your changes with clear commit messages:
   ```bash
   git add .
   git commit -m "Add status code generator with realistic distribution"
   ```

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request with:
   - Clear description of changes
   - Link to related issues
   - Screenshots (if UI changes)
   - Test results

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints for function parameters and return values
- Keep functions simple and focused on a single responsibility
- Use descriptive variable and function names
- Add docstrings for all public functions

### Testing

- Write tests for all new functionality
- Test both individual generators and the factory
- Test edge cases and error conditions
- Ensure realistic data distributions
- Test export functionality

### Adding New Generators

When adding new generators, follow the established patterns:

1. Add to appropriate consolidated file (`core_generators.py` or `client_generators.py`)
2. Define constants for options and weights at the top
3. Create `generate_single()` and `generate_multiple(count)` functions
4. Add comprehensive tests
5. Update the log entry factory
6. Update exporters if needed
7. Update the maintenance guide in README

### Example: Adding a Status Code Generator

```python
# In core_generators.py
STATUS_CODES = [200, 201, 400, 401, 403, 404, 500, 502, 503]
STATUS_CODE_WEIGHTS = [70, 5, 8, 5, 2, 5, 3, 1, 1]

def generate_status_code() -> int:
    """Return a single HTTP status code with realistic distribution."""
    return random.choices(STATUS_CODES, weights=STATUS_CODE_WEIGHTS)[0]

def generate_status_codes(count: int) -> list[int]:
    """Return a list of HTTP status codes with realistic distribution."""
    return [generate_status_code() for _ in range(count)]
```

## Project Structure

```
fake_log_generator/
├── generators/           # Core generation logic
│   ├── core_generators.py
│   ├── client_generators.py
│   └── log_entry_factory.py
├── exporters/           # Data export functionality
│   ├── csv_exporter.py
│   └── postgres_exporter.py
├── tests/              # Test suite
├── generate_logs.py    # CLI script
├── config.py          # Configuration
├── requirements.txt   # Dependencies
├── README.md         # Project documentation
├── CONTRIBUTING.md   # This file
├── LICENSE          # Open source license
└── .gitignore      # Git ignore rules
```

## Getting Help

- Check the [README.md](README.md) for usage examples
- Look at existing issues and pull requests
- Create an issue for questions or problems

## Code of Conduct

This project is committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and constructive in all interactions.

## License

By contributing to this project, you agree that your contributions will be licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0). 