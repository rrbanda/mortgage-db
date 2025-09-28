# Mortgage Database - Build and Deployment Makefile

.PHONY: help build-podman deploy-podman test-podman clean-podman build-openshift deploy-openshift test-openshift clean-openshift test-all

# Default target
help: ## Show this help message
	@echo "Mortgage Database - Available Commands:"
	@echo "======================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# =====================================
# PODMAN COMMANDS
# =====================================

build-podman: ## Build container image for Podman
	@echo "🐳 Building Mortgage Database container for Podman..."
	podman build -f deployment/containers/Containerfile -t localhost/mortgage-db:latest .
	@echo "✅ Container build complete"

deploy-podman: build-podman ## Deploy to Podman using Kubernetes YAML
	@echo "🚀 Deploying Mortgage Database to Podman..."
	podman play kube deployment/podman/mortgage-db-complete.yaml
	@echo "✅ Deployment complete"
	@echo "📊 Access Neo4j at: http://localhost:30474"
	@echo "🔐 Login: neo4j / mortgage123"

test-podman: ## Test Podman deployment
	@echo "🧪 Testing Podman deployment..."
	@echo "Waiting for service to be ready..."
	@sleep 10
	@curl -f http://localhost:30474/db/data/ && echo "✅ Neo4j HTTP accessible" || echo "❌ Neo4j HTTP failed"
	@podman exec mortgage-db-mortgage-db python3 /opt/mortgage-db/setup/initialize_database.py --health-check || echo "⚠️  Health check failed"

logs-podman: ## Show Podman container logs
	@echo "📋 Podman container logs:"
	podman logs mortgage-db-mortgage-db

status-podman: ## Show Podman deployment status
	@echo "📊 Podman deployment status:"
	@podman pod ps
	@podman ps -a --filter ancestor=localhost/mortgage-db:latest

clean-podman: ## Clean up Podman deployment
	@echo "🧹 Cleaning up Podman deployment..."
	-podman play kube --down deployment/podman/mortgage-db-complete.yaml
	-podman pod rm -f mortgage-db
	-podman container prune -f
	@echo "✅ Podman cleanup complete"

# =====================================
# OPENSHIFT COMMANDS  
# =====================================

deploy-openshift: ## Deploy to OpenShift
	@echo "🏢 Deploying Mortgage Database to OpenShift..."
	@echo "Creating project if not exists..."
	-oc new-project mortgage-system
	oc project mortgage-system
	@echo "Applying resources..."
	oc apply -f deployment/openshift/secret.yaml
	oc apply -f deployment/openshift/pvc.yaml
	oc apply -f deployment/openshift/deployment.yaml
	oc apply -f deployment/openshift/service.yaml
	oc apply -f deployment/openshift/route.yaml
	@echo "✅ OpenShift deployment complete"
	@echo "🌐 Route URL:"
	@oc get route mortgage-db-http -o jsonpath='{.spec.host}' 2>/dev/null || echo "Route not ready yet"

test-openshift: ## Test OpenShift deployment
	@echo "🧪 Testing OpenShift deployment..."
	@echo "Checking deployment status..."
	oc get deployment mortgage-db
	@echo "Checking route..."
	@ROUTE_URL=$$(oc get route mortgage-db-http -o jsonpath='{.spec.host}' 2>/dev/null) && \
	if [ -n "$$ROUTE_URL" ]; then \
		curl -f https://$$ROUTE_URL/db/data/ && echo "✅ Neo4j accessible via route" || echo "❌ Route access failed"; \
	else \
		echo "⚠️  Route not ready yet"; \
	fi

logs-openshift: ## Show OpenShift deployment logs
	@echo "📋 OpenShift deployment logs:"
	oc logs deployment/mortgage-db --tail=100 -f

status-openshift: ## Show OpenShift deployment status
	@echo "📊 OpenShift deployment status:"
	@oc get all -l app=mortgage-db
	@echo ""
	@echo "📊 Route information:"
	@oc get route mortgage-db-http

clean-openshift: ## Clean up OpenShift deployment
	@echo "🧹 Cleaning up OpenShift deployment..."
	-oc delete all -l app=mortgage-db
	-oc delete pvc mortgage-db-data-pvc
	-oc delete secret mortgage-db-secret
	@echo "✅ OpenShift cleanup complete"

# =====================================
# TESTING COMMANDS
# =====================================

test-schema: ## Test database schema after deployment
	@echo "🔍 Testing database schema..."
	@if command -v podman >/dev/null 2>&1 && podman ps --filter ancestor=localhost/mortgage-db:latest --format '{{.Names}}' | head -1 >/dev/null; then \
		echo "Testing with Podman..."; \
		podman exec mortgage-db-mortgage-db python3 -c "import sys; sys.path.append('/opt/mortgage-db'); from utils.neo4j_connection import get_neo4j_connection, initialize_connection; initialize_connection(); conn = get_neo4j_connection(); \
		with conn.driver.session(database=conn.database) as session: \
			result = session.run('MATCH (n) RETURN labels(n)[0] as NodeType, count(n) as Count ORDER BY Count DESC'); \
			print('Node Types:'); \
			for record in result: print(f'  {record[\"NodeType\"]}: {record[\"Count\"]}')"; \
	elif command -v oc >/dev/null 2>&1 && oc get deployment mortgage-db >/dev/null 2>&1; then \
		echo "Testing with OpenShift..."; \
		oc exec deployment/mortgage-db -- python3 -c "import sys; sys.path.append('/opt/mortgage-db'); from utils.neo4j_connection import get_neo4j_connection, initialize_connection; initialize_connection(); conn = get_neo4j_connection(); \
		with conn.driver.session(database=conn.database) as session: \
			result = session.run('MATCH (n) RETURN labels(n)[0] as NodeType, count(n) as Count ORDER BY Count DESC'); \
			print('Node Types:'); \
			for record in result: print(f'  {record[\"NodeType\"]}: {record[\"Count\"]}')"; \
	else \
		echo "❌ No running deployment found"; \
	fi

test-business-rules: ## Test business rules loading
	@echo "🧠 Testing business rules..."
	@if command -v podman >/dev/null 2>&1 && podman ps --filter ancestor=localhost/mortgage-db:latest --format '{{.Names}}' | head -1 >/dev/null; then \
		podman exec mortgage-db-mortgage-db python3 -c "import sys; sys.path.append('/opt/mortgage-db'); from utils.neo4j_connection import get_neo4j_connection, initialize_connection; initialize_connection(); conn = get_neo4j_connection(); \
		with conn.driver.session(database=conn.database) as session: \
			result = session.run('MATCH (r:ApplicationIntakeRule) RETURN count(r) as Count'); \
			count = result.single()['Count']; \
			print(f'✅ Application Intake Rules: {count}'); \
			result = session.run('MATCH (r:DocumentVerificationRule) RETURN count(r) as Count'); \
			count = result.single()['Count']; \
			print(f'✅ Document Verification Rules: {count}')"; \
	elif command -v oc >/dev/null 2>&1 && oc get deployment mortgage-db >/dev/null 2>&1; then \
		oc exec deployment/mortgage-db -- python3 -c "import sys; sys.path.append('/opt/mortgage-db'); from utils.neo4j_connection import get_neo4j_connection, initialize_connection; initialize_connection(); conn = get_neo4j_connection(); \
		with conn.driver.session(database=conn.database) as session: \
			result = session.run('MATCH (r:ApplicationIntakeRule) RETURN count(r) as Count'); \
			count = result.single()['Count']; \
			print(f'✅ Application Intake Rules: {count}'); \
			result = session.run('MATCH (r:DocumentVerificationRule) RETURN count(r) as Count'); \
			count = result.single()['Count']; \
			print(f'✅ Document Verification Rules: {count}')"; \
	else \
		echo "❌ No running deployment found"; \
	fi

test-all: test-schema test-business-rules ## Run all tests

# =====================================
# DEVELOPMENT COMMANDS
# =====================================

config-check: ## Verify configuration files
	@echo "🔧 Checking configuration..."
	@python3 -c "import yaml; yaml.safe_load(open('config.yaml.example'))" && echo "✅ config.yaml.example valid" || echo "❌ config.yaml.example invalid"
	@python3 -c "import yaml; [yaml.safe_load_all(open(f)) for f in ['deployment/podman/mortgage-db-complete.yaml']]" && echo "✅ Podman YAML valid" || echo "❌ Podman YAML invalid"

requirements-check: ## Check Python requirements
	@echo "📋 Checking Python requirements..."
	@python3 -c "import pkg_resources; pkg_resources.require(open('requirements.txt').read().splitlines())" && echo "✅ All requirements available" || echo "⚠️  Some requirements missing"

# =====================================
# UTILITY COMMANDS
# =====================================

clean-all: clean-podman clean-openshift ## Clean up all deployments
	@echo "🧹 All deployments cleaned up"

info: ## Show deployment information
	@echo "📊 Mortgage Database Information:"
	@echo "================================"
	@echo "📁 Project Directory: $(shell pwd)"
	@echo "🐳 Container Image: localhost/mortgage-db:latest"
	@echo "🗄️  Database Name: mortgage"
	@echo "🔐 Default Credentials: neo4j / mortgage123"
	@echo "🌐 Podman HTTP: http://localhost:30474"
	@echo "🔌 Podman Bolt: bolt://localhost:30687"
	@if command -v oc >/dev/null 2>&1; then \
		echo "🏢 OpenShift Route: $$(oc get route mortgage-db-http -o jsonpath='{.spec.host}' 2>/dev/null || echo 'Not deployed')"; \
	fi

# Default target when no argument is provided
.DEFAULT_GOAL := help

