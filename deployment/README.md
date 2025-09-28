# Mortgage Database Deployment Guide

This guide covers deployment of the **bulletproof portable container** using Podman and OpenShift.

## 🏗️ Architecture Overview

- **🌍 Bulletproof Container**: Self-initializing with complete 7-phase data loading
- **🎯 Zero-Touch Deployment**: Automatic Neo4j readiness detection and full database setup
- **🔧 Production Ready**: UBI-based, OpenShift SCC compliant, non-root security
- **📊 Complete System**: 1,000+ entities, 23 node types, 200+ business rules
- **🤖 AI Agent Optimized**: Schema alignment, performance indexes, 100% property coverage

## 📋 Prerequisites

### For Podman Deployment
- [Podman Desktop](https://podman-desktop.io/) installed
- 8GB+ available RAM
- 20GB+ available disk space

### For OpenShift Deployment  
- OpenShift cluster access with project creation permissions
- `oc` CLI tool configured
- Container registry access (or ability to import images)

## 🐳 Phase 1: Podman Desktop Deployment

### Step 1: Setup Configuration

```bash
cd /path/to/mortgage-db

# Copy configuration templates
cp deployment/neo4j/podman/config.yaml.example deployment/neo4j/podman/config.yaml
cp deployment/neo4j/podman/mortgage-pod.yaml.example deployment/neo4j/podman/mortgage-pod.yaml

# Edit config.yaml and mortgage-pod.yaml
# - Set YOUR_NEO4J_PASSWORD to your preferred password
# - Set YOUR_REGISTRY/YOUR_IMAGE to localhost/mortgage-db:latest for local builds
```

### Step 2: Build and Deploy

```bash
# Build the bulletproof container
./deployment/neo4j/podman/build.sh

# Deploy the complete stack (Neo4j + Application)
./deployment/neo4j/podman/deploy.sh
```

**The container automatically:**
- ⏳ Waits for Neo4j startup (60-90 seconds)
- 📊 Loads all 7 phases of data
- 🤖 Optimizes schema for AI agents  
- ✅ Validates complete setup
- 🔄 Stays running for access

### Step 3: Access Your System

```bash
# Monitor the initialization progress
podman logs -f mortgage-db-pod-mortgage-app

# Access Neo4j Browser
open http://localhost:7474
# Login: neo4j / [your-configured-password]
```

### Step 4: Verify Database Setup

Access Neo4j Browser at http://localhost:7474 and run:

```cypher
// Verify database name
:use mortgage

// Check all loaded data (should see 23 different node types)
MATCH (n) RETURN labels(n)[0] as NodeType, count(n) as Count ORDER BY Count DESC

// Verify AI agent schema optimization
MATCH (app:Application) 
RETURN count(app) as total_applications,
       count(app.id) as has_id,
       count(app.borrower_name) as has_borrower_name,
       count(app.status) as has_status

// Verify knowledge graph relationships
MATCH ()-[r]-() RETURN type(r) as RelType, count(r) as Count ORDER BY Count DESC LIMIT 10
```

**Expected Results (Bulletproof Container):**
- **23 Node Types**: Application (110), Person (120), Property (123), Document (611), etc.
- **Agent Schema**: 100% property coverage for all Applications
- **Knowledge Graph**: Intelligent relationships like MATCHES_PROFILE, ELIGIBLE_FOR
- **Total Entities**: 1,000+ nodes with rich relationship network

## 🏢 Phase 2: OpenShift Deployment

### Step 1: Prepare OpenShift Project

```bash
# Login to OpenShift
oc login

# Create project
oc new-project mortgage-system

# Verify project
oc project mortgage-system
```

### Step 2: Import Container Image

**Option A: Build in OpenShift**
```bash
# Create ImageStream
oc create imagestream mortgage-db

# Start build from local Containerfile
oc new-build --strategy docker --binary --name mortgage-db
oc start-build mortgage-db --from-dir=. --follow
```

**Option B: Import from Registry**
```bash
# Tag and push to accessible registry first
podman tag localhost/mortgage-db:latest <your-registry>/mortgage-db:latest
podman push <your-registry>/mortgage-db:latest

# Import to OpenShift
oc import-image mortgage-db:latest --from=<your-registry>/mortgage-db:latest --confirm
```

### Step 3: Deploy to OpenShift

```bash
cd deployment/openshift

# Create resources in order
oc apply -f secret.yaml
oc apply -f pvc.yaml
oc apply -f deployment.yaml
oc apply -f service.yaml
oc apply -f route.yaml
```

### Step 4: Verify OpenShift Deployment

```bash
# Check deployment status
oc get all -l app=mortgage-db

# Check pod logs
oc logs deployment/mortgage-db -f

# Check route
oc get route mortgage-db-http
ROUTE_URL=$(oc get route mortgage-db-http -o jsonpath='{.spec.host}')
curl https://$ROUTE_URL/db/data/
```

### Step 5: Access Neo4j in OpenShift

```bash
# Get the route URL
oc get route mortgage-db-http

# Access Neo4j Browser
open https://<route-url>
# Login: neo4j / mortgage123
```

## 🔧 Configuration Options

### Memory Settings

**Podman (Local Development):**
- Heap: 2G initial, 4G max
- Page Cache: 2G

**OpenShift (Production):**
- Heap: 1G initial, 2G max  
- Page Cache: 1G
- Resource requests: 2Gi RAM, 500m CPU
- Resource limits: 4Gi RAM, 1500m CPU

### Environment Variables

| Variable | Podman Value | OpenShift Value | Description |
|----------|--------------|-----------------|-------------|
| `NEO4J_AUTH` | `neo4j/mortgage123` | From secret | Authentication |
| `NEO4J_dbms_default__database` | `mortgage` | `mortgage` | Database name |
| `NEO4J_dbms_memory_heap_max__size` | `4G` | `2G` | Max heap size |

## 🩺 Troubleshooting

### Podman Issues

```bash
# Container won't start
podman logs mortgage-db-mortgage-db

# Port conflicts
podman ps --all
# Change nodePort in service.yaml if needed

# Memory issues
# Reduce memory settings in deployment.yaml
```

### OpenShift Issues

```bash
# Permission denied errors
oc describe pod <pod-name>
# Check SCC settings

# Image pull issues
oc get events --field-selector type=Warning

# Storage issues
oc get pvc
oc describe pvc mortgage-db-data-pvc
```

### Database Issues

```bash
# Database not initializing
oc/podman exec -it <container> python3 /opt/mortgage-db/setup/initialize_database.py

# Connection refused
# Check if Neo4j is fully started (may take 2-3 minutes)
oc/podman logs <container> | grep "Started"
```

## 🧪 Testing the Setup

### Automated Tests

```bash
# Run inside container
podman exec -it mortgage-db-mortgage-db python3 -m pytest /opt/mortgage-db/tests/ -v

# Or in OpenShift
oc exec deployment/mortgage-db -- python3 -m pytest /opt/mortgage-db/tests/ -v
```

### Manual Verification

1. **Database Connectivity**: Neo4j Browser accessible
2. **Schema Created**: Constraints and indexes present  
3. **Data Loaded**: Sample data exists
4. **Knowledge Graph**: Business rules loaded
5. **Performance**: Response time < 2 seconds for basic queries

## 📊 Monitoring

### Health Endpoints

- Neo4j HTTP: `http://<host>:7474/db/data/`
- Application Health: Built into startup probes

### Key Metrics to Monitor

- Memory usage (should be < 80% of limits)
- Query response time
- Number of active connections
- Database growth over time

## 🔄 Maintenance

### Backup (OpenShift)

```bash
# Create backup job
oc create job --from=cronjob/backup-mortgage-db backup-$(date +%Y%m%d)
```

### Updates

```bash
# Podman: Rebuild and redeploy
podman build -f deployment/containers/Containerfile -t localhost/mortgage-db:latest .
podman play kube deployment/podman/mortgage-db-complete.yaml --replace

# OpenShift: Update deployment
oc rollout restart deployment/mortgage-db
```

---

## 🎯 Success Criteria

✅ **Podman Working**: Neo4j accessible at localhost:30474, database "mortgage" contains business rules
✅ **OpenShift Working**: Neo4j accessible via route, all resources healthy, persistent storage working
✅ **Auto-Initialization**: All phases complete successfully on startup
✅ **Performance**: System responds within expected time limits
✅ **Security**: OpenShift SCC compliance, no root containers

