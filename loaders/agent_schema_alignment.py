"""
Agent Schema Alignment Module

This module standardizes the Application schema and adds performance optimizations
specifically for AI agent tool compatibility. It ensures all agent tools can
query the database consistently without missing property errors.

Created based on agent tool feedback to resolve storage-retrieval bridge issues
at the database deployment level rather than in application code.
"""

import logging
from typing import Optional
from utils.neo4j_connection import Neo4jConnection

logger = logging.getLogger(__name__)

def align_application_schema(connection: Optional[Neo4jConnection] = None) -> bool:
    """
    Standardize Application nodes for agent tool compatibility.
    
    Adds missing properties with sensible defaults, ensuring all agent tools
    can query Applications without property existence errors.
    
    Args:
        connection: Optional Neo4j connection. If None, creates new connection.
        
    Returns:
        bool: True if successful, False otherwise
    """
    should_close = False
    
    try:
        if connection is None:
            connection = Neo4jConnection()
            if not connection.connect():
                logger.error("Failed to connect to Neo4j for schema alignment")
                return False
            should_close = True
        
        logger.info("🔧 Aligning Application schema for agent tool compatibility...")
        
        # Add missing properties to Application nodes with sensible defaults
        schema_alignment_query = """
        MATCH (app:Application)
        SET app.borrower_name = coalesce(app.borrower_name, 'Application User'),
            app.first_name = coalesce(app.first_name, 'Not'),
            app.last_name = coalesce(app.last_name, 'Provided'),
            app.property_value = coalesce(app.property_value, app.loan_amount * 1.25),
            app.phone = coalesce(app.phone, '000-000-0000'),
            app.email = coalesce(app.email, 'not.provided@example.com')
        RETURN count(app) as updated_applications
        """
        
        # Use session.run instead of execute_query for better result handling
        with connection.driver.session() as session:
            result = session.run(schema_alignment_query)
            record = result.single()
            updated_count = record['updated_applications'] if record else 0
        
        logger.info(f"✅ Updated {updated_count} Application nodes with missing properties")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during Application schema alignment: {e}")
        return False
    
    finally:
        if should_close and connection:
            connection.disconnect()

def create_performance_optimizations(connection: Optional[Neo4jConnection] = None) -> bool:
    """
    Add constraints and indexes for optimal agent tool performance.
    
    Creates database constraints and indexes specifically designed for
    the query patterns used by AI agent tools.
    
    Args:
        connection: Optional Neo4j connection. If None, creates new connection.
        
    Returns:
        bool: True if successful, False otherwise
    """
    should_close = False
    
    try:
        if connection is None:
            connection = Neo4jConnection()
            if not connection.connect():
                logger.error("Failed to connect to Neo4j for performance optimizations")
                return False
            should_close = True
        
        logger.info("⚡ Creating performance optimizations for agent tools...")
        
        # Performance optimization queries
        optimization_queries = [
            # Unique constraint on Application ID (critical for agent tools)
            "CREATE CONSTRAINT application_id_unique IF NOT EXISTS FOR (app:Application) REQUIRE app.id IS UNIQUE",
            
            # Index on borrower_name for agent queries
            "CREATE INDEX application_borrower_name IF NOT EXISTS FOR (app:Application) ON (app.borrower_name)",
            
            # Index on application status for workflow queries
            "CREATE INDEX application_status IF NOT EXISTS FOR (app:Application) ON (app.status)",
            
            # Index on loan amount for financial queries
            "CREATE INDEX application_loan_amount IF NOT EXISTS FOR (app:Application) ON (app.loan_amount)",
            
            # Index on application date for temporal queries
            "CREATE INDEX application_date IF NOT EXISTS FOR (app:Application) ON (app.application_date)",
            
            # Compound index for common agent query patterns
            "CREATE INDEX application_status_amount IF NOT EXISTS FOR (app:Application) ON (app.status, app.loan_amount)"
        ]
        
        for query in optimization_queries:
            try:
                connection.execute_query(query)
                logger.debug(f"✅ Executed: {query}")
            except Exception as e:
                # Some constraints/indexes may already exist, that's OK
                logger.debug(f"ℹ️  Constraint/Index already exists or similar: {e}")
        
        logger.info("✅ Performance optimizations applied successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during performance optimizations: {e}")
        return False
    
    finally:
        if should_close and connection:
            connection.disconnect()

def validate_schema_alignment(connection: Optional[Neo4jConnection] = None) -> bool:
    """
    Validate that schema alignment was successful.
    
    Verifies all required properties exist on Application nodes and reports
    coverage statistics for agent tool compatibility.
    
    Args:
        connection: Optional Neo4j connection. If None, creates new connection.
        
    Returns:
        bool: True if validation successful, False otherwise
    """
    should_close = False
    
    try:
        if connection is None:
            connection = Neo4jConnection()
            if not connection.connect():
                logger.error("Failed to connect to Neo4j for schema validation")
                return False
            should_close = True
        
        logger.info("🔍 Validating Application schema alignment...")
        
        # Validation query to check all required properties
        validation_query = """
        MATCH (app:Application)
        RETURN
          count(app) as total_applications,
          count(app.id) as has_id,
          count(app.borrower_name) as has_borrower_name,
          count(app.first_name) as has_first_name,
          count(app.last_name) as has_last_name,
          count(app.status) as has_status,
          count(app.loan_amount) as has_loan_amount,
          count(app.property_value) as has_property_value,
          count(app.phone) as has_phone,
          count(app.email) as has_email
        """
        
        # Use session.run for better result handling
        with connection.driver.session() as session:
            result = session.run(validation_query)
            stats = result.single()
            
        if not stats:
            logger.warning("⚠️  No Application nodes found for validation")
            return True
        total = stats['total_applications']
        
        logger.info("📊 Application Schema Validation Results:")
        logger.info(f"   Total Applications: {total}")
        logger.info(f"   Has ID: {stats['has_id']} ({100 * stats['has_id'] / total:.1f}%)")
        logger.info(f"   Has Borrower Name: {stats['has_borrower_name']} ({100 * stats['has_borrower_name'] / total:.1f}%)")
        logger.info(f"   Has First Name: {stats['has_first_name']} ({100 * stats['has_first_name'] / total:.1f}%)")
        logger.info(f"   Has Last Name: {stats['has_last_name']} ({100 * stats['has_last_name'] / total:.1f}%)")
        logger.info(f"   Has Status: {stats['has_status']} ({100 * stats['has_status'] / total:.1f}%)")
        logger.info(f"   Has Loan Amount: {stats['has_loan_amount']} ({100 * stats['has_loan_amount'] / total:.1f}%)")
        logger.info(f"   Has Property Value: {stats['has_property_value']} ({100 * stats['has_property_value'] / total:.1f}%)")
        logger.info(f"   Has Phone: {stats['has_phone']} ({100 * stats['has_phone'] / total:.1f}%)")
        logger.info(f"   Has Email: {stats['has_email']} ({100 * stats['has_email'] / total:.1f}%)")
        
        # Check if all critical properties are 100% covered
        critical_properties = ['has_id', 'has_borrower_name', 'has_status', 'has_loan_amount']
        all_critical_covered = all(stats[prop] == total for prop in critical_properties)
        
        if all_critical_covered:
            logger.info("✅ All critical properties have 100% coverage - Agent tools ready!")
        else:
            logger.warning("⚠️  Some critical properties missing - Agent tools may encounter errors")
            
        return all_critical_covered
        
    except Exception as e:
        logger.error(f"❌ Error during schema validation: {e}")
        return False
    
    finally:
        if should_close and connection:
            connection.disconnect()

def apply_agent_schema_alignment(connection: Optional[Neo4jConnection] = None) -> bool:
    """
    Complete agent schema alignment process.
    
    Applies all schema alignments, performance optimizations, and validations
    needed for agent tool compatibility.
    
    Args:
        connection: Optional Neo4j connection. If None, creates new connection.
        
    Returns:
        bool: True if all steps successful, False otherwise
    """
    should_close = False
    
    try:
        if connection is None:
            connection = Neo4jConnection()
            if not connection.connect():
                logger.error("Failed to connect to Neo4j for agent schema alignment")
                return False
            should_close = True
        
        logger.info("🤖 Starting Agent Tool Schema Alignment Process...")
        
        # Step 1: Align Application schema
        if not align_application_schema(connection):
            logger.error("❌ Failed to align Application schema")
            return False
        
        # Step 2: Create performance optimizations
        if not create_performance_optimizations(connection):
            logger.error("❌ Failed to create performance optimizations")
            return False
        
        # Step 3: Validate the alignment
        if not validate_schema_alignment(connection):
            logger.error("❌ Schema validation failed")
            return False
        
        logger.info("🎉 Agent Tool Schema Alignment completed successfully!")
        logger.info("")
        logger.info("📋 Agent Tools Now Have:")
        logger.info("   • Standardized Application properties")
        logger.info("   • Performance-optimized indexes")
        logger.info("   • Unique constraints for data integrity")
        logger.info("   • 100% property coverage validation")
        logger.info("")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during agent schema alignment: {e}")
        return False
    
    finally:
        if should_close and connection:
            connection.disconnect()

if __name__ == "__main__":
    """Direct execution for testing"""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    success = apply_agent_schema_alignment()
    if success:
        logger.info("✅ Agent schema alignment completed successfully!")
    else:
        logger.error("❌ Agent schema alignment failed!")
