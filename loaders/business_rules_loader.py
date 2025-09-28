"""
Business Rules Loader for Mortgage Database

This module loads all business rules from the organized business_rules folders
to create the knowledge graph component of the mortgage database.

Usage:
    from loaders.business_rules_loader import load_business_rules
    load_business_rules()
"""

import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.neo4j_connection import get_neo4j_connection

logger = logging.getLogger(__name__)


def load_business_rules():
    """
    Load all business rules from organized categories to create the knowledge graph.
    
    This loads rules from:
    - Application Processing (intake, URLA 1003)
    - Verification (document, ID verification)
    - Financial Assessment (income calculation, property appraisal)
    - Risk Scoring (scoring rules, qualification thresholds)
    - Underwriting (business rules, underwriting rules)
    - Compliance (compliance rules, special requirements)
    - Pricing (rate pricing)
    - Process Optimization (improvement strategies)
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("🧠 Loading business rules knowledge graph...")
    
    try:
        connection = get_neo4j_connection()
        
        # Track loaded rules for summary
        loaded_rules = {}
        
        # Application Processing Rules
        logger.info("Loading application processing rules...")
        try:
            from business_rules.application_processing.application_intake import load_application_intake_rules
            load_application_intake_rules(connection)
            loaded_rules["Application Intake"] = "✅"
        except ImportError as e:
            logger.warning(f"Could not load application intake rules: {e}")
            loaded_rules["Application Intake"] = "⚠️ "
        
        # Verification Rules
        logger.info("Loading verification rules...")
        try:
            from business_rules.verification.document_verification import load_document_verification_rules
            load_document_verification_rules(connection)
            loaded_rules["Document Verification"] = "✅"
        except ImportError as e:
            logger.warning(f"Could not load document verification rules: {e}")
            loaded_rules["Document Verification"] = "⚠️ "
        
        try:
            from business_rules.verification.id_verification import load_id_verification_rules
            load_id_verification_rules(connection)
            loaded_rules["ID Verification"] = "✅"
        except ImportError as e:
            logger.warning(f"Could not load ID verification rules: {e}")
            loaded_rules["ID Verification"] = "⚠️ "
        
        # Financial Assessment Rules
        logger.info("Loading financial assessment rules...")
        try:
            from business_rules.financial_assessment.income_calculation import load_income_calculation_rules
            load_income_calculation_rules(connection)
            loaded_rules["Income Calculation"] = "✅"
        except ImportError as e:
            logger.warning(f"Could not load income calculation rules: {e}")
            loaded_rules["Income Calculation"] = "⚠️ "
        
        try:
            from business_rules.financial_assessment.property_appraisal import load_property_appraisal_rules
            load_property_appraisal_rules(connection)
            loaded_rules["Property Appraisal"] = "✅"
        except ImportError as e:
            logger.warning(f"Could not load property appraisal rules: {e}")
            loaded_rules["Property Appraisal"] = "⚠️ "
        
        # Risk Scoring Rules
        logger.info("Loading risk scoring rules...")
        try:
            from business_rules.risk_scoring.scoring_rules import load_scoring_rules
            load_scoring_rules(connection)
            loaded_rules["Scoring Rules"] = "✅"
        except ImportError as e:
            logger.warning(f"Could not load scoring rules: {e}")
            loaded_rules["Scoring Rules"] = "⚠️ "
        
        try:
            from business_rules.risk_scoring.qualification_thresholds import load_qualification_thresholds
            load_qualification_thresholds(connection)
            loaded_rules["Qualification Thresholds"] = "✅"
        except ImportError as e:
            logger.warning(f"Could not load qualification thresholds: {e}")
            loaded_rules["Qualification Thresholds"] = "⚠️ "
        
        # Underwriting Rules
        logger.info("Loading underwriting rules...")
        try:
            from business_rules.underwriting.business_rules import load_business_rules as load_underwriting_business_rules
            load_underwriting_business_rules(connection)
            loaded_rules["Underwriting Business Rules"] = "✅"
        except ImportError as e:
            logger.warning(f"Could not load underwriting business rules: {e}")
            loaded_rules["Underwriting Business Rules"] = "⚠️ "
        
        try:
            from business_rules.underwriting.underwriting import load_underwriting_rules
            load_underwriting_rules(connection)
            loaded_rules["Underwriting Rules"] = "✅"
        except ImportError as e:
            logger.warning(f"Could not load underwriting rules: {e}")
            loaded_rules["Underwriting Rules"] = "⚠️ "
        
        # Compliance Rules
        logger.info("Loading compliance rules...")
        try:
            from business_rules.compliance.compliance import load_compliance_rules
            load_compliance_rules(connection)
            loaded_rules["Compliance Rules"] = "✅"
        except ImportError as e:
            logger.warning(f"Could not load compliance rules: {e}")
            loaded_rules["Compliance Rules"] = "⚠️ "
        
        try:
            from business_rules.compliance.special_requirements import load_special_requirements
            load_special_requirements(connection)
            loaded_rules["Special Requirements"] = "✅"
        except ImportError as e:
            logger.warning(f"Could not load special requirements: {e}")
            loaded_rules["Special Requirements"] = "⚠️ "
        
        # Pricing Rules
        logger.info("Loading pricing rules...")
        try:
            from business_rules.pricing.rate_pricing import load_rate_pricing_rules
            load_rate_pricing_rules(connection)
            loaded_rules["Rate Pricing"] = "✅"
        except ImportError as e:
            logger.warning(f"Could not load rate pricing rules: {e}")
            loaded_rules["Rate Pricing"] = "⚠️ "
        
        # Process Optimization Rules
        logger.info("Loading process optimization rules...")
        try:
            from business_rules.process_optimization.improvement_strategies import load_improvement_strategies
            load_improvement_strategies(connection)
            loaded_rules["Improvement Strategies"] = "✅"
        except ImportError as e:
            logger.warning(f"Could not load improvement strategies: {e}")
            loaded_rules["Improvement Strategies"] = "⚠️ "
        
        # Summary
        logger.info("\n📊 Business Rules Loading Summary:")
        logger.info("=" * 50)
        for rule_type, status in loaded_rules.items():
            logger.info(f"{status} {rule_type}")
        
        successful_loads = sum(1 for status in loaded_rules.values() if status == "✅")
        total_rule_types = len(loaded_rules)
        
        logger.info(f"\n✅ Successfully loaded {successful_loads}/{total_rule_types} business rule categories")
        
        if successful_loads == total_rule_types:
            logger.info("🎉 All business rules loaded successfully!")
            return True
        elif successful_loads > 0:
            logger.warning("⚠️  Some business rules loaded with warnings")
            return True
        else:
            logger.error("❌ No business rules could be loaded")
            return False
        
    except Exception as e:
        logger.error(f"❌ Error loading business rules: {e}")
        return False


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    success = load_business_rules()
    if not success:
        exit(1)

