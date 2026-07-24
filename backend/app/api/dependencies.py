"""FastAPI dependency providers.

Concrete dependencies will be added as backend and AI modules are integrated.
"""


def get_decision_service():
    raise RuntimeError(
        "DecisionService is not available until backend and AI modules are integrated."
    )
