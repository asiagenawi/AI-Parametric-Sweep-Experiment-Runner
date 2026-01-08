# Apser

An AI-powered experiment management system for scientific computing workflows using LangChain, OpenAI, and Jupyter notebooks.

## Setup

**Prerequisites**: Python 3.9+

1. Clone and navigate to the repository:
```bash
git clone <repository-url>
cd Experiment
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

## Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Implementation

### Python API

```python
from schema import EventSchema

# Load and validate event schema
schema = EventSchema({
    "$id": "my-event",
    "version": 1,
    "properties": {
        "timestamp": {"type": "string"},
        "value": {"type": "number"}
    }
})

# Validate data
event_data = {
    "timestamp": "2026-01-07T00:00:00Z",
    "value": 42.0
}
schema.validate(event_data)
```

### Project Structure

```
Experiment/
├── schema.py           # Event schema validation
├── tools/src/          # Custom tools and utilities
├── AgentPrompts/       # AI agent prompts
└── main.ipynb          # Main notebook
```


