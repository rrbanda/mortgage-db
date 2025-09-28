// Mortgage Database - Neo4j Graph Schema Definition
// Phase 1: Database Foundation
// This file creates the core graph schema for mortgage processing

// =====================================
// NODE CONSTRAINTS AND UNIQUE INDEXES
// =====================================

// Person node constraints
CREATE CONSTRAINT person_ssn_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.ssn IS UNIQUE;
CREATE CONSTRAINT person_id_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.person_id IS UNIQUE;

// Property node constraints  
CREATE CONSTRAINT property_id_unique IF NOT EXISTS FOR (p:Property) REQUIRE p.property_id IS UNIQUE;
CREATE CONSTRAINT property_address_unique IF NOT EXISTS FOR (p:Property) REQUIRE (p.address, p.city, p.state, p.zip) IS NODE KEY;

// Application node constraints
CREATE CONSTRAINT application_id_unique IF NOT EXISTS FOR (a:Application) REQUIRE a.application_id IS UNIQUE;
CREATE CONSTRAINT application_number_unique IF NOT EXISTS FOR (a:Application) REQUIRE a.application_number IS UNIQUE;

// Document node constraints
CREATE CONSTRAINT document_id_unique IF NOT EXISTS FOR (d:Document) REQUIRE d.document_id IS UNIQUE;

// Company/Employer node constraints
CREATE CONSTRAINT company_id_unique IF NOT EXISTS FOR (c:Company) REQUIRE c.company_id IS UNIQUE;

// Location node constraints
CREATE CONSTRAINT location_id_unique IF NOT EXISTS FOR (l:Location) REQUIRE l.location_id IS UNIQUE;
CREATE CONSTRAINT zipcode_unique IF NOT EXISTS FOR (l:Location) REQUIRE l.zip_code IS UNIQUE;

// Product node constraints
CREATE CONSTRAINT product_id_unique IF NOT EXISTS FOR (p:Product) REQUIRE p.product_id IS UNIQUE;

// =====================================
// PERFORMANCE INDEXES
// =====================================

// Person indexes for common queries
CREATE INDEX person_name_index IF NOT EXISTS FOR (p:Person) ON (p.last_name, p.first_name);
CREATE INDEX person_email_index IF NOT EXISTS FOR (p:Person) ON (p.email);
CREATE INDEX person_phone_index IF NOT EXISTS FOR (p:Person) ON (p.phone);

// Application indexes for common queries  
CREATE INDEX application_status_index IF NOT EXISTS FOR (a:Application) ON (a.status);
CREATE INDEX application_date_index IF NOT EXISTS FOR (a:Application) ON (a.application_date);
CREATE INDEX application_loan_amount_index IF NOT EXISTS FOR (a:Application) ON (a.loan_amount);

// Property indexes for searches
CREATE INDEX property_location_index IF NOT EXISTS FOR (p:Property) ON (p.city, p.state);
CREATE INDEX property_type_index IF NOT EXISTS FOR (p:Property) ON (p.property_type);
CREATE INDEX property_value_index IF NOT EXISTS FOR (p:Property) ON (p.estimated_value);

// Document indexes for verification
CREATE INDEX document_type_index IF NOT EXISTS FOR (d:Document) ON (d.document_type);
CREATE INDEX document_status_index IF NOT EXISTS FOR (d:Document) ON (d.verification_status);

// Location indexes for geographic queries
CREATE INDEX location_state_index IF NOT EXISTS FOR (l:Location) ON (l.state);
CREATE INDEX location_county_index IF NOT EXISTS FOR (l:Location) ON (l.county);

// =====================================
// RELATIONSHIP CONSTRAINTS
// =====================================

// Ensure relationship integrity
CREATE CONSTRAINT employment_relationship IF NOT EXISTS FOR ()-[r:WORKS_AT]-() REQUIRE r.start_date IS NOT NULL;
CREATE CONSTRAINT application_relationship IF NOT EXISTS FOR ()-[r:APPLIES_FOR]-() REQUIRE r.application_date IS NOT NULL;

// =====================================
// SCHEMA VERIFICATION QUERIES
// =====================================

// Verify schema creation (run after schema setup)
// CALL db.schema.visualization();
// CALL db.constraints();
// CALL db.indexes();

