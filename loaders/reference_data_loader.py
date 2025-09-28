"""
Reference Data Loader for Mortgage Database

This module loads core reference data that forms the foundation of the mortgage
knowledge graph. This includes loan programs, qualification requirements,
process steps, and borrower profiles.

Usage:
    from loaders.reference_data_loader import load_reference_data
    load_reference_data()
"""

import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.neo4j_connection import get_neo4j_connection

logger = logging.getLogger(__name__)


def load_loan_programs():
    """Load loan program data into Neo4j."""
    logger.info("Loading loan programs...")
    connection = get_neo4j_connection()
    
    loan_programs = [
        {
            "name": "FHA",
            "full_name": "FHA (Federal Housing Administration) Loan",
            "type": "Government-backed",
            "summary": "Government-insured loan designed for first-time buyers and those with lower credit scores or limited down payment funds",
            "min_credit_score": 580,
            "min_down_payment": 0.035,  # 3.5%
            "max_dti": 0.57,  # 57%
            "mortgage_insurance_required": True,
            "benefits": [
                "Low down payment requirement (3.5%)",
                "Lower credit score acceptance", 
                "Gift funds allowed for down payment",
                "Down payment assistance programs available",
                "Assumable loans",
                "Easier qualification guidelines"
            ],
            "considerations": [
                "Mortgage insurance premium required",
                "Property limits apply",
                "Primary residence only",
                "Property must meet FHA standards"
            ]
        },
        {
            "name": "VA",
            "full_name": "VA (Veterans Affairs) Loan",
            "type": "Government-backed",
            "summary": "Loan program exclusively for eligible veterans, service members, and surviving spouses",
            "min_credit_score": 620,  # Most lenders prefer this minimum
            "min_down_payment": 0.0,  # 0% - No down payment required
            "max_dti": 0.41,  # 41% (can go higher with compensating factors)
            "mortgage_insurance_required": False,
            "benefits": [
                "No down payment required",
                "No private mortgage insurance",
                "Competitive interest rates",
                "No prepayment penalties",
                "Assumable loans",
                "Multiple use for eligible borrowers"
            ],
            "considerations": [
                "VA funding fee applies (can be financed)",
                "Only for eligible veterans/service members",
                "Property must be primary residence",
                "VA appraisal required"
            ]
        },
        {
            "name": "USDA",
            "full_name": "USDA Rural Development Loan",
            "type": "Government-backed",
            "summary": "Zero-down payment loan for eligible rural and suburban areas",
            "min_credit_score": 640,
            "min_down_payment": 0.0,  # 0%
            "max_dti": 0.41,  # 41%
            "mortgage_insurance_required": True,
            "benefits": [
                "No down payment required",
                "Below-market interest rates",
                "Low mortgage insurance",
                "Flexible credit guidelines"
            ],
            "considerations": [
                "Income limits apply",
                "Property must be in eligible rural area",
                "Primary residence only",
                "Annual fee required"
            ]
        },
        {
            "name": "CONVENTIONAL",
            "full_name": "Conventional Loan",
            "type": "Conventional",
            "summary": "Standard mortgage not insured by government, offers flexibility for various borrower profiles",
            "min_credit_score": 620,
            "min_down_payment": 0.03,  # 3%
            "max_dti": 0.43,  # 43% (may vary by lender)
            "mortgage_insurance_required": True,  # If less than 20% down
            "benefits": [
                "Can be used for primary, secondary, or investment properties",
                "PMI can be removed at 20% equity",
                "Higher loan limits than government loans",
                "Variety of term options"
            ],
            "considerations": [
                "Higher credit score requirements",
                "PMI required if less than 20% down",
                "Stricter debt-to-income requirements",
                "Full documentation typically required"
            ]
        },
        {
            "name": "JUMBO",
            "full_name": "Jumbo Loan",
            "type": "Conventional",
            "summary": "Loan amounts above conforming loan limits, typically for high-value properties",
            "min_credit_score": 700,
            "min_down_payment": 0.10,  # 10-20% typically required
            "max_dti": 0.38,  # 38% (stricter requirements)
            "mortgage_insurance_required": False,
            "benefits": [
                "Finance high-value properties",
                "Competitive rates for qualified borrowers",
                "Various term options available"
            ],
            "considerations": [
                "Higher credit score requirements",
                "Larger down payment required",
                "Stricter debt-to-income ratios",
                "More cash reserves required",
                "Comprehensive documentation required"
            ]
        }
    ]
    
    for program in loan_programs:
        query = """
        CREATE (lp:LoanProgram {
            name: $name,
            full_name: $full_name,
            type: $type,
            summary: $summary,
            min_credit_score: $min_credit_score,
            min_down_payment: $min_down_payment,
            max_dti: $max_dti,
            mortgage_insurance_required: $mortgage_insurance_required,
            benefits: $benefits,
            considerations: $considerations
        })
        """
        connection.execute_query(query, program)
        logger.debug(f"Created LoanProgram: {program['name']}")
    
    logger.info(f"✅ Loaded {len(loan_programs)} loan programs")


def load_qualification_requirements():
    """Load qualification requirements into Neo4j."""
    logger.info("Loading qualification requirements...")
    connection = get_neo4j_connection()
    
    requirements = [
        {
            "requirement_type": "CreditScore",
            "min_value": 580,
            "max_value": 850,
            "description": "FICO credit score requirement",
            "applies_to": ["FHA", "VA", "USDA", "Conventional", "Jumbo"],
            "notes": "Minimum varies by loan program"
        },
        {
            "requirement_type": "DebtToIncome",
            "min_value": 0.0,
            "max_value": 0.57,
            "description": "Total debt-to-income ratio",
            "applies_to": ["FHA", "VA", "USDA", "Conventional", "Jumbo"],
            "notes": "Maximum varies by loan program and compensating factors"
        },
        {
            "requirement_type": "DownPayment",
            "min_value": 0.0,
            "max_value": 1.0,
            "description": "Minimum down payment percentage",
            "applies_to": ["FHA", "VA", "USDA", "Conventional", "Jumbo"],
            "notes": "Varies significantly by loan program"
        },
        {
            "requirement_type": "EmploymentHistory",
            "min_value": 2.0,
            "max_value": None,
            "description": "Years of employment history required",
            "applies_to": ["FHA", "VA", "USDA", "Conventional", "Jumbo"],
            "notes": "2 years minimum, gaps may require explanation"
        }
    ]
    
    for req in requirements:
        query = """
        CREATE (qr:QualificationRequirement {
            requirement_type: $requirement_type,
            min_value: $min_value,
            max_value: $max_value,
            description: $description,
            applies_to: $applies_to,
            notes: $notes
        })
        """
        connection.execute_query(query, req)
        logger.debug(f"Created QualificationRequirement: {req['requirement_type']}")
    
    logger.info(f"✅ Loaded {len(requirements)} qualification requirements")


def load_process_steps():
    """Load mortgage process steps into Neo4j."""
    logger.info("Loading process steps...")
    connection = get_neo4j_connection()
    
    process_steps = [
        {
            "step_number": 1,
            "step_name": "Pre-qualification",
            "description": "Initial assessment of borrower's financial situation",
            "typical_duration_days": 1,
            "required_documents": ["Basic financial information", "Income estimate", "Debt summary"],
            "output": "Pre-qualification letter"
        },
        {
            "step_number": 2,
            "step_name": "Loan Application",
            "description": "Complete mortgage application submission",
            "typical_duration_days": 1,
            "required_documents": ["Completed application", "Initial documentation"],
            "output": "Application receipt and initial disclosures"
        },
        {
            "step_number": 3,
            "step_name": "Documentation Collection",
            "description": "Gather all required financial documents",
            "typical_duration_days": 7,
            "required_documents": ["Pay stubs", "Tax returns", "Bank statements", "Asset verification"],
            "output": "Complete documentation package"
        },
        {
            "step_number": 4,
            "step_name": "Processing",
            "description": "Loan processor reviews and verifies all documentation",
            "typical_duration_days": 7,
            "required_documents": ["All borrower documentation", "Property information"],
            "output": "Complete file ready for underwriting"
        },
        {
            "step_number": 5,
            "step_name": "Underwriting",
            "description": "Underwriter reviews and makes loan decision",
            "typical_duration_days": 3,
            "required_documents": ["Complete processed file", "Appraisal", "Title report"],
            "output": "Approval, conditional approval, or denial"
        },
        {
            "step_number": 6,
            "step_name": "Conditional Approval",
            "description": "Address any conditions from underwriter",
            "typical_duration_days": 5,
            "required_documents": ["Additional documentation as required"],
            "output": "Clear to close"
        },
        {
            "step_number": 7,
            "step_name": "Closing Preparation",
            "description": "Prepare all closing documents and coordinate",
            "typical_duration_days": 3,
            "required_documents": ["Final documents", "Closing disclosures"],
            "output": "Closing package ready"
        },
        {
            "step_number": 8,
            "step_name": "Closing",
            "description": "Final loan closing and funding",
            "typical_duration_days": 1,
            "required_documents": ["All closing documents", "Final walk-through"],
            "output": "Funded loan"
        }
    ]
    
    for step in process_steps:
        query = """
        CREATE (ps:ProcessStep {
            step_number: $step_number,
            step_name: $step_name,
            description: $description,
            typical_duration_days: $typical_duration_days,
            required_documents: $required_documents,
            output: $output
        })
        """
        connection.execute_query(query, step)
        logger.debug(f"Created ProcessStep: {step['step_name']}")
    
    logger.info(f"✅ Loaded {len(process_steps)} process steps")


def load_borrower_profiles():
    """Load borrower profile scenarios into Neo4j."""
    logger.info("Loading borrower profiles...")
    connection = get_neo4j_connection()
    
    profiles = [
        {
            "profile_name": "FirstTimeBuyer",
            "description": "First-time homebuyer with limited savings",
            "typical_credit_range": "580-680",
            "typical_down_payment": "3-5%",
            "recommended_programs": ["FHA", "VA", "USDA"],
            "key_considerations": [
                "Take advantage of first-time buyer programs",
                "Consider FHA loans for lower down payment",
                "Look into down payment assistance",
                "Focus on building credit before applying"
            ]
        },
        {
            "profile_name": "HighIncomeStrongCredit",
            "description": "High-income borrower with excellent credit",
            "typical_credit_range": "740+",
            "typical_down_payment": "10-20%+",
            "recommended_programs": ["Conventional", "Jumbo"],
            "key_considerations": [
                "May qualify for best interest rates",
                "Consider conventional loans to avoid mortgage insurance",
                "Jumbo loans for high-value properties",
                "Shop around for competitive rates"
            ]
        },
        {
            "profile_name": "SelfEmployed",
            "description": "Self-employed borrower with variable income",
            "typical_credit_range": "620-740",
            "typical_down_payment": "10-25%",
            "recommended_programs": ["Conventional", "FHA"],
            "key_considerations": [
                "Bank statement programs may be available",
                "2 years tax returns typically required",
                "May need larger down payment",
                "Consider asset-based qualification"
            ]
        },
        {
            "profile_name": "Veteran",
            "description": "Military veteran or active service member",
            "typical_credit_range": "620-740",
            "typical_down_payment": "0%",
            "recommended_programs": ["VA"],
            "key_considerations": [
                "VA loan is typically the best option",
                "No down payment or PMI required",
                "Certificate of eligibility required",
                "Can be used multiple times"
            ]
        }
    ]
    
    for profile in profiles:
        query = """
        CREATE (bp:BorrowerProfile {
            profile_name: $profile_name,
            description: $description,
            typical_credit_range: $typical_credit_range,
            typical_down_payment: $typical_down_payment,
            recommended_programs: $recommended_programs,
            key_considerations: $key_considerations
        })
        """
        connection.execute_query(query, profile)
        logger.debug(f"Created BorrowerProfile: {profile['profile_name']}")
    
    logger.info(f"✅ Loaded {len(profiles)} borrower profiles")


def load_reference_data():
    """
    Load all reference data that forms the foundation of the mortgage knowledge graph.
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("🏗️  Loading reference data...")
    
    try:
        load_loan_programs()
        load_qualification_requirements()
        load_process_steps()
        load_borrower_profiles()
        
        logger.info("✅ All reference data loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error loading reference data: {e}")
        return False


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    success = load_reference_data()
    if not success:
        exit(1)

