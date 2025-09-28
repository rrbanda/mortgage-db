"""
Mortgage Database Orchestrator

This module coordinates the loading of all mortgage data into Neo4j in the correct order
to build a comprehensive knowledge graph for AI agents.

Loading Order:
1. Clear existing data
2. Load reference data (loan programs, requirements) 
3. Load sample data (customers, properties, applications)
4. Load business rules (knowledge graph rules)
5. Create relationships (connect all entities)

Usage:
    python -m loaders.orchestrator
    
Or programmatically:
    from loaders.orchestrator import load_all_data
    load_all_data()
"""

import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.neo4j_connection import get_neo4j_connection, initialize_connection
from loaders.reference_data_loader import load_reference_data
from loaders.sample_data_loader import load_sample_data
from loaders.business_rules_loader import load_business_rules
from loaders.relationships_loader import create_all_relationships
from loaders.create_knowledge_graph import create_knowledge_graph
from loaders.agent_schema_alignment import apply_agent_schema_alignment

logger = logging.getLogger(__name__)


def align_schema_for_agents():
    """
    Align database schema for optimal AI agent tool compatibility.
    
    This function standardizes Application nodes with missing properties,
    adds performance indexes, and validates the schema alignment.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info("🤖 Aligning database schema for AI agent tools...")
        connection = get_neo4j_connection()
        
        if connection and apply_agent_schema_alignment(connection):
            logger.info("✅ Agent schema alignment completed successfully!")
            return True
        else:
            logger.error("❌ Failed to align schema for agent tools")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during agent schema alignment: {e}")
        return False


def clear_all_data():
    """Clear all existing mortgage data from Neo4j database."""
    logger.info("Clearing all existing data...")
    connection = get_neo4j_connection()
    
    clear_queries = [
        # Reference data and rules
        "MATCH (n:LoanProgram) DETACH DELETE n",
        "MATCH (n:QualificationRequirement) DETACH DELETE n", 
        "MATCH (n:DocumentRequirement) DETACH DELETE n",
        "MATCH (n:ProcessStep) DETACH DELETE n",
        "MATCH (n:BorrowerProfile) DETACH DELETE n",
        "MATCH (n:LoanLimit) DETACH DELETE n",
        "MATCH (n:BusinessRule) DETACH DELETE n",
        "MATCH (n:ScoringRule) DETACH DELETE n",
        "MATCH (n:QualificationThreshold) DETACH DELETE n",
        "MATCH (n:SpecialRequirement) DETACH DELETE n",
        "MATCH (n:ImprovementStrategy) DETACH DELETE n",
        "MATCH (n:DocumentVerificationRule) DETACH DELETE n",
        "MATCH (n:IncomeCalculationRule) DETACH DELETE n",
        "MATCH (n:PropertyAppraisalRule) DETACH DELETE n",
        "MATCH (n:UnderwritingRule) DETACH DELETE n",
        "MATCH (n:ComplianceRule) DETACH DELETE n",
        "MATCH (n:RatePricingRule) DETACH DELETE n",
        "MATCH (n:IDVerificationRule) DETACH DELETE n",
        "MATCH (n:ApplicationIntakeRule) DETACH DELETE n",
        
        # Sample data entities
        "MATCH (n:Person) DETACH DELETE n",
        "MATCH (n:Property) DETACH DELETE n",
        "MATCH (n:Application) DETACH DELETE n",
        "MATCH (n:Document) DETACH DELETE n",
        "MATCH (n:Company) DETACH DELETE n",
        "MATCH (n:Location) DETACH DELETE n"
    ]
    
    for query in clear_queries:
        try:
            connection.execute_query(query)
            logger.debug(f"Executed: {query}")
        except Exception as e:
            logger.error(f"Error executing clear query: {query} - {e}")
    
    logger.info("✅ All existing data cleared")


def load_all_data():
    """
    Main orchestrator function to load all mortgage data into Neo4j.
    
    This creates a comprehensive knowledge graph with:
    - Reference data for mortgage processing
    - Sample customer/application data for AI agent testing  
    - Business rules entities for decision making
    - Basic data relationships
    - Intelligent knowledge graph (semantic reasoning layer)
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("🚀 Starting complete mortgage database loading process...")
    
    # Initialize connection
    if not initialize_connection():
        logger.error("❌ Failed to connect to Neo4j database")
        return False
    
    try:
        # Phase 1: Clear existing data
        logger.info("\n📋 PHASE 1: Clearing existing data...")
        clear_all_data()
        
        # Phase 2: Load reference data (foundation)
        logger.info("\n📋 PHASE 2: Loading reference data...")
        if not load_reference_data():
            logger.error("❌ Failed to load reference data")
            return False
        
        # Phase 3: Load sample data (for AI agent testing)
        logger.info("\n📋 PHASE 3: Loading sample data...")
        if not load_sample_data():
            logger.error("❌ Failed to load sample data")
            return False
        
        # Phase 4: Load business rules (rule entities)
        logger.info("\n📋 PHASE 4: Loading business rules...")
        if not load_business_rules():
            logger.error("❌ Failed to load business rules")
            return False
        
        # Phase 5: Create basic relationships (data connections)
        logger.info("\n📋 PHASE 5: Creating basic relationships...")
        if not create_all_relationships():
            logger.error("❌ Failed to create basic relationships")
            return False
        
        # Phase 6: Create knowledge graph (intelligent semantic layer)
        logger.info("\n📋 PHASE 6: Creating knowledge graph...")
        if not create_knowledge_graph():
            logger.error("❌ Failed to create knowledge graph")
            return False

        # Phase 7: Agent Tool Schema Alignment (for AI agent compatibility)
        logger.info("\n📋 PHASE 7: Aligning schema for AI agent tools...")
        if not align_schema_for_agents():
            logger.error("❌ Failed to align schema for agent tools")
            return False

        logger.info("\n🎉 Mortgage database loading completed successfully!")
        logger.info("\n📊 Database now contains:")
        logger.info("   • Reference data (loan programs, requirements)")
        logger.info("   • Sample data (120+ customers, properties, applications)")
        logger.info("   • Business rules (rule entities and logic)")
        logger.info("   • Basic relationships (data connections)")
        logger.info("   • Knowledge graph (intelligent semantic reasoning layer)")
        logger.info("   • Agent-optimized schema (standardized properties & indexes)")

        return True
        
    except Exception as e:
        logger.error(f"❌ Error during data loading: {e}")
        return False


def verify_complete_load():
    """Verify that all data was loaded correctly."""
    logger.info("\n🔍 Verifying complete data load...")
    connection = get_neo4j_connection()
    
    verification_queries = [
        ("Loan Programs", "MATCH (n:LoanProgram) RETURN count(n) as count"),
        ("Qualification Requirements", "MATCH (n:QualificationRequirement) RETURN count(n) as count"),
        ("Process Steps", "MATCH (n:ProcessStep) RETURN count(n) as count"),
        ("Borrower Profiles", "MATCH (n:BorrowerProfile) RETURN count(n) as count"),
        ("People (Sample Data)", "MATCH (n:Person) RETURN count(n) as count"),
        ("Properties (Sample Data)", "MATCH (n:Property) RETURN count(n) as count"),
        ("Applications (Sample Data)", "MATCH (n:Application) RETURN count(n) as count"),
        ("Documents (Sample Data)", "MATCH (n:Document) RETURN count(n) as count"),
        ("Companies (Sample Data)", "MATCH (n:Company) RETURN count(n) as count"),
        ("Locations (Sample Data)", "MATCH (n:Location) RETURN count(n) as count"),
        ("Business Rules", "MATCH (n:BusinessRule) RETURN count(n) as count"),
        ("All Relationships", "MATCH ()-[r]->() RETURN count(r) as count")
    ]
    
    print("\n📊 Complete Data Load Verification:")
    print("=" * 60)
    
    for description, query in verification_queries:
        try:
            result = connection.execute_query(query)
            count = result.single()["count"]
            print(f"{description:.<30} {count:>8}")
        except Exception as e:
            print(f"{description:.<30} {'ERROR':>8} - {e}")
    
    print("=" * 60)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Load all data
    success = load_all_data()
    
    if success:
        verify_complete_load()
        print("\n✅ All data loaded successfully! Database ready for AI agents.")
    else:
        print("\n❌ Data loading failed. Check logs for details.")
        sys.exit(1)
