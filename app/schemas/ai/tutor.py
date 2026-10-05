from pydantic import BaseModel, Field


class TutorAnalysis(BaseModel):
    is_correct: bool
    first_error_step: int | None = Field(default=None, ge=1)
    error_content: str | None = None

    concept_code: str | None = None
    skill_code: str | None = None
    misconception_code: str | None = None

    confidence: float = Field(ge=0.0, le=1.0)


class RepeatedMisconception(BaseModel):
    code: str
    count: int = Field(ge=1)


class TutorStudentState(BaseModel):
    concept_mastery: float | None = Field(default=None, ge=0.0, le=1.0)
    skill_mastery: float | None = Field(default=None, ge=0.0, le=1.0)
    skill_weakness: float | None = Field(default=None, ge=0.0, le=1.0)

    consecutive_wrong_count: int = Field(default=0, ge=0)

    repeated_misconceptions: list[RepeatedMisconception] = []


class PrerequisiteSkillState(BaseModel):
    skill_code: str
    mastery_score: float | None = Field(default=None, ge=0.0, le=1.0)


class TutorAttemptContext(BaseModel):
    retry_count: int = Field(default=0, ge=0)
    hint_count: int = Field(default=0, ge=0)
    solve_time_seconds: int | None = Field(default=None, ge=0)


class TutorRequest(BaseModel):
    request_id: str
    student_id: int
    attempt_id: int

    analysis: TutorAnalysis
    student_state: TutorStudentState

    prerequisite_skills: list[PrerequisiteSkillState] = []

    attempt_context: TutorAttemptContext


from typing import Literal


TutorActionType = Literal[
    "HINT",
    "CONCEPT_REVIEW",
    "PREREQUISITE_REVIEW",
    "VARIANT_PROBLEM",
]


class TutorHint(BaseModel):
    level: int = Field(ge=1)
    content: str


class TutorTarget(BaseModel):
    concept_code: str | None = None
    skill_code: str | None = None


class TutorVariantProblem(BaseModel):
    problem_code: str


class TutorActionResult(BaseModel):
    action_type: TutorActionType
    reason: str
    message: str

    hint: TutorHint | None = None
    target: TutorTarget | None = None
    variant_problem: TutorVariantProblem | None = None


class TutorResponse(BaseModel):
    request_id: str
    attempt_id: int
    tutor_action: TutorActionResult
