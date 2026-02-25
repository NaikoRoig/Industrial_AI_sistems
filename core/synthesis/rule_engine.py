from typing import List, Dict
from ..ingestion.models import PIDModel, Equipment, IOSignal

class KnowledgeBase:
    """
    Simulated Engineering Knowledge Base with standard rules.
    """
    RULES = [
        {
            "equipment_type": "CentrifugalPump",
            "rule": "Interlock Stop if Fault is True",
            "logic": "IF {tag_prefix}_FLT THEN {tag_prefix}_RUN := FALSE; END_IF;"
        },
        {
            "equipment_type": "DigitalValve",
            "rule": "Mismatched State Alarm",
            "logic": "IF {tag_prefix}_OPEN AND {tag_prefix}_CLOSE THEN {tag_prefix}_ALM_CONFIG := TRUE; END_IF;"
        }
    ]

class RuleEngine:
    """
    Synthesizes SCL logic fragments based on engineering rules and user intent.
    """
    def generate_with_intent(self, model: PIDModel, intent: str) -> str:
        scl_code = f"// Automated Industrial Synthesis\n// Intent: {intent if intent else 'Default baseline logic'}\n\n"
        
        intent = intent.lower()
        
        # Base interlocks are always included
        scl_code += "// --- SAFETY INTERLOCKS ---\n"
        for equip in model.inventory:
            for rule in KnowledgeBase.RULES:
                if equip.type == rule["equipment_type"]:
                    scl_code += rule["logic"].format(tag_prefix=equip.name.split('_')[0] + equip.name.split('_')[1]) + "\n"
        
        # Sequence Logic Synthesis
        if "secuencia" in intent or "sequence" in intent:
            scl_code += "\n// --- SEQUENTIAL CONTROL ---\n"
            scl_code += "CASE State OF\n"
            scl_code += "  0: // IDLE\n"
            scl_code += "    IF Start_PB THEN State := 10; END_IF;\n"
            scl_code += "  10: // STARTUP\n"
            for equip in model.inventory:
                if equip.type == "CentrifugalPump":
                    scl_code += f"    {equip.name.replace('_','')}_RUN := TRUE;\n"
            scl_code += "    State := 20;\n"
            scl_code += "  20: // RUNNING\n"
            scl_code += "    IF Stop_PB THEN State := 30; END_IF;\n"
            scl_code += "  30: // SHUTDOWN\n"
            for equip in model.inventory:
                if equip.type == "CentrifugalPump":
                    scl_code += f"    {equip.name.replace('_','')}_RUN := FALSE;\n"
            scl_code += "    State := 0;\n"
            scl_code += "END_CASE;\n"

        # Diagnostic Logic Synthesis
        if "diagnóstico" in intent or "diagnostic" in intent or "alarm" in intent:
            scl_code += "\n// --- DIAGNOSTICS & ALARMS ---\n"
            for equip in model.inventory:
                scl_code += f"IF NOT {equip.name.replace('_','')}_FBK AND {equip.name.replace('_','')}_RUN THEN\n"
                scl_code += f"  {equip.name.replace('_','')}_ALM_FAIL := TRUE;\n"
                scl_code += "END_IF;\n"
                
        return scl_code
