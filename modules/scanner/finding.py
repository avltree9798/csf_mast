class Finding:
    def __init__(self, *, title: str, description: str, likelihood: int, impact: int, risk: int, recommendation: str) -> object:
        self.title = title
        self.description = description
        self.likelihood = likelihood
        self.impact = impact
        self.risk = risk
        self.recommendation = recommendation
