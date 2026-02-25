from ..ingestion.models import PIDModel

class SiemensExporter:
    """
    Exports the synthesized logic into Siemens TIA Portal SCL format.
    """
    def export(self, model: PIDModel, logic_content: str) -> str:
        header = f"FUNCTION_BLOCK FB_{model.project_name.replace(' ', '_')}\n"
        header += "VAR_INPUT\n"
        
        # Add all DI signals to input variables
        for equip in model.inventory:
            for sig in equip.signals:
                if sig.signal_type == "DI":
                    header += f"  {sig.tag} : {sig.data_type}; // {sig.description}\n"
        
        header += "END_VAR\n"
        header += "VAR_OUTPUT\n"
        
        # Add all DO signals to output variables
        for equip in model.inventory:
            for sig in equip.signals:
                if sig.signal_type == "DO":
                    header += f"  {sig.tag} : {sig.data_type};\n"
                    
        header += "END_VAR\n"
        header += "BEGIN\n"
        
        footer = "END_FUNCTION_BLOCK\n"
        
        return header + logic_content + footer
