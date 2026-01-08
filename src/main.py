#!/usr/bin/env python3
"""
Experiment Management System - Main Script
"""
import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from agents import Agent, Runner, AgentOutputSchema
from src.tools.schema import ExperimentSpec
from agents.tool import WebSearchTool
from tools.fileWriter import write_file_tool
from tools.executeCommand import execute_command_tool
from tools.fileReader import read_file_tool


async def main():
    """Main workflow for experiment management."""
    # Setup
    load_dotenv()
    llm = ChatOpenAI(model="gpt-5.2", temperature=0)

    print("\n=== Step 1: Parsing Experiment Specification ===")
    PARSER_INSTRUCTIONS = Path('AgentPrompts/parser.txt').read_text(encoding="utf-8")
    parser = Agent(
        name='Experiment Specification Parser',
        instructions=PARSER_INSTRUCTIONS,
        output_type=AgentOutputSchema(ExperimentSpec, strict_json_schema=False),
        model='gpt-4o'
    )

    user_text = input('''
Describe the experiment you want to run.

Please explain, in plain English:
    - What the experiment is doing conceptually (what is being simulated, evaluated, or tested)
    - What inputs can vary (parameters you want to sweep or optimize, with ranges or options)
    - What inputs stay fixed (constants or conditions held the same across runs)
    - What your goal is, if any (explore behavior, minimize/maximize something, hit a target)
    - What you want to measure (outputs or metrics you care about)
    - How you want the system to search (exhaustive grid, random sampling, or adaptive optimization)
    - Where it should run (local machine, cluster, container)
    - Any important setup details, assumptions, or context?

Your input: ''')

    parser_result = await Runner.run(parser, user_text)
    spec = parser_result.final_output
    data = spec.model_dump_json(indent=2)

    with open("experiment.json", "w") as f:
        f.write(data)
    print("✓ Experiment specification saved to experiment.json")

    print("\n=== Step 2: Reviewing Specification ===")
    CRITIC_INSTRUCTIONS = Path('AgentPrompts/critic.txt').read_text(encoding="utf-8")
    spec = ExperimentSpec.model_validate(
        json.loads(Path("experiment.json").read_text())
    )
    critic = Agent(
        name='Spec Critic',
        instructions=CRITIC_INSTRUCTIONS,
        model='gpt-4o',
    )
    critic_result = await Runner.run(critic, spec.model_dump_json(indent=2))
    user_clarifying_response = input(f"\n{critic_result.final_output}\n\nYour response: ")

    print("\n=== Step 3: Updating Specification ===")
    editor_partial_instructions = Path("AgentPrompts/editor.txt").read_text(encoding="utf-8")
    EDITOR_INSTRUCTIONS = f'''
You are an experiment specification editor.

Task:
Given:
    (1) an existing experiment specification JSON: {spec.model_dump_json(indent=2)}
    (2) clarification questions that were asked to the user: {critic_result.final_output}
    (3) the user's answers to those questions, which will be provided to you as input
produce an UPDATED experiment specification JSON.
{editor_partial_instructions}
'''

    editor = Agent(
        name="Experiment Spec Editor",
        instructions=EDITOR_INSTRUCTIONS,
        model='gpt-4o',
        output_type=AgentOutputSchema(ExperimentSpec, strict_json_schema=False),
    )
    editor_result = await Runner.run(editor, user_clarifying_response)
    spec = editor_result.final_output
    data = spec.model_dump_json(indent=2)

    with open("experiment.json", "w") as f:
        f.write(data)
    print("✓ Updated specification saved")

    print("\n=== Step 4: Summarizing Experiment ===")
    SUMMARIZER_INSTRUCTIONS = Path("AgentPrompts/summarizer.txt").read_text(encoding="utf-8")
    summarizer = Agent(
        name='Experiment Summarizer',
        instructions=SUMMARIZER_INSTRUCTIONS,
        model='gpt-4o'
    )
    spec = ExperimentSpec.model_validate(
        json.loads(Path("experiment.json").read_text())
    )
    summarizer_result = await Runner.run(summarizer, spec.model_dump_json(indent=2))
    print("\nHere is your experiment as I understand it:")
    print(summarizer_result.final_output)

    print("\n=== Step 5: Conducting Research ===")
    RESEARCHER_INSTRUCTIONS = Path("AgentPrompts/researcher.txt").read_text(encoding="utf-8")
    spec = ExperimentSpec.model_validate(
        json.loads(Path("experiment.json").read_text())
    )
    researcher = Agent(
        name='Experiment Researcher',
        instructions=RESEARCHER_INSTRUCTIONS,
        model='gpt-4o',
        tools=[WebSearchTool()]
    )
    researcher_result = await Runner.run(researcher, spec.model_dump_json(indent=2))

    with open("research.txt", "w") as f:
        f.write(researcher_result.final_output)
    print("✓ Research saved to research.txt")

    print("\n=== Step 6: Executing Experiment ===")
    EXECUTOR_INSTRUCTIONS = Path("AgentPrompts/executor.txt").read_text(encoding="utf-8")
    executor = Agent(
        name='Experiment Executor',
        instructions=EXECUTOR_INSTRUCTIONS,
        model='gpt-4o',
        tools=[write_file_tool, execute_command_tool]
    )
    executor_result = await Runner.run(executor, researcher_result.final_output)
    print(executor_result.final_output)
    
    print("\n=== Step 7: Plotting Results ===")
    PLOTTER_INSTRUCTIONS = Path("AgentPrompts/plotter.txt").read_text(encoding="utf-8")
    plotter = Agent(
        name='Results Plotter',
        instructions=PLOTTER_INSTRUCTIONS,
        model='gpt-4o',
        tools=[read_file_tool, write_file_tool, execute_command_tool]
    )
    plot_result = await Runner.run(plotter, "results.log")
    print(plot_result.final_output)

    print("\n=== Step 8: Writing Report ===")
    WRITER_INSTRUCTIONS = Path("AgentPrompts/writer.txt").read_text(encoding="utf-8")
    writer = Agent(
        name='Report Writer',
        instructions=WRITER_INSTRUCTIONS,
        tools=[write_file_tool, read_file_tool]
    )
    files = f"results.log, experiment.json, research.txt, plot.png, {executor_result.final_output}"
    report_result = await Runner.run(writer, files)

    print("\n✓ Experiment workflow complete!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nWorkflow cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
