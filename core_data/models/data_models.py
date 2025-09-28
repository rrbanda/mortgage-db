"""
Core Data Models for Mortgage Database

Phase 2: Core Data Loading
This module defines the data models for actual mortgage application data.
These are NOT business rules - these are data structures for real entities.

Separation of Concerns:
- DATA: Person, Property, Application (what exists)
- KNOWLEDGE: Business rules, qualification logic (what we know about the data)
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# =====================================
# CORE ENTITY MODELS
# =====================================

class PersonType(str, Enum):
    BORROWER = "borrower"
    CO_BORROWER = "co_borrower"
    GUARANTOR = "guarantor"
    REAL_ESTATE_AGENT = "real_estate_agent"
    LOAN_OFFICER = "loan_officer"
    APPRAISER = "appraiser"

class Person(BaseModel):
    """Core Person entity - represents actual people in the system"""
    person_id: str = Field(..., description="Unique person identifier")
    ssn: str = Field(..., description="Social Security Number")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    middle_name: Optional[str] = None
    email: str = Field(..., description="Email address")
    phone: str = Field(..., description="Phone number")
    date_of_birth: datetime = Field(..., description="Date of birth")
    person_type: PersonType = Field(..., description="Type of person in mortgage process")
    
    # Address information
    current_address: str = Field(..., description="Current street address")
    city: str = Field(..., description="Current city")
    state: str = Field(..., description="Current state")
    zip_code: str = Field(..., description="Current ZIP code")
    years_at_address: float = Field(..., description="Years at current address")
    
    # Credit information (data, not rules)
    credit_score: Optional[int] = Field(None, description="Current credit score")
    credit_report_date: Optional[datetime] = Field(None, description="Credit report date")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class PropertyType(str, Enum):
    SINGLE_FAMILY_DETACHED = "single_family_detached"
    CONDOMINIUM = "condominium"
    TOWNHOUSE = "townhouse"
    MANUFACTURED = "manufactured"
    MULTI_FAMILY_2_4 = "multi_family_2_4"

class OccupancyType(str, Enum):
    PRIMARY_RESIDENCE = "primary_residence"
    SECOND_HOME = "second_home"
    INVESTMENT_PROPERTY = "investment_property"

class Property(BaseModel):
    """Core Property entity - represents actual properties"""
    property_id: str = Field(..., description="Unique property identifier")
    address: str = Field(..., description="Property street address")
    city: str = Field(..., description="Property city")
    state: str = Field(..., description="Property state")
    zip_code: str = Field(..., description="Property ZIP code")
    
    property_type: PropertyType = Field(..., description="Type of property")
    occupancy_type: OccupancyType = Field(..., description="Intended occupancy")
    
    # Property characteristics (data)
    square_feet: Optional[int] = Field(None, description="Square footage")
    bedrooms: Optional[int] = Field(None, description="Number of bedrooms")
    bathrooms: Optional[float] = Field(None, description="Number of bathrooms")
    year_built: Optional[int] = Field(None, description="Year property was built")
    lot_size: Optional[float] = Field(None, description="Lot size in acres")
    
    # Financial data
    estimated_value: Optional[int] = Field(None, description="Estimated property value")
    purchase_price: Optional[int] = Field(None, description="Purchase price (if buying)")
    appraised_value: Optional[int] = Field(None, description="Appraised value")
    appraisal_date: Optional[datetime] = Field(None, description="Appraisal date")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class ApplicationStatus(str, Enum):
    RECEIVED = "received"
    IN_REVIEW = "in_review"
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"
    IN_PROCESSING = "in_processing"
    UNDERWRITING = "underwriting"
    APPROVED = "approved"
    DENIED = "denied"
    CLOSED = "closed"
    WITHDRAWN = "withdrawn"

class LoanPurpose(str, Enum):
    PURCHASE = "purchase"
    REFINANCE = "refinance"
    CASH_OUT_REFINANCE = "cash_out_refinance"
    CONSTRUCTION = "construction"
    RENOVATION = "renovation"

class Application(BaseModel):
    """Core Application entity - represents actual mortgage applications"""
    application_id: str = Field(..., description="Unique application identifier")
    application_number: str = Field(..., description="Human-readable application number")
    
    # Application details (data)
    loan_purpose: LoanPurpose = Field(..., description="Purpose of the loan")
    loan_amount: int = Field(..., description="Requested loan amount")
    loan_term_months: int = Field(default=360, description="Loan term in months")
    
    # Status tracking (data)
    status: ApplicationStatus = Field(default=ApplicationStatus.RECEIVED)
    application_date: datetime = Field(default_factory=datetime.utcnow)
    
    # Financial data from application
    down_payment_amount: Optional[int] = Field(None, description="Down payment amount")
    down_payment_percentage: Optional[float] = Field(None, description="Down payment percentage")
    
    # Income data (actual numbers, not calculation rules)
    monthly_income: Optional[int] = Field(None, description="Monthly income reported")
    monthly_debts: Optional[int] = Field(None, description="Monthly debt payments")
    
    # Processing dates (data)
    submitted_date: Optional[datetime] = None
    complete_date: Optional[datetime] = None
    approval_date: Optional[datetime] = None
    closing_date: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class DocumentType(str, Enum):
    PAY_STUB = "pay_stub"
    W2 = "w2"
    TAX_RETURN = "tax_return"
    BANK_STATEMENT = "bank_statement"
    EMPLOYMENT_VERIFICATION = "employment_verification"
    DRIVERS_LICENSE = "drivers_license"
    PROPERTY_APPRAISAL = "property_appraisal"
    PURCHASE_CONTRACT = "purchase_contract"
    INSURANCE_POLICY = "insurance_policy"

class DocumentStatus(str, Enum):
    RECEIVED = "received"
    PENDING_REVIEW = "pending_review"
    VERIFIED = "verified"
    REJECTED = "rejected"
    EXPIRED = "expired"

class Document(BaseModel):
    """Core Document entity - represents actual documents"""
    document_id: str = Field(..., description="Unique document identifier")
    document_type: DocumentType = Field(..., description="Type of document")
    document_name: str = Field(..., description="Document filename or description")
    
    verification_status: DocumentStatus = Field(default=DocumentStatus.RECEIVED)
    received_date: datetime = Field(default_factory=datetime.utcnow)
    verified_date: Optional[datetime] = None
    
    # Document metadata (data)
    file_path: Optional[str] = Field(None, description="Path to document file")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    page_count: Optional[int] = Field(None, description="Number of pages")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class Company(BaseModel):
    """Core Company entity - represents employers, lenders, service providers"""
    company_id: str = Field(..., description="Unique company identifier")
    company_name: str = Field(..., description="Company name")
    company_type: str = Field(..., description="Type of company (employer, lender, etc.)")
    
    # Company details (data)
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    phone: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class Location(BaseModel):
    """Core Location entity - represents geographic locations"""
    location_id: str = Field(..., description="Unique location identifier")
    zip_code: str = Field(..., description="ZIP code")
    city: str = Field(..., description="City name")
    county: str = Field(..., description="County name")
    state: str = Field(..., description="State name")
    
    # Geographic data
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

# =====================================
# RELATIONSHIP MODELS
# =====================================

class RelationshipType(str, Enum):
    APPLIES_FOR = "APPLIES_FOR"
    CO_SIGNS = "CO_SIGNS"  
    WORKS_AT = "WORKS_AT"
    LOCATED_IN = "LOCATED_IN"
    HAS_PROPERTY = "HAS_PROPERTY"
    REQUIRES = "REQUIRES"
    VERIFIES = "VERIFIES"
    REFERS = "REFERS"

class Relationship(BaseModel):
    """Base relationship model"""
    relationship_type: RelationshipType
    from_node_id: str
    to_node_id: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# =====================================
# DATA VALIDATION UTILITIES
# =====================================

class DataValidator:
    """Validates actual data (not business rules)"""
    
    @staticmethod
    def validate_ssn(ssn: str) -> bool:
        """Validate SSN format (data validation, not business rules)"""
        import re
        return bool(re.match(r'^\d{3}-\d{2}-\d{4}$', ssn))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re
        return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
    
    @staticmethod
    def validate_zip_code(zip_code: str) -> bool:
        """Validate ZIP code format"""
        import re
        return bool(re.match(r'^\d{5}(-\d{4})?$', zip_code))

# =====================================
# EXPORT ALL MODELS
# =====================================

__all__ = [
    'Person', 'PersonType',
    'Property', 'PropertyType', 'OccupancyType',
    'Application', 'ApplicationStatus', 'LoanPurpose',
    'Document', 'DocumentType', 'DocumentStatus',
    'Company', 'Location',
    'Relationship', 'RelationshipType',
    'DataValidator'
]

