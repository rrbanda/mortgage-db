#!/usr/bin/env python3
"""
Generate Sample Mortgage Data

Creates realistic sample data for testing:
- 100+ unique borrowers
- Properties
- Applications
- Documents
- Companies/Employers
- Relationships

This generates data that matches our graph data models.
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict
import uuid
from faker import Faker
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    """JSON encoder that handles Decimal objects"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

# Initialize Faker for realistic data
fake = Faker('en_US')
Faker.seed(42)  # For reproducible results

def generate_ssn() -> str:
    """Generate a fake SSN in correct format"""
    return f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"

def generate_credit_score() -> int:
    """Generate realistic credit score"""
    return random.choices(
        population=[
            random.randint(300, 579),  # Poor
            random.randint(580, 619),  # Fair  
            random.randint(620, 679),  # Good
            random.randint(680, 739),  # Very Good
            random.randint(740, 850),  # Excellent
        ],
        weights=[10, 15, 25, 30, 20],  # Distribution weights
        k=1
    )[0]

def generate_income() -> int:
    """Generate realistic monthly income"""
    return random.choices(
        population=[
            random.randint(3000, 5000),    # Lower income
            random.randint(5001, 8000),    # Middle income
            random.randint(8001, 12000),   # Upper middle
            random.randint(12001, 20000),  # High income
            random.randint(20001, 50000),  # Very high income
        ],
        weights=[20, 35, 25, 15, 5],
        k=1
    )[0]

def generate_loan_amount(income: int, property_value: int) -> int:
    """Generate realistic loan amount based on income and property value"""
    max_loan_by_income = income * 12 * 5  # 5x annual income
    max_loan_by_property = int(property_value * 0.95)  # 95% LTV
    max_loan = min(max_loan_by_income, max_loan_by_property)
    return random.randint(int(max_loan * 0.7), max_loan)

def generate_property_value(zip_code: str) -> int:
    """Generate property value based on location"""
    # High-value zip codes (CA, NY, etc.)
    high_value_zips = ['94102', '94105', '10001', '10002', '90210', '90211']
    medium_value_zips = ['75001', '30301', '60601', '80202']
    
    if zip_code in high_value_zips:
        return random.randint(800000, 2000000)
    elif zip_code in medium_value_zips:
        return random.randint(400000, 800000)
    else:
        return random.randint(200000, 500000)

class SampleDataGenerator:
    def __init__(self):
        self.people = []
        self.properties = []
        self.applications = []
        self.documents = []
        self.companies = []
        self.locations = []
        self.relationships = []
        
        # Predefined companies for variety
        self.company_names = [
            "Google Inc", "Apple Inc", "Microsoft Corp", "Amazon", "Tesla Inc",
            "JP Morgan Chase", "Bank of America", "Wells Fargo", "Goldman Sachs",
            "Johnson & Johnson", "Pfizer Inc", "Walmart Inc", "Target Corp",
            "McDonald's Corp", "Starbucks Corp", "General Electric", "IBM Corp",
            "Intel Corp", "Cisco Systems", "Oracle Corp", "Salesforce Inc",
            "Netflix Inc", "Meta Platforms", "Twitter Inc", "Uber Technologies",
            "Kaiser Permanente", "Mayo Clinic", "City School District", "State University",
            "Local Government", "Fire Department", "Police Department", "Hospital System"
        ]
        
        # Property types and locations
        self.property_types = [
            "single_family_detached", "condominium", "townhouse", 
            "manufactured", "multi_family_2_4"
        ]
        
        self.occupancy_types = [
            "primary_residence", "second_home", "investment_property"
        ]
        
        # US Cities with ZIP codes
        self.locations_data = [
            {"city": "San Francisco", "state": "CA", "zip_code": "94102", "county": "San Francisco"},
            {"city": "San Francisco", "state": "CA", "zip_code": "94105", "county": "San Francisco"},
            {"city": "New York", "state": "NY", "zip_code": "10001", "county": "New York"},
            {"city": "New York", "state": "NY", "zip_code": "10002", "county": "New York"},
            {"city": "Los Angeles", "state": "CA", "zip_code": "90210", "county": "Los Angeles"},
            {"city": "Los Angeles", "state": "CA", "zip_code": "90211", "county": "Los Angeles"},
            {"city": "Chicago", "state": "IL", "zip_code": "60601", "county": "Cook"},
            {"city": "Chicago", "state": "IL", "zip_code": "60602", "county": "Cook"},
            {"city": "Houston", "state": "TX", "zip_code": "77001", "county": "Harris"},
            {"city": "Houston", "state": "TX", "zip_code": "77002", "county": "Harris"},
            {"city": "Dallas", "state": "TX", "zip_code": "75001", "county": "Dallas"},
            {"city": "Dallas", "state": "TX", "zip_code": "75002", "county": "Dallas"},
            {"city": "Phoenix", "state": "AZ", "zip_code": "85001", "county": "Maricopa"},
            {"city": "Phoenix", "state": "AZ", "zip_code": "85002", "county": "Maricopa"},
            {"city": "Atlanta", "state": "GA", "zip_code": "30301", "county": "Fulton"},
            {"city": "Atlanta", "state": "GA", "zip_code": "30302", "county": "Fulton"},
            {"city": "Denver", "state": "CO", "zip_code": "80202", "county": "Denver"},
            {"city": "Denver", "state": "CO", "zip_code": "80203", "county": "Denver"},
            {"city": "Miami", "state": "FL", "zip_code": "33101", "county": "Miami-Dade"},
            {"city": "Miami", "state": "FL", "zip_code": "33102", "county": "Miami-Dade"},
            {"city": "Seattle", "state": "WA", "zip_code": "98101", "county": "King"},
            {"city": "Seattle", "state": "WA", "zip_code": "98102", "county": "King"},
        ]

    def generate_locations(self):
        """Generate location entities"""
        for loc_data in self.locations_data:
            location = {
                "location_id": f"LOC_{loc_data['zip_code']}",
                "zip_code": loc_data['zip_code'],
                "city": loc_data['city'],
                "county": loc_data['county'],
                "state": loc_data['state'],
                "latitude": fake.latitude(),
                "longitude": fake.longitude(),
                "created_at": datetime.utcnow().isoformat()
            }
            self.locations.append(location)

    def generate_companies(self):
        """Generate employer/company entities"""
        for i, company_name in enumerate(self.company_names):
            location = random.choice(self.locations_data)
            company = {
                "company_id": f"COMP_{i+1:03d}",
                "company_name": company_name,
                "company_type": "employer",
                "address": fake.street_address(),
                "city": location['city'],
                "state": location['state'],
                "zip_code": location['zip_code'],
                "phone": fake.phone_number(),
                "created_at": datetime.utcnow().isoformat()
            }
            self.companies.append(company)

    def generate_people(self, count: int = 120):
        """Generate borrower entities"""
        for i in range(count):
            location = random.choice(self.locations_data)
            
            person = {
                "person_id": f"PERSON_{i+1:03d}",
                "ssn": generate_ssn(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "middle_name": fake.first_name() if random.random() < 0.6 else None,
                "email": fake.email(),
                "phone": fake.phone_number(),
                "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=75).isoformat(),
                "person_type": "borrower",
                
                # Address
                "current_address": fake.street_address(),
                "city": location['city'],
                "state": location['state'],
                "zip_code": location['zip_code'],
                "years_at_address": round(random.uniform(0.5, 15.0), 1),
                
                # Credit info
                "credit_score": generate_credit_score(),
                "credit_report_date": (datetime.utcnow() - timedelta(days=random.randint(1, 90))).isoformat(),
                
                "created_at": datetime.utcnow().isoformat()
            }
            self.people.append(person)

    def generate_properties(self):
        """Generate property entities for each person"""
        for i, person in enumerate(self.people[:100]):  # First 100 people get properties
            # Some people might have multiple properties
            num_properties = random.choices([1, 2, 3], weights=[80, 15, 5], k=1)[0]
            
            for j in range(num_properties):
                property_id = f"PROP_{i+1:03d}_{j+1}"
                
                # Use same or different location as person
                if j == 0 or random.random() < 0.3:
                    # Primary property in same location
                    location = {"city": person["city"], "state": person["state"], "zip_code": person["zip_code"]}
                else:
                    # Additional property in different location
                    location = random.choice(self.locations_data)
                
                property_value = generate_property_value(location["zip_code"])
                
                property_data = {
                    "property_id": property_id,
                    "address": fake.street_address(),
                    "city": location["city"],
                    "state": location["state"],
                    "zip_code": location["zip_code"],
                    
                    "property_type": random.choice(self.property_types),
                    "occupancy_type": random.choices(
                        self.occupancy_types, 
                        weights=[70, 20, 10], 
                        k=1
                    )[0],
                    
                    # Property characteristics
                    "square_feet": random.randint(800, 4000),
                    "bedrooms": random.randint(1, 5),
                    "bathrooms": random.choice([1, 1.5, 2, 2.5, 3, 3.5, 4]),
                    "year_built": random.randint(1950, 2023),
                    "lot_size": round(random.uniform(0.1, 2.0), 2),
                    
                    # Financial data
                    "estimated_value": property_value,
                    "purchase_price": int(property_value * random.uniform(0.95, 1.05)),
                    "appraised_value": None,  # Will be set during application process
                    "appraisal_date": None,
                    
                    "created_at": datetime.utcnow().isoformat()
                }
                self.properties.append(property_data)
                
                # Create property relationship
                self.relationships.append({
                    "relationship_type": "HAS_PROPERTY",
                    "from_node_id": person["person_id"],
                    "to_node_id": property_id,
                    "properties": {"relationship_date": datetime.utcnow().isoformat()}
                })

    def generate_applications(self):
        """Generate mortgage applications"""
        loan_purposes = ["purchase", "refinance", "cash_out_refinance", "renovation"]
        statuses = ["received", "in_review", "complete", "in_processing", "underwriting", "approved", "denied"]
        status_weights = [5, 10, 15, 20, 25, 20, 5]
        
        # Generate applications for first 100 people
        for i in range(100):
            person = self.people[i]
            person_properties = [p for p in self.properties if p["property_id"].startswith(f"PROP_{i+1:03d}")]
            
            if not person_properties:
                continue
                
            # Each person has 1-2 applications
            num_apps = random.choices([1, 2], weights=[85, 15], k=1)[0]
            
            for j in range(num_apps):
                app_id = f"APP_{i+1:03d}_{j+1}"
                property_data = random.choice(person_properties)
                
                monthly_income = generate_income()
                loan_amount = generate_loan_amount(monthly_income, property_data["estimated_value"])
                down_payment = property_data["estimated_value"] - loan_amount
                
                app_date = fake.date_between(start_date='-2y', end_date='today')
                status = random.choices(statuses, weights=status_weights, k=1)[0]
                
                application = {
                    "application_id": app_id,
                    "application_number": f"MTG{random.randint(100000, 999999)}",
                    
                    "loan_purpose": random.choice(loan_purposes),
                    "loan_amount": loan_amount,
                    "loan_term_months": random.choice([180, 240, 300, 360]),
                    
                    "status": status,
                    "application_date": app_date.isoformat(),
                    
                    "down_payment_amount": down_payment,
                    "down_payment_percentage": round(down_payment / property_data["estimated_value"], 3),
                    
                    "monthly_income": monthly_income,
                    "monthly_debts": random.randint(500, int(monthly_income * 0.4)),
                    
                    "submitted_date": (app_date + timedelta(days=random.randint(0, 5))).isoformat() if status != "received" else None,
                    "complete_date": (app_date + timedelta(days=random.randint(5, 15))).isoformat() if status in ["complete", "in_processing", "underwriting", "approved", "denied"] else None,
                    "approval_date": (app_date + timedelta(days=random.randint(15, 45))).isoformat() if status == "approved" else None,
                    "closing_date": None,
                    
                    "created_at": datetime.utcnow().isoformat()
                }
                self.applications.append(application)
                
                # Create application relationships
                self.relationships.append({
                    "relationship_type": "APPLIES_FOR",
                    "from_node_id": person["person_id"],
                    "to_node_id": app_id,
                    "properties": {"application_date": app_date.isoformat()}
                })
                
                self.relationships.append({
                    "relationship_type": "HAS_PROPERTY",
                    "from_node_id": app_id,
                    "to_node_id": property_data["property_id"],
                    "properties": {"loan_to_value": round(loan_amount / property_data["estimated_value"], 3)}
                })

    def generate_employment_relationships(self):
        """Generate employment relationships"""
        for person in self.people:
            # 90% of people have employment
            if random.random() < 0.9:
                company = random.choice(self.companies)
                self.relationships.append({
                    "relationship_type": "WORKS_AT",
                    "from_node_id": person["person_id"],
                    "to_node_id": company["company_id"],
                    "properties": {
                        "start_date": fake.date_between(start_date='-10y', end_date='-1m').isoformat(),
                        "position": fake.job(),
                        "employment_type": random.choice(["full_time", "part_time", "contract", "self_employed"])
                    }
                })

    def generate_documents(self):
        """Generate document entities"""
        doc_types = [
            "pay_stub", "w2", "tax_return", "bank_statement", 
            "employment_verification", "drivers_license", "property_appraisal"
        ]
        
        for app in self.applications:
            # Each application has 3-8 documents
            num_docs = random.randint(3, 8)
            selected_doc_types = random.sample(doc_types, min(num_docs, len(doc_types)))
            
            for i, doc_type in enumerate(selected_doc_types):
                doc_id = f"DOC_{app['application_id']}_{i+1:02d}"
                
                document = {
                    "document_id": doc_id,
                    "document_type": doc_type,
                    "document_name": f"{doc_type}_{fake.word()}.pdf",
                    
                    "verification_status": random.choices(
                        ["received", "pending_review", "verified", "rejected"],
                        weights=[10, 20, 60, 10],
                        k=1
                    )[0],
                    
                    "received_date": datetime.utcnow().isoformat(),
                    "verified_date": (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat() if random.random() < 0.7 else None,
                    
                    "file_path": f"/documents/{app['application_id']}/{doc_id}.pdf",
                    "file_size": random.randint(50000, 2000000),
                    "page_count": random.randint(1, 10),
                    
                    "created_at": datetime.utcnow().isoformat()
                }
                self.documents.append(document)
                
                # Create document relationship
                self.relationships.append({
                    "relationship_type": "REQUIRES",
                    "from_node_id": app["application_id"],
                    "to_node_id": doc_id,
                    "properties": {"required_date": datetime.utcnow().isoformat()}
                })

    def generate_location_relationships(self):
        """Generate location relationships"""
        for person in self.people:
            # Find matching location
            matching_location = next(
                (loc for loc in self.locations if loc["zip_code"] == person["zip_code"]), 
                None
            )
            if matching_location:
                self.relationships.append({
                    "relationship_type": "LOCATED_IN",
                    "from_node_id": person["person_id"],
                    "to_node_id": matching_location["location_id"],
                    "properties": {"address": person["current_address"]}
                })
        
        for prop in self.properties:
            matching_location = next(
                (loc for loc in self.locations if loc["zip_code"] == prop["zip_code"]), 
                None
            )
            if matching_location:
                self.relationships.append({
                    "relationship_type": "LOCATED_IN",
                    "from_node_id": prop["property_id"],
                    "to_node_id": matching_location["location_id"],
                    "properties": {"address": prop["address"]}
                })

    def generate_all_data(self):
        """Generate complete sample dataset"""
        print("🏗️  Generating locations...")
        self.generate_locations()
        
        print("🏢 Generating companies...")
        self.generate_companies()
        
        print("👥 Generating people (120 borrowers)...")
        self.generate_people(120)
        
        print("🏠 Generating properties...")
        self.generate_properties()
        
        print("📋 Generating applications...")
        self.generate_applications()
        
        print("👔 Generating employment relationships...")
        self.generate_employment_relationships()
        
        print("📄 Generating documents...")
        self.generate_documents()
        
        print("🗺️  Generating location relationships...")
        self.generate_location_relationships()
        
        print(f"✅ Generated complete dataset:")
        print(f"   👥 People: {len(self.people)}")
        print(f"   🏠 Properties: {len(self.properties)}")
        print(f"   📋 Applications: {len(self.applications)}")
        print(f"   📄 Documents: {len(self.documents)}")
        print(f"   🏢 Companies: {len(self.companies)}")
        print(f"   🗺️  Locations: {len(self.locations)}")
        print(f"   🔗 Relationships: {len(self.relationships)}")

    def save_data(self, output_dir: str = "."):
        """Save generated data to JSON files"""
        datasets = {
            "people": self.people,
            "properties": self.properties,
            "applications": self.applications,
            "documents": self.documents,
            "companies": self.companies,
            "locations": self.locations,
            "relationships": self.relationships
        }
        
        for filename, data in datasets.items():
            filepath = f"{output_dir}/{filename}.json"
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, cls=DecimalEncoder)
            print(f"💾 Saved {len(data)} records to {filepath}")

if __name__ == "__main__":
    generator = SampleDataGenerator()
    generator.generate_all_data()
    generator.save_data()
