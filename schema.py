from pydantic import BaseModel
from typing import List

class Analysis(BaseModel):
    file_path: str
    line_number: int
    issue: str
    suggested_fix: str
    time_complexity: str  # e.g., "O(n^2) -> O(n)"
    severity: str        # e.g., "Critical" or "Nit"