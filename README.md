# APSER: AI Parameteric Sensitivity Sweep Experiment Runner
A multi-agent AI system that orchestrates end-to-end parametric sweep experiments: converts natural language into structured specifications, performs automated research, generates and executes code, creates visualizations, and produces comprehensive reports.

## Setup

**Prerequisites**: Python 3.9+

1. Clone and navigate to the repository:
```bash
git clone <repository-url>
cd ASPER
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
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

## Workflow Logic

The main workflow (`src/main.py` or `src/main.ipynb`) orchestrates an 8-step agent pipeline:

### Step 1: Parse (`parser.txt`)
- User describes their experiment in plain English
- Parser agent converts natural language into structured `ExperimentSpec` JSON
- Specification saved to `experiment.json`

### Step 2: Critique (`critic.txt`)
- Critic agent reviews the parsed specification
- Identifies ambiguities, missing details, or potential issues
- Generates clarifying questions for the user

### Step 3: Edit (`editor.txt`)
- User provides answers to clarifying questions
- Editor agent updates the specification based on user responses
- Updated specification overwrites `experiment.json`

### Step 4: Summarize (`summarizer.txt`)
- Summarizer agent generates human-readable description
- User confirms understanding of the planned experiment
- Provides checkpoint before expensive operations

### Step 5: Research (`researcher.txt`)
- Researcher agent performs web searches using `WebSearchTool`
- Gathers implementation details, best practices, parameter values
- Research findings saved to `research.txt`

### Step 6: Execute (`executor.txt`)
- Executor agent writes experiment code using `write_file_tool`
- Runs the experiment using `execute_command_tool`
- Outputs experiment results to `results.log`

### Step 7: Plot (`plotter.txt`)
- Plotter agent reads results using `read_file_tool`
- Generates visualizations (e.g., `plot.png`)
- Uses Python plotting libraries via command execution

### Step 8: Write Report (`writer.txt`)
- Writer agent collects all artifacts (results, plots, research)
- Generates comprehensive experiment report
- Final deliverable synthesizing the entire workflow

### Data Flow

```
User Input (natural language)
    ↓
Parser → experiment.json
    ↓
Critic → clarifying questions
    ↓
Editor → updated experiment.json
    ↓
Summarizer → human summary
    ↓
Researcher → research.txt
    ↓
Executor → results.log + experiment code
    ↓
Plotter → plot.png
    ↓
Writer → final report
```

## Implementation

### Project Structure

```
Experiment/
├── src/
│   ├── main.py              # Main workflow script
│   ├── main.ipynb           # Interactive notebook version
│   └── tools/
│       ├── schema.py        # ExperimentSpec schema
│       ├── fileWriter.py    # File writing tool
│       ├── fileReader.py    # File reading tool
│       └── executeCommand.py # Command execution tool
├── AgentPrompts/
│   ├── parser.txt           # Step 1 instructions
│   ├── critic.txt           # Step 2 instructions
│   ├── editor.txt           # Step 3 instructions
│   ├── summarizer.txt       # Step 4 instructions
│   ├── researcher.txt       # Step 5 instructions
│   ├── executor.txt         # Step 6 instructions
│   ├── plotter.txt          # Step 7 instructions
│   └── writer.txt           # Step 8 instructions
└── .env                     # OPENAI_API_KEY
```


