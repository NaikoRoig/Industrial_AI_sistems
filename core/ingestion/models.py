from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class IOSignal(BaseModel):
    tag: str
    description: str
    data_type: str  # BOOL, INT, REAL, etc.
    address: Optional[str] = None
    signal_type: str = "DI"  # DI, DO, AI, AO

class Equipment(BaseModel):
    name: str
    type: str  # Pump, Valve, Motor, etc.
    signals: List[IOSignal] = []
    metadata: Dict[str, str] = {}

class PIDModel(BaseModel):
    project_name: str
    inventory: List[Equipment] = []
    interlocks: List[Dict[str, str]] = []  # Simplified interlock definitions
