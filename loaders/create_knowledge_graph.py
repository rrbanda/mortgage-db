"""
Knowledge Graph Creator for Mortgage Database

This module creates the intelligent knowledge graph by applying business rules,
generating semantic relationships, and creating inference-based connections
that enable AI agents to reason about mortgage data.

This is different from basic data relationships - it creates the "knowledge"
part of the knowledge graph through:
- Rule-based intelligent connections
- Semantic relationships 
- Business logic inferences
- Classification and categorization
- Risk assessment connections
- Compliance mapping

Usage:
    from loaders.create_knowledge_graph import create_knowledge_graph
    create_knowledge_graph()
"""

import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.neo4j_connection import get_neo4j_connection

logger = logging.getLogger(__name__)


def create_credit_score_knowledge():
    """Create intelligent relationships based on credit score analysis."""
    logger.info("Creating credit score knowledge relationships...")
    connection = get_neo4j_connection()
    
    # Connect people to risk categories based on credit scores
    risk_queries = [
        """
        MATCH (p:Person)
        WHERE p.credit_score >= 740
        SET p:ExcellentCredit
        WITH p
        MATCH (lp:LoanProgram)
        WHERE lp.name IN ["Conventional", "Jumbo"] 
        CREATE (p)-[:QUALIFIES_FOR {
            confidence: "high",
            reason: "excellent_credit",
            created_by: "knowledge_graph"
        }]->(lp)
        """,
        
        """
        MATCH (p:Person)
        WHERE p.credit_score >= 620 AND p.credit_score <= 739
        SET p:GoodCredit
        WITH p
        MATCH (lp:LoanProgram)
        WHERE lp.name IN ["Conventional", "FHA", "VA"]
        CREATE (p)-[:QUALIFIES_FOR {
            confidence: "medium",
            reason: "good_credit",
            created_by: "knowledge_graph"
        }]->(lp)
        """,
        
        """
        MATCH (p:Person)
        WHERE p.credit_score >= 580 AND p.credit_score <= 619
        SET p:FairCredit
        WITH p
        MATCH (lp:LoanProgram)
        WHERE lp.name IN ["FHA", "VA"]
        CREATE (p)-[:QUALIFIES_FOR {
            confidence: "low",
            reason: "fair_credit_needs_review",
            created_by: "knowledge_graph"
        }]->(lp)
        """
    ]
    
    for query in risk_queries:
        connection.execute_query(query)
    
    logger.info("✅ Credit score knowledge created")


def create_income_debt_knowledge():
    """Create intelligent relationships based on income and debt analysis."""
    logger.info("Creating income/debt ratio knowledge...")
    connection = get_neo4j_connection()
    
    # Calculate and create DTI-based knowledge
    dti_queries = [
        """
        MATCH (p:Person)-[:APPLIES_FOR]->(a:Application)
        WHERE a.monthly_income > 0 AND a.monthly_debts >= 0
        WITH p, a, (a.monthly_debts * 1.0 / a.monthly_income) as dti_ratio
        SET a.calculated_dti = dti_ratio
        
        // Create knowledge based on DTI
        WITH p, a, dti_ratio
        WHERE dti_ratio <= 0.28
        SET a:LowRiskDTI
        WITH a, dti_ratio
        MATCH (r:BusinessRule)
        WHERE r.rule_type = "DebtToIncomeCalculation"
        CREATE (a)-[:MEETS_CRITERIA {
            rule_type: "debt_to_income",
            dti_ratio: dti_ratio,
            risk_level: "low",
            created_by: "knowledge_graph"
        }]->(r)
        """,
        
        """
        MATCH (a:Application)
        WHERE a.calculated_dti > 0.28 AND a.calculated_dti <= 0.43
        SET a:MediumRiskDTI
        WITH a
        MATCH (r:BusinessRule)
        WHERE r.rule_type = "DebtToIncomeCalculation"
        CREATE (a)-[:REQUIRES_REVIEW {
            rule_type: "debt_to_income", 
            dti_ratio: a.calculated_dti,
            risk_level: "medium",
            created_by: "knowledge_graph"
        }]->(r)
        """,
        
        """
        MATCH (a:Application)
        WHERE a.calculated_dti > 0.43
        SET a:HighRiskDTI
        WITH a
        MATCH (r:BusinessRule)
        WHERE r.rule_type = "DebtToIncomeCalculation"
        CREATE (a)-[:LIKELY_DENIED {
            rule_type: "debt_to_income",
            dti_ratio: a.calculated_dti,
            risk_level: "high",
            created_by: "knowledge_graph"
        }]->(r)
        """
    ]
    
    for query in dti_queries:
        connection.execute_query(query)
    
    logger.info("✅ Income/debt knowledge created")


def create_loan_program_matching_knowledge():
    """Create intelligent loan program recommendations based on borrower characteristics."""
    logger.info("Creating intelligent loan program matching...")
    connection = get_neo4j_connection()
    
    # Complex loan matching logic
    matching_queries = [
        """
        // VA Loan eligibility inference
        MATCH (p:Person)-[:APPLIES_FOR]->(a:Application)
        MATCH (lp:LoanProgram {name: "VA"})
        WHERE p.person_type = "veteran" OR toLower(p.first_name) CONTAINS "military"
        CREATE (p)-[:RECOMMENDED_FOR {
            program: "VA",
            reason: "veteran_status",
            priority: "highest",
            down_payment_savings: a.loan_amount * 0.20,
            created_by: "knowledge_graph"
        }]->(lp)
        """,
        
        """
        // FHA recommendation for first-time buyers with limited funds
        MATCH (p:Person)-[:APPLIES_FOR]->(a:Application)
        MATCH (lp:LoanProgram {name: "FHA"})
        WHERE 
            a.down_payment_percentage <= 0.05 AND
            p.credit_score >= 580 AND p.credit_score <= 680 AND
            a.calculated_dti <= 0.57
        CREATE (p)-[:RECOMMENDED_FOR {
            program: "FHA",
            reason: "first_time_buyer_profile",
            priority: "high",
            benefits: ["Low down payment", "Flexible credit"],
            created_by: "knowledge_graph"
        }]->(lp)
        """,
        
        """
        // Jumbo loan qualification
        MATCH (p:Person)-[:APPLIES_FOR]->(a:Application)
        MATCH (lp:LoanProgram {name: "Jumbo"})
        WHERE 
            a.loan_amount > 766550 AND
            p.credit_score >= 700 AND
            a.down_payment_percentage >= 0.20 AND
            a.calculated_dti <= 0.38
        CREATE (p)-[:QUALIFIES_FOR {
            program: "Jumbo", 
            reason: "high_value_property_qualified",
            priority: "medium",
            loan_amount: a.loan_amount,
            created_by: "knowledge_graph"
        }]->(lp)
        """
    ]
    
    for query in matching_queries:
        connection.execute_query(query)
    
    logger.info("✅ Loan program matching knowledge created")


def create_risk_assessment_knowledge():
    """Create intelligent risk assessment relationships."""
    logger.info("Creating risk assessment knowledge...")
    connection = get_neo4j_connection()
    
    risk_queries = [
        """
        // Overall risk scoring
        MATCH (p:Person)-[:APPLIES_FOR]->(a:Application)
        WITH p, a,
            CASE 
                WHEN p.credit_score >= 740 THEN 10
                WHEN p.credit_score >= 680 THEN 8
                WHEN p.credit_score >= 620 THEN 6
                ELSE 3
            END as credit_score_points,
            CASE
                WHEN a.calculated_dti <= 0.28 THEN 10
                WHEN a.calculated_dti <= 0.36 THEN 8
                WHEN a.calculated_dti <= 0.43 THEN 5
                ELSE 2
            END as dti_points,
            CASE
                WHEN a.down_payment_percentage >= 0.20 THEN 10
                WHEN a.down_payment_percentage >= 0.10 THEN 7
                WHEN a.down_payment_percentage >= 0.05 THEN 5
                ELSE 3
            END as down_payment_points
            
        WITH p, a, (credit_score_points + dti_points + down_payment_points) as risk_score
        SET a.calculated_risk_score = risk_score
        
        // Create risk categories
        WITH p, a, risk_score
        SET a.risk_category = CASE
            WHEN risk_score >= 25 THEN "LowRisk"
            WHEN risk_score >= 18 AND risk_score < 25 THEN "MediumRisk"
            ELSE "HighRisk"
        END
        
        // Add appropriate labels based on risk score
        WITH p, a, risk_score
        FOREACH (_ IN CASE WHEN risk_score >= 25 THEN [1] ELSE [] END | SET a:LowRisk)
        FOREACH (_ IN CASE WHEN risk_score >= 18 AND risk_score < 25 THEN [1] ELSE [] END | SET a:MediumRisk)
        FOREACH (_ IN CASE WHEN risk_score < 18 THEN [1] ELSE [] END | SET a:HighRisk)
        
        RETURN count(a) as processed
        """,
        
        """
        // Connect risk categories to underwriting rules
        MATCH (a:Application:LowRisk)
        MATCH (rule:UnderwritingRule)
        WHERE rule.rule_type = "AutoApproval"
        CREATE (a)-[:ELIGIBLE_FOR {
            approval_type: "automated",
            created_by: "knowledge_graph"
        }]->(rule)
        """,
        
        """
        MATCH (a:Application:HighRisk)
        MATCH (rule:UnderwritingRule)
        WHERE rule.rule_type = "ManualReview"
        CREATE (a)-[:REQUIRES {
            review_type: "manual_underwriter",
            created_by: "knowledge_graph"
        }]->(rule)
        """
    ]
    
    for query in risk_queries:
        connection.execute_query(query)
    
    logger.info("✅ Risk assessment knowledge created")


def create_document_requirement_knowledge():
    """Create intelligent document requirement relationships."""
    logger.info("Creating document requirement knowledge...")
    connection = get_neo4j_connection()
    
    # Smart document requirements based on borrower characteristics
    doc_queries = [
        """
        // Self-employed borrowers need additional documentation
        MATCH (p:Person)-[:WORKS_AT]->(c:Company)
        MATCH (p)-[:APPLIES_FOR]->(a:Application)
        WHERE c.company_type = "sole_proprietorship" OR p.person_type = "self_employed"
        SET p:SelfEmployed
        WITH p, a
        MATCH (rule:DocumentVerificationRule)
        WHERE rule.rule_type = "SelfEmployedDocumentation"
        CREATE (a)-[:REQUIRES_ADDITIONAL {
            document_type: "tax_returns_2_years",
            reason: "self_employed_verification",
            created_by: "knowledge_graph"
        }]->(rule)
        """,
        
        """
        // High loan amounts require additional verification
        MATCH (a:Application)
        WHERE a.loan_amount > 500000
        WITH a
        MATCH (rule:DocumentVerificationRule)
        WHERE rule.rule_type = "AssetVerification"
        CREATE (a)-[:REQUIRES_ENHANCED {
            verification_level: "full_documentation",
            reason: "high_loan_amount",
            created_by: "knowledge_graph"
        }]->(rule)
        """,
        
        """
        // Low credit scores require additional documentation
        MATCH (p:Person:FairCredit)-[:APPLIES_FOR]->(a:Application)
        MATCH (rule:DocumentVerificationRule)
        WHERE rule.rule_type = "CreditExplanation"
        CREATE (a)-[:REQUIRES_EXPLANATION {
            explanation_type: "credit_issues",
            reason: "below_optimal_credit",
            created_by: "knowledge_graph"
        }]->(rule)
        """
    ]
    
    for query in doc_queries:
        connection.execute_query(query)
    
    logger.info("✅ Document requirement knowledge created")


def create_geographic_market_knowledge():
    """Create knowledge based on geographic market conditions."""
    logger.info("Creating geographic market knowledge...")
    connection = get_neo4j_connection()
    
    geo_queries = [
        """
        // Create market condition relationships
        MATCH (prop:Property)-[:LOCATED_IN]->(loc:Location)
        MATCH (a:Application)-[:HAS_PROPERTY]->(prop)
        WITH loc, count(a) as application_count, avg(prop.estimated_value) as avg_property_value
        WHERE application_count >= 3
        SET loc.market_activity = 
            CASE 
                WHEN application_count >= 10 THEN "hot"
                WHEN application_count >= 6 THEN "active" 
                ELSE "normal"
            END,
            loc.avg_property_value = avg_property_value
        """,
        
        """
        // Connect high-value markets to jumbo loan considerations
        MATCH (loc:Location)
        WHERE loc.avg_property_value > 600000
        SET loc:HighValueMarket
        WITH loc
        MATCH (prop:Property)-[:LOCATED_IN]->(loc)
        MATCH (a:Application)-[:HAS_PROPERTY]->(prop)
        MATCH (lp:LoanProgram {name: "Jumbo"})
        CREATE (a)-[:CONSIDER_PROGRAM {
            reason: "high_value_market",
            market_avg: loc.avg_property_value,
            created_by: "knowledge_graph"
        }]->(lp)
        """
    ]
    
    for query in geo_queries:
        connection.execute_query(query)
    
    logger.info("✅ Geographic market knowledge created")


def create_compliance_knowledge():
    """Create compliance and regulatory knowledge relationships."""
    logger.info("Creating compliance knowledge...")
    connection = get_neo4j_connection()
    
    compliance_queries = [
        """
        // ATR (Ability to Repay) rule compliance
        MATCH (a:Application)
        WHERE a.calculated_dti IS NOT NULL
        WITH a,
            CASE
                WHEN a.calculated_dti <= 0.43 THEN "compliant"
                ELSE "requires_qm_exception"
            END as atr_status
        SET a.atr_compliance = atr_status
        WITH a
        MATCH (rule:ComplianceRule)
        WHERE rule.rule_type = "ATR_QualifiedMortgage"
        CREATE (a)-[:COMPLIANCE_STATUS {
            rule_name: "ATR",
            status: a.atr_compliance,
            created_by: "knowledge_graph"
        }]->(rule)
        """,
        
        """
        // TRID compliance for closing timeline
        MATCH (a:Application)
        WHERE a.application_date IS NOT NULL
        SET a.required_closing_date = date(a.application_date) + duration({days: 45})
        WITH a
        MATCH (rule:ComplianceRule)
        WHERE rule.rule_type = "TRID_Compliance"
        CREATE (a)-[:SUBJECT_TO {
            rule_name: "TRID",
            deadline: a.required_closing_date,
            created_by: "knowledge_graph"
        }]->(rule)
        """
    ]
    
    for query in compliance_queries:
        connection.execute_query(query)
    
    logger.info("✅ Compliance knowledge created")


def create_knowledge_graph():
    """
    Create the intelligent knowledge graph by applying business logic,
    generating semantic relationships, and creating inference-based connections.
    
    This transforms raw data + business rules into a true knowledge graph
    that enables AI agents to reason about mortgage decisions.
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("🧠 Creating intelligent knowledge graph...")
    
    try:
        # Phase 1: Credit and risk analysis
        create_credit_score_knowledge()
        
        # Phase 2: Income and debt analysis  
        create_income_debt_knowledge()
        
        # Phase 3: Intelligent loan program matching
        create_loan_program_matching_knowledge()
        
        # Phase 4: Risk assessment and scoring
        create_risk_assessment_knowledge()
        
        # Phase 5: Document requirements intelligence
        create_document_requirement_knowledge()
        
        # Phase 6: Geographic market analysis
        create_geographic_market_knowledge()
        
        # Phase 7: Compliance and regulatory knowledge
        create_compliance_knowledge()
        
        logger.info("🎉 Knowledge graph creation completed successfully!")
        logger.info("\n📊 Knowledge Graph Features Created:")
        logger.info("   🎯 Credit score-based qualification logic")
        logger.info("   📊 DTI ratio risk assessment")  
        logger.info("   🏠 Intelligent loan program matching")
        logger.info("   ⚖️  Automated risk scoring")
        logger.info("   📋 Smart document requirement inference")
        logger.info("   🗺️  Geographic market analysis")
        logger.info("   ✅ Regulatory compliance mapping")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating knowledge graph: {e}")
        return False


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🧠 Mortgage Knowledge Graph Creator")
    print("=" * 50)
    print("Creating intelligent semantic relationships...")
    print("This enables AI agents to reason about mortgage decisions")
    print("=" * 50)
    
    success = create_knowledge_graph()
    if not success:
        exit(1)

