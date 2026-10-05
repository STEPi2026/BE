from typing import Literal

from pydantic import BaseModel, Field, model_validator


class AIAnalysisProblem(BaseModel):
    source_type: Literal["internal", "captured"]

    problem_id: int | None = None
    captured_problem_id: int | None = None
    problem_code: str | None = None

    problem_text: str | None = None
    problem_image_url: str | None = None

    @model_validator(mode="after")
    def validate_problem_source(self):
        if self.source_type == "internal":
            if self.problem_id is None:
                raise ValueError(
                    "internal problem requires problem_id"
                )

            if self.captured_problem_id is not None:
                raise ValueError(
                    "internal problem cannot have captured_problem_id"
                )

        elif self.source_type == "captured":
            if self.captured_problem_id is None:
                raise ValueError(
                    "captured problem requires captured_problem_id"
                )

            if self.problem_id is not None:
                raise ValueError(
                    "captured problem cannot have problem_id"
                )

        return self


class AIAnalysisSolution(BaseModel):
    solution_image_url: str | None = None
    solution_text: str | None = None

    @model_validator(mode="after")
    def validate_solution(self):
        if (
            self.solution_image_url is None
            and self.solution_text is None
        ):
            raise ValueError(
                "solution_image_url or solution_text is required"
            )

        return self


class AIAnalysisAttemptContext(BaseModel):
    retry_count: int = Field(default=0, ge=0)
    solve_time_seconds: int | None = Field(default=None, ge=0)
    hint_count: int = Field(default=0, ge=0)


class AIAnalysisRequest(BaseModel):
    request_id: str
    attempt_id: int
    student_id: int

    problem: AIAnalysisProblem
    solution: AIAnalysisSolution
    attempt: AIAnalysisAttemptContext


class AIAnalysisTarget(BaseModel):
    code: str
    confidence: float = Field(ge=0.0, le=1.0)


class AIAnalysisResult(BaseModel):
    is_correct: bool

    first_error_step: int | None = Field(default=None, ge=1)
    error_content: str | None = None

    concept: AIAnalysisTarget | None = None
    skill: AIAnalysisTarget | None = None
    misconception: AIAnalysisTarget | None = None

    overall_confidence: float = Field(ge=0.0, le=1.0)


class AIAnalysisResponse(BaseModel):
    request_id: str
    attempt_id: int
    analysis: AIAnalysisResult
