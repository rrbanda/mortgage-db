"""
Sample Data Loader for Mortgage Database

This module loads sample customer, property, application, and document data
for AI agent testing and graph database demonstration purposes.

Usage:
    from loaders.sample_data_loader import load_sample_data
    load_sample_data()
"""

import logging
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.neo4j_connection import get_neo4j_connection

logger = logging.getLogger(__name__)


def load_locations_from_json(locations_data, connection):
    """Load location entities from JSON data."""
    for location in locations_data:
        query = """
        CREATE (l:Location {
            location_id: $location_id,
            zip_code: $zip_code,
            city: $city,
            county: $county,
            state: $state,
            latitude: $latitude,
            longitude: $longitude,
            created_at: $created_at
        })
        """
        connection.execute_query(query, location)


def load_companies_from_json(companies_data, connection):
    """Load company entities from JSON data.""" 
    for company in companies_data:
        query = """
        CREATE (c:Company {
            company_id: $company_id,
            company_name: $company_name,
            company_type: $company_type,
            address: $address,
            city: $city,
            state: $state,
            zip_code: $zip_code,
            phone: $phone,
            created_at: $created_at
        })
        """
        connection.execute_query(query, company)


def load_people_from_json(people_data, connection):
    """Load person entities from JSON data."""
    for person in people_data:
        query = """
        CREATE (p:Person {
            person_id: $person_id,
            ssn: $ssn,
            first_name: $first_name,
            last_name: $last_name,
            middle_name: $middle_name,
            email: $email,
            phone: $phone,
            date_of_birth: $date_of_birth,
            person_type: $person_type,
            current_address: $current_address,
            city: $city,
            state: $state,
            zip_code: $zip_code,
            years_at_address: $years_at_address,
            credit_score: $credit_score,
            credit_report_date: $credit_report_date,
            created_at: $created_at
        })
        """
        connection.execute_query(query, person)


def load_properties_from_json(properties_data, connection):
    """Load property entities from JSON data."""
    for property_data in properties_data:
        query = """
        CREATE (prop:Property {
            property_id: $property_id,
            address: $address,
            city: $city,
            state: $state,
            zip_code: $zip_code,
            property_type: $property_type,
            occupancy_type: $occupancy_type,
            square_feet: $square_feet,
            bedrooms: $bedrooms,
            bathrooms: $bathrooms,
            year_built: $year_built,
            lot_size: $lot_size,
            estimated_value: $estimated_value,
            purchase_price: $purchase_price,
            appraised_value: $appraised_value,
            appraisal_date: $appraisal_date,
            created_at: $created_at
        })
        """
        connection.execute_query(query, property_data)


def load_applications_from_json(applications_data, connection):
    """Load application entities from JSON data."""
    for application in applications_data:
        query = """
        CREATE (app:Application {
            application_id: $application_id,
            id: $application_id,
            application_number: $application_number,
            loan_purpose: $loan_purpose,
            loan_amount: $loan_amount,
            loan_term_months: $loan_term_months,
            status: $status,
            application_date: $application_date,
            down_payment_amount: $down_payment_amount,
            down_payment_percentage: $down_payment_percentage,
            monthly_income: $monthly_income,
            monthly_debts: $monthly_debts,
            submitted_date: $submitted_date,
            complete_date: $complete_date,
            approval_date: $approval_date,
            closing_date: $closing_date,
            created_at: $created_at
        })
        """
        connection.execute_query(query, application)


def load_documents_from_json(documents_data, connection):
    """Load document entities from JSON data."""
    for document in documents_data:
        query = """
        CREATE (doc:Document {
            document_id: $document_id,
            document_type: $document_type,
            document_name: $document_name,
            verification_status: $verification_status,
            received_date: $received_date,
            verified_date: $verified_date,
            file_path: $file_path,
            file_size: $file_size,
            page_count: $page_count,
            created_at: $created_at
        })
        """
        connection.execute_query(query, document)


def load_sample_data():
    """
    Load sample data (people, properties, applications, documents) from JSON files 
    for AI agent testing and graph database demonstration.
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("📋 Loading sample data for AI agent testing...")
    
    try:
        # Get path to sample data directory
        current_dir = Path(__file__).parent
        sample_data_dir = current_dir.parent / "core_data" / "sample_data"
        
        if not sample_data_dir.exists():
            logger.warning(f"⚠️  Sample data directory not found: {sample_data_dir}")
            logger.info("Sample data loading skipped - no demonstration data available")
            return True  # Not a failure, just no sample data
        
        connection = get_neo4j_connection()
        
        # Load data files in order (to handle dependencies)
        data_files = [
            ("locations.json", load_locations_from_json),
            ("companies.json", load_companies_from_json),
            ("people.json", load_people_from_json),
            ("properties.json", load_properties_from_json),
            ("applications.json", load_applications_from_json),
            ("documents.json", load_documents_from_json)
        ]
        
        for filename, loader_func in data_files:
            file_path = sample_data_dir / filename
            if file_path.exists():
                logger.info(f"Loading {filename}...")
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    loader_func(data, connection)
                    count = len(data) if isinstance(data, list) else "N/A"
                    logger.info(f"✅ Loaded {count} records from {filename}")
                except Exception as e:
                    logger.error(f"❌ Error loading {filename}: {e}")
                    return False
            else:
                logger.warning(f"⚠️  Sample data file not found: {filename}")
        
        logger.info("✅ All sample data loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error loading sample data: {e}")
        return False


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    success = load_sample_data()
    if not success:
        exit(1)

