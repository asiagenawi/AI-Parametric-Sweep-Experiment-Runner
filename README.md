# Apser

An AI-powered experiment management system designed to streamline scientific computing workflows and manage complex experiments with intelligent automation.

## Overview

Apser is a Python-based framework that combines the power of AI agents with Jupyter notebooks to create a seamless experiment management experience. The system leverages LangChain and OpenAI to provide intelligent assistance throughout the experimental workflow.

## Features

- **AI-Powered Automation**: Intelligent agents powered by LangChain and OpenAI for experiment orchestration
- **Schema Validation**: Built-in event schema validation using JSON Schema for data integrity
- **Jupyter Integration**: Native support for Jupyter notebooks with nbconvert capabilities
- **Type-Safe Configuration**: Pydantic v2 for robust data validation and settings management
- **Command-Line Interface**: Easy-to-use CLI tools for managing experiments

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Experiment
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

### Development Installation

For development with additional tools:

```bash
pip install -e ".[dev]"
```

This includes:
- pytest for testing
- black for code formatting
- ruff for linting

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
# Add other environment variables as needed
```

## Usage

### Command-Line Interface

The package provides a CLI entry point:

```bash
# Using the command
apser [options]
```

### Python API

```python
from src.tools import ...
from src.schema import EventSchema

# Example: Load and validate an event schema
schema = EventSchema(schema_dict)
schema.validate(event_data)
```

### Schema Validation

The system includes robust schema validation capabilities:

```python
from schema import EventSchema

# Load schema from a dictionary
schema = EventSchema({
    "$id": "my-event",
    "version": 1,
    "properties": {
        "timestamp": {"type": "string"},
        "value": {"type": "number"}
    }
})

# Validate event data
event_data = {
    "timestamp": "2026-01-07T00:00:00Z",
    "value": 42.0
}
schema.validate(event_data)
```

## Project Structure

```
Experiment/
├── README.md
├── pyproject.toml          # Project configuration and dependencies
├── schema.py               # Event schema validation
├── tools/                  # Custom tools and utilities
│   └── src/               # Source code for tools
├── AgentPrompts/          # AI agent prompt templates
├── venv/                  # Virtual environment (not tracked)
└── main.ipynb             # Main Jupyter notebook
```

## Dependencies

### Core Dependencies

- **langchain-openai**: LangChain integration with OpenAI models
- **python-dotenv**: Environment variable management
- **pydantic**: Data validation using Python type annotations
- **agents**: Agent framework for automation
- **jupyter**: Interactive notebook environment
- **nbconvert**: Converting Jupyter notebooks to various formats
- **jsonschema**: JSON Schema validation
- **referencing**: JSON Schema reference handling

### Development Dependencies

- **pytest**: Testing framework
- **black**: Code formatter
- **ruff**: Fast Python linter

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
```

### Linting

```bash
ruff check .
```

## Schema System

The project includes a sophisticated event schema validation system based on JSON Schema Draft 7:

### Key Features

- **Schema Loading**: Load schemas from dictionaries, YAML/JSON strings, or file paths
- **Validation**: Automatic validation against Jupyter Events metaschema
- **Format Checking**: Built-in format validation for common data types
- **Registry Support**: Handle nested schema references with registries

### Custom Exceptions

- `EventSchemaUnrecognized`: Raised when schema type is not recognized
- `EventSchemaLoadingError`: Raised when schema fails to load
- `EventSchemaFileAbsent`: Raised when schema file is not found

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Write docstrings for public APIs
- Keep functions focused and concise

## License

[Specify your license here]

## Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Powered by [OpenAI](https://openai.com/)
- Schema validation based on [Jupyter Events](https://github.com/jupyter/jupyter_events)

## Support

For issues, questions, or contributions, please:
- Open an issue on GitHub
- Check existing documentation
- Review the example notebooks

## Roadmap

- [ ] Enhanced agent capabilities
- [ ] Additional schema validation features
- [ ] Improved CLI interface
- [ ] Comprehensive documentation
- [ ] Example experiment templates

## Version History

### 0.1.0 (Current)
- Initial release
- Basic experiment management functionality
- Schema validation system
- CLI tools
- Jupyter integration

---

**Note**: This project is under active development. APIs may change between versions.
