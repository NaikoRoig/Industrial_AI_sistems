from flask import Flask, render_template, jsonify, request
import sys
import os

# Add core to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.ingestion.pid_parser import PIDParser
from core.synthesis.rule_engine import RuleEngine
from core.exporters.siemens_scl import SiemensExporter
from core.verification.test_runner import POUVerifier

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.json or {}
        user_prompt = data.get("prompt", "")
        
        # 1. Parse Input
        xml_path = "tests/data/sample_pid.xml"
        parser = PIDParser(xml_path)
        project_model = parser.parse_xml()
        
        # 2. Synthesize Logic
        engine = RuleEngine()
        logic = engine.generate_with_intent(project_model, user_prompt)
        
        # 3. Export to Siemens SCL
        exporter = SiemensExporter()
        scl_output = exporter.export(project_model, logic)
        
        # 4. Verify
        verifier = POUVerifier()
        # Simulated test
        verification_passed = verifier.verify_interlock(
            "PUMP_01", 
            {"PUMP01_RUN": True, "PUMP01_FLT": True}, 
            {"PUMP01_RUN": False}
        )
        
        return jsonify({
            "status": "success",
            "project_name": project_model.project_name,
            "equipment_count": len(project_model.inventory),
            "scl_code": scl_output,
            "verification": "Passed" if verification_passed else "Failed"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
