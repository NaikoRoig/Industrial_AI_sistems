import xml.etree.ElementTree as ET
from typing import List
from .models import PIDModel, Equipment, IOSignal

class PIDParser:
    """
    Parses structured P&ID data (simulated with XML/JSON) 
    into the internal project model.
    """
    def __init__(self, source_path: str):
        self.source_path = source_path

    def parse_xml(self) -> PIDModel:
        tree = ET.parse(self.source_path)
        root = tree.getroot()
        
        project = PIDModel(project_name=root.get("name", "Unnamed Project"))
        
        for equip_node in root.findall(".//Equipment"):
            equip = Equipment(
                name=equip_node.get("name"),
                type=equip_node.get("type")
            )
            
            for sig_node in equip_node.findall("Signal"):
                sig = IOSignal(
                    tag=sig_node.get("tag"),
                    description=sig_node.get("desc"),
                    data_type=sig_node.get("type"),
                    signal_type=sig_node.get("io")
                )
                equip.signals.append(sig)
            
            project.inventory.append(equip)
            
        return project
