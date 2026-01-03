from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

@dataclass
class NPCResult:
    name: str
    species: str
    role: str
    personality: str
    goal: str
    quirk: str
    hook: str
    extras: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
class BaseNPCGenerator:
    game_slug: str      # eg. "dnd-5e"

    def generate(self, *, seed: Optional[int] = None, **opts) -> NPCResult:
        raise NotImplementedError