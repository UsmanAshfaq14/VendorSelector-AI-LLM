import json
import csv
from typing import Dict, List, Union
from dataclasses import dataclass
from io import StringIO
from datetime import datetime

@dataclass
class Supplier:
    supplier_id: str
    price_score: float
    delivery_reliability_score: float
    quality_rating_score: float
    overall_score: float = 0.0

class VendorSelectorAI:
    def __init__(self):
        self.suppliers: List[Supplier] = []
        self.validation_report = {
            "structure": {},
            "required_fields": {},
            "data_types": {},
            "summary": ""
        }

    def get_greeting(self, name: str = None, time: str = None, is_urgent: bool = False) -> str:
        if is_urgent:
            return "VendorSelector-AI here! Let's quickly evaluate your supplier data."
        
        if name:
            return f"Hello, {name}! I'm VendorSelector-AI, here to help select the best supplier."
        
        if time:
            hour = int(time.split(':')[0])
            if 5 <= hour < 12:
                return "Good morning! VendorSelector-AI is ready to assist you."
            elif 12 <= hour < 17:
                return "Good afternoon! Let's evaluate your supplier data together."
            elif 17 <= hour < 22:
                return "Good evening! I'm here to help review your supplier details."
            else:
                return "Hello! VendorSelector-AI is working late to assist you."
        
        return "Greetings! I am VendorSelector-AI, your supplier evaluation assistant. Please share your supplier data in CSV or JSON format to begin."

    def validate_language(self, text: str) -> bool:
        # Simplified language check - could be enhanced with proper language detection
        if not text.isascii():
            raise ValueError("ERROR: Unsupported language detected. Please use ENGLISH.")
        return True

    def validate_format(self, data: str, format_type: str) -> bool:
        if format_type not in ['csv', 'json']:
            raise ValueError("ERROR: Invalid data format. Please provide CSV or JSON.")
        return True

    def validate_score(self, score: float, field_name: str, supplier_id: str) -> bool:
        if not isinstance(score, (int, float)):
            raise ValueError(f"ERROR: Invalid data type in {supplier_id}: {field_name}. Please provide numeric values.")
        if not 0 <= score <= 100:
            raise ValueError(f"ERROR: Invalid value in {supplier_id}: {field_name}. Please provide scores between 0 and 100.")
        return True

    def parse_input_data(self, data: str, format_type: str) -> None:
        self.validate_language(data)
        self.validate_format(data, format_type)
        
        if format_type == 'csv':
            self.parse_csv_data(data)
        else:
            self.parse_json_data(data)

    def parse_csv_data(self, csv_data: str) -> None:
        csv_reader = csv.DictReader(StringIO(csv_data))
        for row in csv_reader:
            self._process_supplier_data(row)

    def parse_json_data(self, json_data: str) -> None:
        data = json.loads(json_data)
        for supplier in data.get("suppliers", []):
            self._process_supplier_data(supplier)

    def _process_supplier_data(self, data: Dict) -> None:
        required_fields = ["supplier_id", "price_score", "delivery_reliability_score", "quality_rating_score"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            raise ValueError(f"ERROR: Missing required field(s): {', '.join(missing_fields)}")

        supplier = Supplier(
            supplier_id=data["supplier_id"],
            price_score=float(data["price_score"]),
            delivery_reliability_score=float(data["delivery_reliability_score"]),
            quality_rating_score=float(data["quality_rating_score"])
        )

        self.validate_score(supplier.price_score, "price_score", supplier.supplier_id)
        self.validate_score(supplier.delivery_reliability_score, "delivery_reliability_score", supplier.supplier_id)
        self.validate_score(supplier.quality_rating_score, "quality_rating_score", supplier.supplier_id)

        supplier.overall_score = self.calculate_overall_score(supplier)
        self.suppliers.append(supplier)

    def calculate_overall_score(self, supplier: Supplier) -> float:
        price_component = (supplier.price_score / 100) * 0.4
        delivery_component = (supplier.delivery_reliability_score / 100) * 0.3
        quality_component = (supplier.quality_rating_score / 100) * 0.3
        return round(price_component + delivery_component + quality_component, 2)

    def generate_validation_report(self) -> str:
        self.validation_report["structure"] = {
            "suppliers": len(self.suppliers),
            "fields_per_record": 4
        }
        
        self.validation_report["required_fields"] = {
            "supplier_id": "Present",
            "price_score": "Present",
            "delivery_reliability_score": "Present",
            "quality_rating_score": "Present"
        }
        
        self.validation_report["data_types"] = {
            "Price Score": "Valid",
            "Delivery Reliability Score": "Valid",
            "Quality Rating Score": "Valid"
        }
        
        report = [
            "# Data Validation Report",
            "## 1. Data Structure Check:",
            f"- Number of suppliers: {self.validation_report['structure']['suppliers']}",
            f"- Number of fields per record: {self.validation_report['structure']['fields_per_record']}",
            "",
            "## 2. Required Fields Check:"
        ]
        
        for field, status in self.validation_report["required_fields"].items():
            report.append(f"- {field}: {status}")
        
        report.extend([
            "",
            "## 3. Data Type Validation:"
        ])
        
        for field, status in self.validation_report["data_types"].items():
            report.append(f"- {field} (positive number): {status}")
        
        report.extend([
            "",
            "## Validation Summary:",
            "Data validation is successful! Proceeding with analysis..."
        ])
        
        return "\n".join(report)

    def generate_supplier_analysis(self, supplier: Supplier, rank: int, is_top: bool) -> str:
        price_component = round((supplier.price_score / 100) * 0.4, 2)
        delivery_component = round((supplier.delivery_reliability_score / 100) * 0.3, 2)
        quality_component = round((supplier.quality_rating_score / 100) * 0.3, 2)
        
        analysis = [
            f"## Supplier {supplier.supplier_id}",
            "### Input Data:",
            f"- Price Score: {supplier.price_score}",
            f"- Delivery Reliability Score: {supplier.delivery_reliability_score}",
            f"- Quality Rating Score: {supplier.quality_rating_score}",
            "",
            "### Detailed Calculations:",
            "",
            "1. Sum the scores:",
            f"   - Price Score: {supplier.price_score} × 0.4 = {price_component}",
            f"   - Delivery Reliability Score: {supplier.delivery_reliability_score} × 0.3 = {delivery_component}",
            f"   - Quality Rating Score: {supplier.quality_rating_score} × 0.3 = {quality_component}",
            "2. Compute Overall Score:",
            f"   $\\text{{Overall Score}} = {price_component} + {delivery_component} + {quality_component} = {supplier.overall_score}$",
            "",
            "### Ranking Status:",
            f"- {'Selected as Top Vendor' if is_top else f'Rank: {rank}'}"
        ]
        return "\n".join(analysis)

    def generate_final_report(self) -> str:
        ranked_suppliers = sorted(self.suppliers, key=lambda x: x.overall_score, reverse=True)
        top_score = ranked_suppliers[0].overall_score if ranked_suppliers else 0
        
        report_sections = [
            self.generate_validation_report(),
            "",
            "# Formulas Used:",
            "1. Overall Supplier Score Formula:",
            r"$$\text{Overall Score} = \left(\frac{\text{price_score}}{100} \times 0.4 \right) + \left(\frac{\text{delivery_reliability_score}}{100} \times 0.3 \right) + \left(\frac{\text{quality_rating_score}}{100} \times 0.3 \right)$$",
            "",
            "# Supplier Evaluation Summary",
            f"Total Suppliers Evaluated: {len(self.suppliers)}",
            "",
            "# Detailed Analysis for Each Supplier"
        ]
        
        for i, supplier in enumerate(ranked_suppliers, 1):
            is_top = supplier.overall_score == top_score
            report_sections.append(self.generate_supplier_analysis(supplier, i, is_top))
        
        report_sections.extend([
            "",
            "# Final Ranking",
            f"Top supplier(s) with overall score of {top_score}:",
        ])
        
        for supplier in ranked_suppliers:
            if supplier.overall_score == top_score:
                report_sections.append(f"- Supplier {supplier.supplier_id}")
        
        report_sections.extend([
            "",
            "# Feedback Request",
            "Would you like detailed calculations for any specific supplier? Rate this analysis (1-5)."
        ])
        
        return "\n".join(report_sections)

def main():
    # Your supplier data
    csv_data = '''supplier_id,price_score,delivery_reliability_score,quality_rating_score
s1,78,85,80
s2,82,80,79
s3,91,88,86
s4,67,90,75
s5,74,83,84
s6,88,92,89
s7,70,76,77
s8,85,89,90
s9,79,83,82
s10,90,89,91
s11,86,87,85
s12,75,81,80
s13,92,90,91
s14,73,78,76
s15,80,85,82    '''

    selector = VendorSelectorAI()
    
    try:
        # Show greeting (optional)
        greeting = selector.get_greeting(time="14:30")
        print(f"{greeting}\n")
        
        # Process the data and generate report
        selector.parse_input_data(csv_data, 'csv')
        print(selector.generate_final_report())
        
    except ValueError as e:
        print(str(e))

if __name__ == "__main__":
    main()
