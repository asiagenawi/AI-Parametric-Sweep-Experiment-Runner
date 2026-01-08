from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field


class Setup(BaseModel):
    context: Dict[str, Any] = Field(default_factory=dict)
    assumptions: List[str] = Field(default_factory=list)
    methodology: Optional[str] = None
    references: List[str] = Field(default_factory=list)
    notes: Optional[str] = None


class Resources(BaseModel):
    cpus: int = 1
    memory_gb: float = 4.0
    time_minutes: int = 60
    gpus: Optional[int] = None


class Domain(BaseModel):
    kind: Literal["range", "values"] = "values"
    min: Optional[float] = None
    max: Optional[float] = None
    step: Optional[float] = None
    values: Optional[List[Any]] = None
    log: bool = False


class Parameter(BaseModel):
    name: str
    type: Literal["int", "float", "str", "bool"] = "float"
    domain: Domain = Field(default_factory=Domain)


class SearchBudget(BaseModel):
    trials: Optional[int] = None
    time_minutes_total: Optional[int] = None


class SearchConfig(BaseModel):
    strategy: Literal["grid", "random", "optuna", "bayes", "adaptive"] = "grid"
    budget: SearchBudget = Field(default_factory=SearchBudget)
    seed: Optional[int] = None


class Metric(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ObjectiveTarget(BaseModel):
    metric: str
    direction: Literal["maximize", "minimize"] = "maximize"
    target_value: Optional[float] = None
    weight: Optional[float] = None


class Objective(BaseModel):
    type: Literal["single", "multi", "none"] = "single"
    aggregate: Literal["weighted_sum", "pareto", "lexicographic"] = "weighted_sum"
    targets: List[ObjectiveTarget] = Field(default_factory=list)


class Constraint(BaseModel):
    name: Optional[str] = None
    expression: Optional[str] = None


class Outputs(BaseModel):
    artifacts: List[str] = Field(default_factory=list)
    save_stdout: bool = True
    save_stderr: bool = True

class ExperimentSpec(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    setup: Setup = Field(default_factory=Setup)
    constants: Dict[str, Any] = Field(default_factory=dict)
    resources: Resources = Field(default_factory=Resources)
    parameters: List[Parameter] = Field(default_factory=list)
    search: SearchConfig = Field(default_factory=SearchConfig)
    metrics: List[Union[str, Metric]] = Field(default_factory=list)
    objective: Objective = Field(default_factory=Objective)
    constraints: List[Union[str, Constraint]] = Field(default_factory=list)
    outputs: Outputs = Field(default_factory=Outputs)

