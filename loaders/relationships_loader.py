"""
Relationships Loader for Mortgage Database

This module creates all relationships between entities in the mortgage knowledge graph.
This includes relationships between reference data entities and sample data entities.

Usage:
    from loaders.relationships_loader import create_all_relationships
    create_all_relationships()
"""

import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.neo4j_connection import get_neo4j_connection

logger = logging.getLogger(__name__)


def create_reference_data_relationships():
    """Create relationships between reference data entities."""
    logger.info("Creating reference data relationships...")
    connection = get_neo4j_connection()
    
    # Connect borrower profiles to recommended loan programs
    relationship_queries = [
        # FirstTimeBuyer -> FHA, VA, USDA
        """
        MATCH (bp:BorrowerProfile {profile_name: "FirstTimeBuyer"})
        MATCH (lp:LoanProgram)
        WHERE lp.name IN ["FHA", "VA", "USDA"]
        CREATE (bp)-[:RECOMMENDS {priority: "high"}]->(lp)
        """,
        
        # HighIncomeStrongCredit -> Conventional, Jumbo
        """
        MATCH (bp:BorrowerProfile {profile_name: "HighIncomeStrongCredit"})
        MATCH (lp:LoanProgram)
        WHERE lp.name IN ["Conventional", "Jumbo"]
        CREATE (bp)-[:RECOMMENDS {priority: "high"}]->(lp)
        """,
        
        # SelfEmployed -> Conventional, FHA
        """
        MATCH (bp:BorrowerProfile {profile_name: "SelfEmployed"})
        MATCH (lp:LoanProgram)
        WHERE lp.name IN ["Conventional", "FHA"]
        CREATE (bp)-[:RECOMMENDS {priority: "medium"}]->(lp)
        """,
        
        # Veteran -> VA
        """
        MATCH (bp:BorrowerProfile {profile_name: "Veteran"})
        MATCH (lp:LoanProgram {name: "VA"})
        CREATE (bp)-[:RECOMMENDS {priority: "highest"}]->(lp)
        """,
        
        # ADD RECOMMENDED_FOR relationships for AI agent tool compatibility
        """
        MATCH (bp:BorrowerProfile), (lp:LoanProgram)
        WHERE 
          (bp.profile_name = 'FirstTimeBuyer' AND lp.name IN ['FHA', 'VA', 'USDA', 'Conventional']) OR
          (bp.profile_name = 'HighIncomeStrongCredit' AND lp.name IN ['Conventional', 'Jumbo']) OR  
          (bp.profile_name = 'SelfEmployed' AND lp.name IN ['Conventional', 'FHA']) OR
          (bp.profile_name = 'Veteran' AND lp.name IN ['VA', 'FHA'])
        CREATE (bp)-[:RECOMMENDED_FOR]->(lp)
        """,
        
        # Connect process steps in sequence
        """
        MATCH (ps1:ProcessStep), (ps2:ProcessStep)
        WHERE ps2.step_number = ps1.step_number + 1
        CREATE (ps1)-[:NEXT_STEP]->(ps2)
        """,
        
        # Connect qualification requirements to loan programs
        """
        MATCH (qr:QualificationRequirement), (lp:LoanProgram)
        WHERE lp.name IN qr.applies_to
        CREATE (qr)-[:APPLIES_TO]->(lp)
        """,
        
        # ADD HAS_REQUIREMENT relationships for AI agent tool compatibility
        """
        MATCH (lp:LoanProgram), (qr:QualificationRequirement)
        WHERE lp.name IN qr.applies_to
        AND NOT EXISTS((lp)-[:HAS_REQUIREMENT]->(qr))
        CREATE (lp)-[:HAS_REQUIREMENT]->(qr)
        """
    ]
    
    for query in relationship_queries:
        try:
            connection.execute_query(query)
            logger.debug(f"Executed relationship query successfully")
        except Exception as e:
            logger.error(f"Error creating relationship: {e}")
    
    logger.info("✅ Reference data relationships created")


def create_sample_data_relationships():
    """Create relationships for sample data entities based on data patterns."""
    logger.info("Creating sample data relationships...")
    connection = get_neo4j_connection()
    
    try:
        # Create basic relationships that AI agents need for mortgage processing
        
        # 1. Connect people to their locations
        logger.info("Creating Person->Location relationships...")
        query = """
        MATCH (p:Person), (l:Location)
        WHERE p.zip_code = l.zip_code
        CREATE (p)-[:LOCATED_IN]->(l)
        """
        connection.execute_query(query)
        logger.debug("✅ Created Person->Location relationships")
        
        # 2. Connect properties to their locations  
        logger.info("Creating Property->Location relationships...")
        query = """
        MATCH (prop:Property), (l:Location)
        WHERE prop.zip_code = l.zip_code
        CREATE (prop)-[:LOCATED_IN]->(l)
        """
        connection.execute_query(query)
        logger.debug("✅ Created Property->Location relationships")
        
        # 3. Connect companies to their locations
        logger.info("Creating Company->Location relationships...")
        query = """
        MATCH (c:Company), (l:Location)
        WHERE c.zip_code = l.zip_code
        CREATE (c)-[:LOCATED_IN]->(l)
        """
        connection.execute_query(query)
        logger.debug("✅ Created Company->Location relationships")
        
        # 4. Connect people to companies (employment) - random assignment for demo
        logger.info("Creating Person->Company employment relationships...")
        query = """
        MATCH (p:Person), (c:Company)
        WITH p, c
        WHERE rand() < 0.8  // 80% of people have employment
        WITH p, c ORDER BY rand() LIMIT 1
        CREATE (p)-[:WORKS_AT {
            position: 'Employee',
            start_date: date() - duration({days: toInteger(rand() * 1825)}),
            employment_type: 'full_time'
        }]->(c)
        """
        connection.execute_query(query)
        logger.debug("✅ Created Person->Company employment relationships")
        
        # 5. Connect people to applications (based on naming pattern APP_001_1 -> PERSON_001)
        logger.info("Creating Person->Application relationships...")
        query = """
        MATCH (p:Person), (a:Application)
        WHERE a.application_id STARTS WITH 'APP_' + substring(p.person_id, 7) + '_'
        CREATE (p)-[:APPLIES_FOR {application_date: a.application_date}]->(a)
        """
        connection.execute_query(query)
        logger.debug("✅ Created Person->Application relationships")
        
        # 6. Connect applications to properties (based on naming pattern)
        logger.info("Creating Application->Property relationships...")
        query = """
        MATCH (a:Application), (prop:Property)
        WHERE prop.property_id STARTS WITH 'PROP_' + substring(a.application_id, 5, 3) + '_'
        CREATE (a)-[:HAS_PROPERTY {
            loan_to_value: round((a.loan_amount * 1.0 / prop.estimated_value) * 1000) / 1000
        }]->(prop)
        """
        connection.execute_query(query)
        logger.debug("✅ Created Application->Property relationships")
        
        # 7. Connect applications to documents (based on naming pattern DOC_APP_xxx)
        logger.info("Creating Application->Document relationships...")
        query = """
        MATCH (a:Application), (d:Document)
        WHERE d.document_id CONTAINS a.application_id
        CREATE (a)-[:REQUIRES {required_date: d.received_date}]->(d)
        """
        connection.execute_query(query)
        logger.debug("✅ Created Application->Document relationships")
        
        # 8. Connect applications to loan programs based on loan characteristics
        logger.info("Creating Application->LoanProgram relationships...")
        query = """
        MATCH (a:Application), (lp:LoanProgram)
        WHERE 
            (lp.name = "FHA" AND a.down_payment_percentage <= 0.05) OR
            (lp.name = "VA" AND a.down_payment_percentage = 0.0) OR
            (lp.name = "Conventional" AND a.down_payment_percentage >= 0.03) OR
            (lp.name = "USDA" AND a.down_payment_percentage = 0.0) OR
            (lp.name = "Jumbo" AND a.loan_amount > 766550)
        WITH a, lp LIMIT 200  // Limit to prevent too many relationships
        CREATE (a)-[:ELIGIBLE_FOR]->(lp)
        """
        connection.execute_query(query)
        logger.debug("✅ Created Application->LoanProgram relationships")
        
        # 9. Connect people to borrower profiles based on characteristics
        logger.info("Creating Person->BorrowerProfile relationships...")
        query = """
        MATCH (p:Person), (bp:BorrowerProfile)
        WHERE 
            (bp.profile_name = "FirstTimeBuyer" AND p.credit_score >= 580 AND p.credit_score <= 680) OR
            (bp.profile_name = "HighIncomeStrongCredit" AND p.credit_score >= 740) OR
            (bp.profile_name = "SelfEmployed" AND p.credit_score >= 620 AND p.credit_score <= 740)
        WITH p, bp LIMIT 300  // Limit relationships
        CREATE (p)-[:MATCHES_PROFILE]->(bp)
        """
        connection.execute_query(query)
        logger.debug("✅ Created Person->BorrowerProfile relationships")
        
        logger.info("✅ All sample data relationships created successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error creating sample relationships: {e}")
        raise


def create_knowledge_graph_relationships():
    """Create relationships between business rules and other entities."""
    logger.info("Creating knowledge graph relationships...")
    connection = get_neo4j_connection()
    
    try:
        # Connect business rules to applications (for AI agent processing)
        logger.info("Creating business rule relationships...")
        
        # Connect applications to relevant business rules based on loan characteristics
        query = """
        MATCH (a:Application), (rule:BusinessRule)
        WHERE 
            a.monthly_income IS NOT NULL AND 
            rule.rule_type IN ['CreditScoreAssessment', 'DebtToIncomeCalculation', 'IncomeVerification']
        WITH a, rule
        WHERE rand() < 0.3  // 30% of applications connect to each relevant rule
        CREATE (a)-[:SUBJECT_TO {
            applies_date: a.application_date,
            rule_version: '1.0'
        }]->(rule)
        """
        connection.execute_query(query)
        
        # Connect loan programs to relevant business rules
        query = """
        MATCH (lp:LoanProgram), (rule:BusinessRule)
        WHERE rule.rule_type IN ['LoanProgramRequirements', 'QualificationGuidelines']
        CREATE (lp)-[:GOVERNED_BY]->(rule)
        """
        connection.execute_query(query)
        
        logger.info("✅ Knowledge graph relationships created")
        
    except Exception as e:
        logger.warning(f"⚠️  Some knowledge graph relationships may not be created: {e}")
        # This is not critical failure since business rules structure may vary


def create_all_relationships():
    """
    Create all relationships in the mortgage knowledge graph.
    
    This includes:
    - Reference data relationships (loan programs, profiles, requirements)
    - Sample data relationships (people, properties, applications, documents)
    - Knowledge graph relationships (business rules connections)
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("🔗 Creating all relationships in the knowledge graph...")
    
    try:
        create_reference_data_relationships()
        create_sample_data_relationships()
        create_knowledge_graph_relationships()
        
        logger.info("✅ All relationships created successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating relationships: {e}")
        return False


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    success = create_all_relationships()
    if not success:
        exit(1)

