"""
Mortgage Data Loader - Simplified Interface

This is now a simplified interface that uses the new modular loader architecture.
For detailed control, use the individual loaders or orchestrator directly.

New Modular Structure:
- orchestrator.py           - Main coordinator for all loading operations
- reference_data_loader.py  - Core mortgage reference data  
- sample_data_loader.py     - Customer/application sample data
- business_rules_loader.py  - Business rules knowledge graph
- relationships_loader.py   - Entity relationships

Usage (backward compatible):
    python -m loaders.mortgage_data_loader
    
Or programmatically:
    from loaders.mortgage_data_loader import load_mortgage_data
    load_mortgage_data()

For more control, use the orchestrator directly:
    from loaders.orchestrator import load_all_data
    load_all_data()
"""

import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from loaders.orchestrator import load_all_data, verify_complete_load

logger = logging.getLogger(__name__)


def load_mortgage_data():
    """
    Main function to load all mortgage data into Neo4j.
    
    This is a backward-compatible wrapper around the new modular loader system.
    It loads:
    - Reference data (loan programs, requirements, profiles)
    - Sample data (customers, properties, applications)  
    - Business rules (comprehensive knowledge graph)
    - Relationships (connecting all entities)
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("🏠 Starting mortgage data loading using modular architecture...")
    return load_all_data()


def verify_data_load():
    """Verify that data was loaded correctly."""
    return verify_complete_load()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🏠 Mortgage Database Loader")
    print("=" * 50)
    print("Using new modular architecture:")
    print("  📋 Reference Data Loader")
    print("  👥 Sample Data Loader")  
    print("  🧠 Business Rules Loader")
    print("  🔗 Relationships Loader")
    print("=" * 50)
    
    # Load all data using orchestrator
    success = load_mortgage_data()
    
    if success:
        verify_data_load()
        print("\n✅ All data loaded successfully!")
        print("\n🎯 Database ready for AI agents!")
        print("\nNext steps:")
        print("  • Test with Podman: make deploy-podman")  
        print("  • Run queries to explore the knowledge graph")
        print("  • Connect AI agents for mortgage processing")
    else:
        print("\n❌ Data loading failed. Check logs for details.")
        sys.exit(1)