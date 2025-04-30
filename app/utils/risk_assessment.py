import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

class GeneticRiskAssessment:
    def __init__(self):
        self.label_encoder = LabelEncoder()
        self.risk_model = RandomForestClassifier(n_estimators=100, random_state=42)
        
    def _encode_mutations(self, mutations):
        """
        Encode genetic mutations into numerical values
        """
        if pd.isna(mutations) or mutations == '':
            return 0
        # Count the number of harmful mutations
        mutation_count = len([m for m in mutations.split(',') if 'Positive' in m])
        return mutation_count

    def _encode_conditions(self, conditions):
        """
        Encode genetic conditions into numerical values
        """
        if pd.isna(conditions) or conditions == '':
            return 0
        # Count the number of genetic conditions
        return len(conditions.split(','))

    def _calculate_family_risk_score(self, relationships, conditions):
        """
        Calculate risk score based on family history
        """
        if pd.isna(relationships) or pd.isna(conditions):
            return 0.0
        
        relationship_weights = {
            'Parent': 0.5,
            'Sibling': 0.25,
            'Grandparent': 0.125,
            'Aunt/Uncle': 0.0625,
            'Cousin': 0.03125
        }
        
        total_score = 0.0
        relationships_list = relationships.split(',')
        conditions_list = conditions.split(',')
        
        for rel, cond in zip(relationships_list, conditions_list):
            rel = rel.strip()
            weight = relationship_weights.get(rel, 0)
            total_score += weight
            
        return min(total_score, 1.0)  # Normalize to maximum of 1.0

    def _analyze_gene_sequence(self, sequence):
        """
        Analyze gene sequence for known risk patterns
        """
        if pd.isna(sequence) or sequence == '':
            return 0.0
            
        # Define some example risk patterns (replace with actual genetic risk patterns)
        risk_patterns = {
            'BRCA1': ['ACTG', 'GCTA'],
            'BRCA2': ['TGAC', 'CATG'],
            'P53': ['AGCT', 'TCGA']
        }
        
        risk_score = 0.0
        for gene, patterns in risk_patterns.items():
            for pattern in patterns:
                if pattern in sequence:
                    risk_score += 0.1  # Increment risk score for each found pattern
                    
        return min(risk_score, 1.0)  # Normalize to maximum of 1.0

    def calculate_risk_scores(self, genetic_data, family_history):
        """
        Calculate overall risk scores based on genetic data and family history
        
        Parameters:
        genetic_data: dict containing gene_sequence, mutations, test_results
        family_history: dict containing relationships and genetic_conditions
        
        Returns:
        dict containing risk scores and analysis
        """
        # Extract features
        mutation_score = self._encode_mutations(genetic_data.get('mutations', ''))
        gene_score = self._analyze_gene_sequence(genetic_data.get('gene_sequence', ''))
        family_score = self._calculate_family_risk_score(
            family_history.get('relationships', ''),
            family_history.get('genetic_conditions', '')
        )
        
        # Calculate weighted risk score
        overall_risk_score = (
            0.4 * mutation_score +
            0.3 * gene_score +
            0.3 * family_score
        )
        
        # Determine risk level
        if overall_risk_score >= 0.7:
            risk_level = "High"
        elif overall_risk_score >= 0.4:
            risk_level = "Moderate"
        else:
            risk_level = "Low"
            
        # Generate recommendations based on risk level
        recommendations = self._generate_recommendations(
            risk_level,
            genetic_data.get('mutations', ''),
            family_history.get('genetic_conditions', '')
        )
        
        return {
            'overall_risk_score': round(overall_risk_score, 2),
            'risk_level': risk_level,
            'component_scores': {
                'mutation_score': round(mutation_score, 2),
                'gene_score': round(gene_score, 2),
                'family_score': round(family_score, 2)
            },
            'recommendations': recommendations,
            'assessment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def _generate_recommendations(self, risk_level, mutations, conditions):
        """
        Generate personalized recommendations based on risk assessment
        """
        recommendations = []
        
        # Basic recommendations based on risk level
        if risk_level == "High":
            recommendations.extend([
                "Schedule regular genetic counseling sessions (every 3-6 months)",
                "Consider preventive medical interventions",
                "Implement intensive screening protocol"
            ])
        elif risk_level == "Moderate":
            recommendations.extend([
                "Schedule annual genetic counseling sessions",
                "Regular medical check-ups",
                "Consider lifestyle modifications"
            ])
        else:  # Low risk
            recommendations.extend([
                "Annual medical check-ups",
                "Maintain healthy lifestyle",
                "Stay informed about family health history"
            ])
            
        # Specific recommendations based on mutations
        if 'BRCA' in mutations:
            recommendations.append("Consider increased breast and ovarian cancer screening")
        if 'APOE' in mutations:
            recommendations.append("Monitor cardiovascular health closely")
            
        # Recommendations based on family conditions
        if 'Diabetes' in conditions:
            recommendations.append("Regular blood sugar monitoring")
        if 'Heart Disease' in conditions:
            recommendations.append("Regular cardiovascular check-ups")
            
        return recommendations

    def generate_report(self, patient_data, genetic_data, family_history):
        """
        Generate a complete risk assessment report
        
        Parameters:
        patient_data: dict containing patient information
        genetic_data: dict containing genetic test results
        family_history: dict containing family history information
        
        Returns:
        dict containing complete report
        """
        risk_assessment = self.calculate_risk_scores(genetic_data, family_history)
        
        report = {
            'patient_info': {
                'name': patient_data.get('name', ''),
                'id': patient_data.get('id', ''),
                'medical_history': patient_data.get('medical_history', '')
            },
            'risk_assessment': risk_assessment,
            'genetic_summary': {
                'mutations_found': genetic_data.get('mutations', ''),
                'test_results': genetic_data.get('test_results', '')
            },
            'family_history_summary': {
                'affected_relations': family_history.get('relationships', ''),
                'conditions': family_history.get('genetic_conditions', '')
            },
            'report_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'follow_up_date': self._calculate_follow_up_date(risk_assessment['risk_level'])
        }
        
        return report

    def _calculate_follow_up_date(self, risk_level):
        """
        Calculate recommended follow-up date based on risk level
        """
        today = datetime.now()
        if risk_level == "High":
            follow_up = datetime.now().replace(month=today.month + 3 if today.month <= 9 else ((today.month + 3) % 12))
        elif risk_level == "Moderate":
            follow_up = datetime.now().replace(month=today.month + 6 if today.month <= 6 else ((today.month + 6) % 12))
        else:
            follow_up = datetime.now().replace(year=today.year + 1)
            
        return follow_up.strftime('%Y-%m-%d')

# Usage example:
if __name__ == "__main__":
    # Sample data
    patient_data = {
        'name': 'John Doe',
        'id': '12345',
        'medical_history': 'Previous cancer diagnosis'
    }
    
    genetic_data = {
        'gene_sequence': 'ACTGACTG',
        'mutations': 'BRCA1 Positive, P53 Negative',
        'test_results': 'Positive'
    }
    
    family_history = {
        'relationships': 'Parent,Sibling',
        'genetic_conditions': 'Breast Cancer,Diabetes'
    }
    
    # Create risk assessment instance
    risk_assessor = GeneticRiskAssessment()
    
    # Generate report
    report = risk_assessor.generate_report(patient_data, genetic_data, family_history)
    
    # Print report (for testing)
    import json
    print(json.dumps(report, indent=2))