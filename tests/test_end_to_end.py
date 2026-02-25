import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.ingestion.pid_parser import PIDParser
from core.synthesis.rule_engine import RuleEngine
from core.exporters.siemens_scl import SiemensExporter

def main():
    # 1. Parse Input
    parser = PIDParser("tests/data/sample_pid.xml")
    project_model = parser.parse_xml()
    print(f"Parsed project: {project_model.project_name}")
    print(f"Discovered {len(project_model.inventory)} equipment items.")

    # 2. Synthesize Logic
    engine = RuleEngine()
    logic = engine.generate_interlocks(project_model)
    print("\nSynthesized Logic Fragment:")
    print("-" * 30)
    print(logic)
    print("-" * 30)

    # 3. Export to Siemens SCL
    exporter = SiemensExporter()
    scl_output = exporter.export(project_model, logic)
    
    output_file = "AlphaFactory_L1.scl"
    with open(output_file, "w") as f:
        f.write(scl_output)
    
    print(f"\nSuccessfully exported code to {output_file}")

if __name__ == "__main__":
    main()
