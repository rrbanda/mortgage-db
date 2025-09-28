# Mortgage Database System

A comprehensive **Graph Database** system built on Neo4j, specifically designed for AI agents and mortgage specialists to leverage relationship-driven insights and intelligent business rule processing.

## 🎯 Why Graph Database for Mortgage Processing?

### The Technical Rationale

Mortgage processing is fundamentally about **relationships and context**, not just individual data points. Here's why Neo4j provides concrete value:

#### 1. **Relationship-Centric Business Logic**
Mortgage decisions depend on how entities connect, not just their individual attributes:

```cypher
// Qualification logic: Does borrower's employment support this loan amount?
MATCH (person:Person)-[:WORKS_AT]->(company:Company),
      (person)-[:APPLIES_FOR]->(app:Application)
WHERE app.loan_amount > (person.monthly_income * company.stability_multiplier * 60)
RETURN app.application_id, "income_insufficient" as reason
```

This type of multi-entity reasoning is natural in Cypher but requires complex JOINs in SQL.

#### 2. **Dynamic Rule Application**
Business rules often apply based on relationship patterns:

```cypher
// Self-employed borrowers need different documentation
MATCH (person:Person)-[:WORKS_AT]->(company:Company),
      (person)-[:APPLIES_FOR]->(app:Application)
WHERE company.company_type = "sole_proprietorship" 
CREATE (app)-[:REQUIRES_ADDITIONAL]->(doc:DocumentRequirement {type: "tax_returns_2_years"})
```

#### 3. **Schema Evolution Without Migration**
Mortgage regulations change frequently. Adding new relationship types or entity properties requires no schema migration:

```cypher
// New regulation: Track property flood zones
MATCH (prop:Property)-[:LOCATED_IN]->(location:Location)
WHERE location.flood_zone_updated_2024 = true
SET prop:FloodZoneReview
```

#### 4. **Natural Query Expression**
Mortgage business logic maps directly to graph patterns:

```cypher
// Find similar approved applications for comparison
MATCH (app:Application {status: "approved"})
MATCH (current:Application {application_id: $app_id})
WHERE abs(app.credit_score - current.credit_score) <= 50
  AND abs(app.loan_amount - current.loan_amount) <= 50000
MATCH (app)-[:ELIGIBLE_FOR]->(program:LoanProgram)
RETURN program.name, count(*) as similar_approvals
```

#### 5. **Knowledge Inference**
Create new insights from existing relationship patterns:

```cypher
// Automatically identify qualification patterns
MATCH (person:Person)-[:APPLIES_FOR]->(app:Application {status: "approved"})
MATCH (app)-[:ELIGIBLE_FOR]->(program:LoanProgram)
WHERE person.credit_score >= 740 AND app.down_payment_percentage >= 0.20
CREATE (person)-[:QUALIFIES_FOR {confidence: "high", reason: "pattern_match"}]->(program)
```

### **Real Results from Our Working System**

Here are actual query results from the deployed mortgage database, demonstrating the graph database value:

**Database Contents (Top 10 Node Types):**
```
Node Type               | Count
----------------------- | -----
Document                | 611
Property                | 123  
Person                  | 120
Application             | 112
IDVerificationRule      | 40
Company                 | 33
DocumentVerificationRule| 24
IncomeCalculationRule   | 23
Location                | 22
UnderwritingRule        | 16
```

**Knowledge Graph Intelligence - Risk Assessment:**
```
Risk Category    | Applications
---------------- | ------------
LowRisk          | 60
MediumRisk       | 47  
HighRisk         | 3
```

**Relationship Network (Top Relationship Types):**
```
Relationship Type        | Count
------------------------ | -----
REQUIRES                 | 611
LOCATED_IN               | 276
QUALIFIES_FOR            | 154
SUBJECT_TO               | 152
MATCHES_PROFILE          | 137
APPLIES_FOR              | 110
```

**Credit Score-Based Qualification Inference:**
```
Borrower           | Program | Credit | Confidence | Reason
------------------ | ------- | ------ | ---------- | ---------------
Ashley Long        | FHA     |    737 | medium     | good_credit
Ashley Long        | VA      |    737 | medium     | good_credit  
Rebecca Carlson    | VA      |    730 | medium     | good_credit
Rebecca Carlson    | FHA     |    730 | medium     | good_credit
Nathaniel Williams | VA      |    728 | medium     | good_credit
Nathaniel Williams | FHA     |    728 | medium     | good_credit
```

**Summary of Graph Database Value:**
- ✅ **1,500+ relationships** connecting 1,000+ entities in meaningful patterns
- ✅ **Intelligent risk assessment** automatically categorized 110 applications  
- ✅ **Knowledge inference** created 154 credit-based qualification relationships
- ✅ **Multi-dimensional analysis** through relationship traversals
- ✅ **Pattern-based business logic** working across connected entities

## 🏗️ Architecture Overview

**Complete End-to-End System** for AI agent integration:
- **Multi-environment deployment** (Podman containers, OpenShift ready)
- **Comprehensive data models** (Person, Property, Application, Document, Company)
- **Business rules engine** with 200+ production-ready rules
- **Knowledge graph** with intelligent relationship inference
- **Sample data** (120+ customers, 110+ applications, 600+ documents)
- **AI agent tools** with direct Cypher access

## 📁 Current Project Structure

```
├── README.md                  # This comprehensive guide
├── config.yaml.example       # Configuration template
├── requirements.txt           # Python dependencies
├── 
├── core_data/                 # Data models and sample data
│   ├── models/               # Pydantic models (Person, Property, Application, etc.)
│   ├── reference_data/       # Static data (loan products, property types, locations)
│   └── sample_data/          # 120+ borrowers, applications, properties for testing
├── 
├── business_rules/            # 200+ Production business rules
│   ├── application_processing/  # Application intake and document handling (12 rules)
│   ├── verification/           # Identity, document verification (64 rules)
│   ├── financial_assessment/   # Income, debt, property analysis (31 rules)
│   ├── risk_scoring/          # Risk assessment and qualification (14 rules)
│   ├── compliance/            # Regulatory compliance (23 rules)
│   ├── underwriting/          # Underwriting decision rules (27 rules)
│   ├── pricing/              # Rate and fee calculations (16 rules)
│   └── process_optimization/ # Workflow improvements (5 rules)
├── 
├── loaders/                   # 7-Phase data loading system  
│   ├── orchestrator.py       # Master coordinator for all data loading
│   ├── reference_data_loader.py   # Loan programs, requirements, profiles
│   ├── sample_data_loader.py      # Customer and application data
│   ├── business_rules_loader.py   # Business rule entities
│   ├── relationships_loader.py    # Data relationships and connections
│   ├── create_knowledge_graph.py  # Intelligent semantic reasoning layer
│   └── mortgage_data_loader.py    # Legacy compatibility wrapper
├── 
├── utils/                     # Core database utilities
│   ├── neo4j_connection.py   # Neo4j connection management with config
│   └── application_storage.py # Mortgage application CRUD operations
└── 
└── deployment/                # Container deployment configurations
    ├── neo4j/podman/         # Podman container deployment
    │   ├── build.sh          # Container build script
    │   ├── deploy.sh         # Pod deployment script
    │   └── *.example         # Configuration templates
    └── neo4j/openshift/      # OpenShift deployment templates
```

## 🗂️ Graph Data Model

### Core Node Types
- **Person**: Borrowers, co-borrowers, guarantors, real estate agents, loan officers
- **Property**: Residential properties with location and characteristics  
- **Application**: Mortgage applications with status tracking and workflow
- **Document**: All documents with metadata and verification status
- **Company**: Employers, lenders, service providers with location data
- **Location**: Geographic entities (cities, counties, states, zip codes)
- **LoanProgram**: Available loan products (FHA, VA, Conventional, etc.)
- **BorrowerProfile**: Borrower categorization for targeting
- **BusinessRule**: All business rules as queryable entities

### Key Relationship Types
- **APPLIES_FOR**: Person → Application (application ownership)
- **WORKS_AT**: Person → Company (employment relationships)
- **LOCATED_IN**: Property/Person/Company → Location (geographic connections)
- **HAS_PROPERTY**: Application → Property (loan subject property)
- **REQUIRES**: Application → Document (required documentation)
- **MATCHES_PROFILE**: Person → BorrowerProfile (borrower categorization)  
- **ELIGIBLE_FOR**: Application → LoanProgram (qualification status)
- **SUBJECT_TO**: Application → BusinessRule (applicable rules)
- **MEETS_CRITERIA**: Application → BusinessRule (rule satisfaction)

## 🤖 AI Agent Integration

### Direct Cypher Access for Intelligent Processing

**AI agents can directly execute Cypher queries** for complete mortgage processing workflow:

#### 🤖 **Application Intake Agent**
```cypher
// Create new mortgage application with borrower
CREATE (p:Person {
    person_id: "PER_2025_001",
    first_name: "Sarah", 
    last_name: "Johnson",
    email: "sarah.johnson@email.com",
    credit_score: 750,
    monthly_income: 9200
})
CREATE (app:Application {
    application_id: "APP_2025_001",
    loan_amount: 425000,
    loan_purpose: "purchase",
    status: "received",
    application_date: datetime(),
    monthly_income: 9200,
    down_payment_percentage: 0.20
})
CREATE (p)-[:APPLIES_FOR]->(app)
RETURN app.application_id, app.status
```

#### 🤖 **Document Verification Agent**
```cypher
// Check what documents are still needed
MATCH (app:Application {application_id: "APP_2025_001"})
MATCH (rule:DocumentVerificationRule)
WHERE rule.rule_type = "PAY_STUB_STANDARD"
OPTIONAL MATCH (app)-[:REQUIRES]->(d:Document {document_type: "pay_stub"})
WITH app, rule, d
WHERE d IS NULL
RETURN rule.description as missing_document, rule.requirements
```

#### 🤖 **Underwriting Agent**
```cypher
// Apply business rules and make qualification decision
MATCH (app:Application {application_id: "APP_2025_001"})
WITH app, (app.monthly_debts * 1.0 / app.monthly_income) as dti_ratio
SET app.dti_ratio = dti_ratio,
    app.qualification_status = CASE
        WHEN dti_ratio <= 0.28 THEN "qualified"
        WHEN dti_ratio <= 0.43 THEN "qualified_with_conditions" 
        ELSE "not_qualified"
    END,
    app.status = CASE 
        WHEN dti_ratio <= 0.28 THEN "approved"
        WHEN dti_ratio <= 0.43 THEN "conditional_approval"
        ELSE "denied" 
    END
RETURN app.qualification_status, app.status
```

#### 🤖 **Risk Assessment Agent**  
```cypher
// Find similar applications for risk comparison
MATCH (target:Application {application_id: "APP_2025_001"})
MATCH (similar:Application)
WHERE similar.status = "approved" 
  AND abs(similar.credit_score - target.credit_score) <= 50
  AND abs(similar.loan_amount - target.loan_amount) <= 50000
MATCH (similar)-[:ELIGIBLE_FOR]->(lp:LoanProgram)
RETURN similar.application_id, similar.credit_score, 
       similar.loan_amount, lp.name as recommended_program
LIMIT 5
```

#### 🤖 **Workflow Management Agent**
```cypher
// Find applications needing attention
MATCH (app:Application)
WHERE app.status IN ["incomplete", "in_review"]
  AND datetime() - app.application_date > duration("P7D")
RETURN app.application_id, app.status, 
       duration.between(app.application_date, datetime()).days as days_pending
ORDER BY days_pending DESC
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** 
- **Podman or Docker**
- **8GB+ RAM recommended**

### Installation & Deployment

```bash
# 1. Clone the repository
git clone <repository-url>
cd mortgage-db

# 2. Set up configuration files
cp deployment/neo4j/podman/config.yaml.example deployment/neo4j/podman/config.yaml
cp deployment/neo4j/podman/mortgage-pod.yaml.example deployment/neo4j/podman/mortgage-pod.yaml

# Edit the files and update YOUR_NEO4J_PASSWORD and YOUR_REGISTRY/YOUR_IMAGE
# For local testing, you can use: localhost/mortgage-db:latest

# 3. Build and deploy with Podman (includes Neo4j + Application)
./deployment/neo4j/podman/build.sh
./deployment/neo4j/podman/deploy.sh
```

**The container handles everything automatically:**
- Waits for Neo4j to be ready (60-90 seconds)
- Loads all data in 7 phases (reference data, sample data, business rules, relationships, knowledge graph, agent optimization)
- Validates all data loaded correctly
- Stays running for management access

**Result:** Complete mortgage database with:
- Neo4j running on `localhost:7474` (browser) and `localhost:7687` (bolt)
- 120+ sample customers and applications loaded
- 200+ business rules ready for AI agents
- Complete knowledge graph with relationship intelligence
- Agent-optimized schema with performance indexes

### Access Your Database
- **Neo4j Browser**: http://localhost:7474
- **Credentials**: `neo4j` / `[your-password]` (as configured in your yaml files)
- **Database**: `mortgage`

### Verify Installation
```cypher
// In Neo4j Browser, run this query to see your data:
MATCH (n) 
RETURN labels(n)[0] as nodeType, count(n) as count 
ORDER BY count DESC
```

## 🌍 Deployment Options

### 1. **Container Deployment** (Production Ready)
The system uses a self-initializing container that handles everything automatically:

```bash
# Option A: Use pre-built container (if available in your registry)
podman run -p 7474:7474 -p 7687:7687 your-registry/mortgage-agents:latest

# Option B: Build and deploy locally  
cp deployment/neo4j/podman/*.example deployment/neo4j/podman/
# Edit config.yaml and mortgage-pod.yaml with your settings
./deployment/neo4j/podman/build.sh
./deployment/neo4j/podman/deploy.sh
```

**Container Features:**
- Waits for Neo4j startup (60-90 seconds)
- Loads all 7 phases of data automatically  
- Optimizes schema for AI agent tools
- Validates complete data load
- Stays running for management access

### 2. **Local Development**
```bash
# Install Neo4j Desktop, create database "mortgage"
# Set your preferred password

# Install Python dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy config template and update with your settings
cp config.yaml.example config.yaml

# Load data to local Neo4j
python -m loaders.orchestrator
```

### 3. **OpenShift Enterprise**
The container is built with UBI images and SCC compliance:
- Non-root user (UID 1002)
- Dropped capabilities
- ReadOnlyRootFilesystem support
- OpenShift security context constraints compliant

## 📊 Database Contents

### **Reference Data** (21 entities)
- 5 Loan Programs (FHA, VA, Conventional, USDA, Jumbo)
- 4 Qualification Requirements with eligibility rules
- 8 Process Steps with workflow sequences  
- 4 Borrower Profiles for customer segmentation

### **Sample Data** (1,000+ entities)
- 120 People (borrowers, co-borrowers, agents, officers)
- 123 Properties with full characteristics
- 110 Applications across all loan types
- 611 Documents with verification status
- 33 Companies (employers, lenders, service providers)
- 22 Locations (cities, counties, zip codes)

### **Business Rules** (200+ rules)
- 12 Application Processing rules
- 64 Verification rules (24 document + 40 ID verification)
- 31 Financial Assessment rules  
- 14 Risk Scoring rules
- 23 Compliance rules
- 27 Underwriting rules
- 16 Pricing rules
- 5 Process Optimization rules

### **Knowledge Graph** (Intelligent Relationships)
- Credit score-based qualification logic
- DTI ratio risk assessment
- Intelligent loan program matching
- Automated risk scoring with categories
- Smart document requirement inference
- Geographic market analysis
- Regulatory compliance mapping

## 🔧 AI Agent Development

### Connection Management
```python
from utils.neo4j_connection import Neo4jConnection

# Simple connection for AI agents
conn = Neo4jConnection()
success = conn.connect()
if success:
    result, summary, keys = conn.execute_query(your_cypher_query)
    # Process results
    conn.disconnect()
```

### Application Storage
```python
from utils.application_storage import store_application_data, MortgageApplicationData

# Create new application
app_data = MortgageApplicationData(
    application_id="APP_2025_001",
    first_name="John",
    last_name="Doe",
    loan_amount=350000
    # ... other fields
)
success, app_id = store_application_data(app_data)
```

### Common Agent Patterns
```cypher
-- Get all business rules applicable to an application
MATCH (app:Application {application_id: $app_id})
MATCH (app)-[:SUBJECT_TO]->(rule:BusinessRule)  
RETURN rule.rule_type, rule.description, rule.criteria

-- Update application status
MATCH (app:Application {application_id: $app_id})
SET app.status = $new_status, app.updated_at = datetime()
RETURN app.status

-- Find missing documents  
MATCH (app:Application {application_id: $app_id})
MATCH (rule:DocumentVerificationRule)
OPTIONAL MATCH (app)-[:REQUIRES]->(d:Document {document_type: rule.document_type})
WHERE d IS NULL
RETURN rule.document_type as missing_document

-- Calculate qualification score
MATCH (app:Application {application_id: $app_id})
WITH app, 
     CASE WHEN app.credit_score >= 740 THEN 10 ELSE 5 END as credit_points,
     CASE WHEN app.dti_ratio <= 0.28 THEN 10 ELSE 5 END as dti_points  
SET app.qualification_score = credit_points + dti_points
RETURN app.qualification_score
```

## ⚡ Technical Advantages

### Where Graph Database Excels

**Multi-Hop Relationship Queries**
```cypher
// 3-degree relationship traversal for risk assessment
MATCH path = (person:Person)-[:APPLIES_FOR]->(app:Application)
            -[:HAS_PROPERTY]->(prop:Property)
            -[:LOCATED_IN]->(location:Location)
WHERE location.risk_indicators IS NOT NULL
RETURN person.person_id, collect(location.risk_indicators) as area_risks
```
This single query replaces multiple JOIN operations and is index-free adjacent (constant time per hop).

**Pattern-Based Validation**
```cypher
// Validate employment stability across applications
MATCH (person:Person)-[:WORKS_AT]->(company:Company)
MATCH (person)-[:APPLIES_FOR]->(apps:Application)
WITH person, company, count(apps) as app_count
WHERE company.years_in_business < 2 AND app_count > 1
RETURN person.person_id as flagged_applicant
```

**Schema-Free Evolution**
New mortgage product types, document requirements, or compliance rules can be added without altering existing data structure or requiring migrations.

### Current System Capabilities
- **Complete 7-phase data loading** in under 2 minutes
- **200+ business rules** integrated as queryable entities
- **1,000+ entities** with relationship-driven business logic
- **Knowledge graph** with automatic inference patterns
- **Real-time rule application** based on relationship context
- **Direct Cypher access** for AI agents and complex queries

## 🧪 Testing & Validation

### Quick Health Check
```bash
# Verify deployment is working
curl http://localhost:7474

# Test data loading
./deployment/podman/load-data.sh
```

### Sample Queries to Test
```cypher
-- Verify data loaded correctly
MATCH (n) RETURN labels(n)[0] as nodeType, count(n) as count ORDER BY count DESC

-- Test business rule queries
MATCH (rule:BusinessRule) RETURN rule.rule_type, count(*) ORDER BY count DESC

-- Test relationship intelligence  
MATCH (p:Person)-[:APPLIES_FOR]->(a:Application)-[:ELIGIBLE_FOR]->(lp:LoanProgram)
RETURN p.first_name, p.last_name, a.loan_amount, lp.name LIMIT 10

-- Test knowledge graph
MATCH (a:Application) WHERE a.risk_category IS NOT NULL
RETURN a.risk_category, count(*) ORDER BY count DESC
```

## 🤝 Contributing

### Current Status: **Production Ready**

**Features Available:**
- Complete containerized deployment
- Full data model implementation  
- 200+ business rules loaded and queryable
- AI agent integration ready
- Sample data for development/testing

### Development Setup
```bash
git clone <repository-url>
cd mortgage-db

# Set up development environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run local deployment
./deployment/podman/build.sh
./deployment/podman/deploy.sh
./deployment/podman/load-data.sh
```

### Areas for Enhancement
- **Additional AI Agent Tools** - More helper utilities
- **Advanced Analytics** - Graph algorithm implementations
- **Integration Modules** - Connect with external mortgage systems  
- **Performance Optimization** - Query performance tuning
- **Documentation** - More AI agent examples and use cases

## 🏆 Architecture Benefits

### Concrete Technical Advantages

#### **Query Expressiveness**
Mortgage business logic naturally maps to graph patterns. Compare these equivalent operations:

**Graph Database (Cypher)**
```cypher
MATCH (person:Person)-[:APPLIES_FOR]->(app:Application)
MATCH (person)-[:WORKS_AT]->(company:Company)
MATCH (app)-[:HAS_PROPERTY]->(property:Property)-[:LOCATED_IN]->(location:Location)
WHERE company.stability_rating < 3 AND location.market_trend = "declining"
RETURN app.application_id, "high_risk" as assessment
```

**Relational Database (SQL)**
```sql
SELECT a.application_id, 'high_risk' as assessment
FROM applications a
JOIN people p ON a.applicant_id = p.person_id
JOIN employment e ON p.person_id = e.person_id
JOIN companies c ON e.company_id = c.company_id
JOIN properties pr ON a.property_id = pr.property_id
JOIN locations l ON pr.location_id = l.location_id
WHERE c.stability_rating < 3 AND l.market_trend = 'declining'
```

#### **Regulatory Adaptability**
When mortgage regulations change, graph databases accommodate new requirements without structural changes:

```cypher
// New 2024 regulation: Track beneficial ownership
MATCH (company:Company)
WHERE company.entity_type = "LLC"
CREATE (company)-[:REQUIRES_DISCLOSURE]->(disclosure:BeneficialOwnership {effective_date: "2024-01-01"})
```

#### **Relationship-Driven Intelligence**
Enable AI agents to reason about connections and context:

```cypher
// Context-aware document requirements
MATCH (person:Person)-[:APPLIES_FOR]->(app:Application)
MATCH (person)-[:WORKS_AT]->(company:Company)
WHERE company.years_in_business < 2 OR company.employee_count < 10
CREATE (app)-[:REQUIRES]->(doc:Document {type: "business_verification", reason: "small_business_employment"})
```

### Value Proposition for AI Agents

#### **Natural Language to Graph Pattern Mapping**
AI agents can translate business requirements directly into graph traversals without complex JOIN logic.

#### **Contextual Decision Making**
Agents access full relationship context in single queries, enabling more informed decisions.

#### **Incremental Knowledge Building**
New relationships and insights can be added without disrupting existing data structure.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

### Quick Help
- **Database Access**: Neo4j Browser at http://localhost:7474
- **Credentials**: neo4j / mortgage123
- **Sample Queries**: See AI Agent Integration section above
- **Issues**: Use GitHub Issues for bugs and questions

### System Requirements
- **Minimum**: 8GB RAM, 4 CPU cores
- **Recommended**: 16GB RAM, 8 CPU cores  
- **Storage**: 10GB available space
- **Network**: Ports 7474, 7687 available

---

## 📊 Project Status

### **Version 1.0** - Production Ready

**Status**: Production deployment ready with full AI agent integration.

### **Key Features**
- **Self-Initializing Container**: Complete 7-phase data loading with automatic Neo4j readiness detection
- **Complete Data System**: 1,000+ entities with 23 different node types and comprehensive relationships
- **AI Agent Optimized**: Standardized schema with performance indexes and 100% property coverage
- **Knowledge Graph**: Intelligent relationship inference and semantic reasoning capabilities
- **Production Ready**: UBI-based container with OpenShift SCC compliance and non-root security
- **Comprehensive Rules**: 200+ production business rules across 8 categories

### **AI Agent Integration**
- **Direct Cypher Access**: Complete query interface for mortgage processing workflows
- **Standardized Schema**: All Application nodes include required properties for consistent agent operations
- **Performance Optimized**: Database indexes and constraints designed for fast agent queries
- **Real-time Capabilities**: Live decision making and workflow management support
- **Flexible Architecture**: Graph model designed to adapt to evolving mortgage requirements

### **Deployment**
- **Multi-Platform**: Compatible with Podman, Docker, Kubernetes, and OpenShift
- **Enterprise Security**: SCC compliant with non-root user and dropped capabilities
- **Zero-Touch Setup**: Complete hands-off deployment and data initialization
- **Portable Container**: Works consistently across development, staging, and production environments

### **Roadmap**
1. **Advanced AI Agent Tools** - Query builders and helper utilities for common operations
2. **Graph Analytics** - Advanced algorithms for relationship analysis and insights
3. **Integration APIs** - REST/GraphQL endpoints for external system integration
4. **Monitoring & Observability** - Comprehensive metrics, logging, and health monitoring
5. **Performance Optimization** - Query tuning and caching for high-throughput scenarios