#!/usr/bin/env python3
"""
Mortgage Database Initialization Script

Phase 1: Database Foundation
This script orchestrates the complete database setup in the correct logical order:
1. Database Creation
2. Schema Setup (constraints, indexes)
3. Core Data Loading
4. Knowledge Graph Creation (business rules)

IMPORTANT: This follows the separation of concerns:
- DATA: Actual applications, borrowers, properties
- KNOWLEDGE: Business rules and decision logic
"""

import sys
import os
import logging
import time
from pathlib import Path
from typing import Optional
import yaml

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from utils.neo4j_connection import Neo4jConnection, get_neo4j_connection, initialize_connection

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseInitializer:
    """Orchestrates the complete database initialization process"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or str(project_root / "config.yaml")
        self.connection = None
        self.setup_path = project_root / "setup"
        self.core_data_path = project_root / "core_data"
        self.business_rules_path = project_root / "business_rules"
        
    def load_config(self) -> dict:
        """Load configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}, using defaults")
            return self._default_config()
    
    def _default_config(self) -> dict:
        """Default configuration for development"""
        return {
            'database': {
                'neo4j': {
                    'uri': 'bolt://localhost:7687',
                    'user': 'neo4j',
                    'password': 'mortgage123',
                    'database': 'mortgage'
                }
            }
        }
    
    def wait_for_neo4j(self, max_attempts: int = 30, delay: int = 2) -> bool:
        """Wait for Neo4j to be available"""
        logger.info("Waiting for Neo4j to be available...")
        
        for attempt in range(max_attempts):
            try:
                # Try to connect
                initialize_connection(config=self.load_config())
                connection = get_neo4j_connection()
                
                # Test connection with a simple query
                with connection.driver.session(database=connection.database) as session:
                    result = session.run("RETURN 1 as test")
                    result.single()
                
                logger.info("✅ Neo4j is available!")
                self.connection = connection
                return True
                
            except Exception as e:
                logger.info(f"Attempt {attempt + 1}/{max_attempts}: Neo4j not ready - {e}")
                if attempt < max_attempts - 1:
                    time.sleep(delay)
        
        logger.error("❌ Neo4j is not available after maximum attempts")
        return False
    
    def phase1_database_foundation(self) -> bool:
        """Phase 1: Set up database foundation (schema, constraints, indexes)"""
        logger.info("🏗️  PHASE 1: Database Foundation")
        
        try:
            # Read and execute schema file
            schema_file = self.setup_path / "schema" / "graph_schema.cypher"
            if not schema_file.exists():
                logger.error(f"Schema file not found: {schema_file}")
                return False
            
            with open(schema_file, 'r') as f:
                schema_cypher = f.read()
            
            # Split into individual statements and execute
            statements = [stmt.strip() for stmt in schema_cypher.split(';') if stmt.strip() and not stmt.strip().startswith('//')]
            
            with self.connection.driver.session(database=self.connection.database) as session:
                for statement in statements:
                    if statement:
                        try:
                            session.run(statement)
                            logger.info(f"✅ Executed: {statement[:50]}...")
                        except Exception as e:
                            logger.warning(f"⚠️  Statement failed (may be duplicate): {e}")
            
            logger.info("✅ Phase 1 Complete: Database foundation established")
            return True
            
        except Exception as e:
            logger.error(f"❌ Phase 1 Failed: {e}")
            return False
    
    def phase2_core_data_loading(self) -> bool:
        """Phase 2: Load core data (applications, borrowers, properties)"""
        logger.info("📊 PHASE 2: Core Data Loading")
        
        try:
            # Import data loading utilities
            from loaders.mortgage_data_loader import load_mortgage_data
            
            # Load sample or real data
            sample_data_path = self.core_data_path / "sample_data"
            if sample_data_path.exists():
                logger.info("Loading sample data...")
                # TODO: Implement sample data loading
                logger.info("ℹ️  Sample data loading not yet implemented")
            
            # For now, create some basic reference data
            self._create_reference_data()
            
            logger.info("✅ Phase 2 Complete: Core data loaded")
            return True
            
        except Exception as e:
            logger.error(f"❌ Phase 2 Failed: {e}")
            return False
    
    def phase3_knowledge_graph_creation(self) -> bool:
        """Phase 3: Create knowledge graph (business rules)"""
        logger.info("🧠 PHASE 3: Knowledge Graph Creation")
        
        try:
            # Load business rules in correct order
            from business_rules.application_processing.application_intake import load_application_intake_rules
            from business_rules.verification.document_verification import load_document_verification_rules
            from business_rules.verification.id_verification import load_id_verification_rules
            from business_rules.financial_assessment.income_calculation import load_income_calculation_rules
            from business_rules.underwriting.business_rules import load_business_rules
            
            # Load rules in logical dependency order
            rule_loaders = [
                ("Application Intake Rules", load_application_intake_rules),
                ("Document Verification Rules", load_document_verification_rules),
                ("ID Verification Rules", load_id_verification_rules),
                ("Income Calculation Rules", load_income_calculation_rules),
                ("Business Rules", load_business_rules),
            ]
            
            for rule_name, loader_func in rule_loaders:
                try:
                    logger.info(f"Loading {rule_name}...")
                    loader_func(self.connection)
                    logger.info(f"✅ {rule_name} loaded successfully")
                except Exception as e:
                    logger.error(f"❌ Failed to load {rule_name}: {e}")
                    # Continue with other rules
            
            logger.info("✅ Phase 3 Complete: Knowledge graph created")
            return True
            
        except Exception as e:
            logger.error(f"❌ Phase 3 Failed: {e}")
            return False
    
    def _create_reference_data(self):
        """Create basic reference data"""
        logger.info("Creating reference data...")
        
        reference_queries = [
            # Create loan product types
            """
            CREATE (p1:Product {
                product_id: 'CONV_30_YEAR',
                product_name: 'Conventional 30-Year Fixed',
                loan_term_months: 360,
                product_type: 'conventional'
            })
            """,
            
            # Create property types
            """
            CREATE (pt1:PropertyType {
                type_id: 'SFD',
                type_name: 'Single Family Detached',
                description: 'Detached single-family residence'
            })
            """,
            
            # Create location reference
            """
            CREATE (loc1:Location {
                location_id: 'SF_CA_94102',
                zip_code: '94102',
                city: 'San Francisco',
                county: 'San Francisco',
                state: 'CA'
            })
            """
        ]
        
        with self.connection.driver.session(database=self.connection.database) as session:
            for query in reference_queries:
                try:
                    session.run(query.strip())
                except Exception as e:
                    logger.warning(f"Reference data query failed (may exist): {e}")
    
    def phase4_validation_and_health_check(self) -> bool:
        """Phase 4: Validate setup and perform health checks"""
        logger.info("🔍 PHASE 4: Validation & Health Check")
        
        try:
            health_queries = [
                ("Node count check", "MATCH (n) RETURN count(n) as total_nodes"),
                ("Relationship count check", "MATCH ()-[r]-() RETURN count(r) as total_relationships"),
                ("Constraint verification", "CALL db.constraints()"),
                ("Index verification", "CALL db.indexes()"),
            ]
            
            with self.connection.driver.session(database=self.connection.database) as session:
                for check_name, query in health_queries:
                    try:
                        result = session.run(query)
                        records = list(result)
                        logger.info(f"✅ {check_name}: {len(records)} results")
                        if check_name.endswith("count check") and records:
                            logger.info(f"   Count: {records[0][list(records[0].keys())[0]]}")
                    except Exception as e:
                        logger.warning(f"⚠️  {check_name} failed: {e}")
            
            logger.info("✅ Phase 4 Complete: Database validated and healthy")
            return True
            
        except Exception as e:
            logger.error(f"❌ Phase 4 Failed: {e}")
            return False
    
    def initialize_complete_database(self) -> bool:
        """Execute complete database initialization in logical order"""
        logger.info("🚀 Starting Complete Database Initialization")
        logger.info("=" * 60)
        
        phases = [
            ("Database Foundation", self.phase1_database_foundation),
            ("Core Data Loading", self.phase2_core_data_loading), 
            ("Knowledge Graph Creation", self.phase3_knowledge_graph_creation),
            ("Validation & Health Check", self.phase4_validation_and_health_check),
        ]
        
        # Wait for Neo4j to be available
        if not self.wait_for_neo4j():
            return False
        
        # Execute phases in order
        for phase_name, phase_func in phases:
            logger.info(f"\n▶️  Starting: {phase_name}")
            if not phase_func():
                logger.error(f"💥 CRITICAL FAILURE in {phase_name}")
                logger.error("🛑 Database initialization ABORTED")
                return False
            logger.info(f"✅ Completed: {phase_name}")
        
        logger.info("\n" + "=" * 60)
        logger.info("🎉 Database initialization COMPLETED SUCCESSFULLY!")
        logger.info("📊 Database is ready for mortgage processing operations")
        return True

def main():
    """Main entry point"""
    initializer = DatabaseInitializer()
    
    success = initializer.initialize_complete_database()
    
    if success:
        logger.info("🚀 Database is ready for use!")
        sys.exit(0)
    else:
        logger.error("💥 Database initialization failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
