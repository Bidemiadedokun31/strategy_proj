"""
Jira Ticket Generator for SmartResolve Project
Generates Epics, Features, and Stories in CSV format for bulk import

GitHub Repo: https://github.com/Bidemiadedokun31/strategy_proj.git
"""

JIRA_TICKETS = [
    # ============================================================================
    # EPIC: MVP - Core Platform & AI Agents
    # ============================================================================
    {
        "type": "Epic",
        "key": "EPIC-001",
        "name": "MVP - Core Platform & AI Agents Foundation",
        "description": """
Enterprise AI Complaint Intelligence Platform MVP

Deliverables:
- Core microservices architecture
- Summarization Agent with Bedrock integration
- Resolution Agent with RAG
- Basic web UI dashboard
- Authentication & RBAC
- AWS infrastructure foundation

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git
Timeline: Sprint 1-3 (8 weeks)
Priority: P0 Critical
""",
        "status": "To Do",
        "assignee": "Engineering Lead",
        "story_points": 89,
    },

    # ============================================================================
    # FEATURE: Summarization Service
    # ============================================================================
    {
        "type": "Feature",
        "key": "FEATURE-001",
        "parent": "EPIC-001",
        "name": "Call Transcript Summarization Engine",
        "description": """
Multi-tier AI-powered summarization of customer support call transcripts

Requirements:
- Support for 30+ minute call transcripts
- Multi-language support (EN, ES, FR, DE, PT, ZH)
- Executive summary (1-2 sentences)
- Detailed analysis (3-5 paragraphs)
- Key metrics extraction (issue type, sentiment, duration)
- Confidence scoring
- Processing latency: <10 seconds

AWS Services:
- Bedrock (Claude 3 Sonnet)
- DynamoDB (storage)
- S3 (transcript storage)
- Lambda (processing)

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/ai-agents/summarization-agent
Testing: Unit tests, integration tests, load tests (100 concurrent)
""",
        "status": "To Do",
        "priority": "P0",
        "story_points": 21,
    },

    # Story 1.1: Setup Bedrock integration
    {
        "type": "Story",
        "key": "STORY-001",
        "parent": "FEATURE-001",
        "name": "Integrate with AWS Bedrock for Claude 3 access",
        "description": """
Technical Story: Set up Bedrock client library and authentication

Acceptance Criteria:
- [ ] Bedrock client initialized with correct region & model ID
- [ ] IAM role has Bedrock invoke permissions
- [ ] Model invocation succeeds with test prompt
- [ ] Error handling for rate limits & timeouts
- [ ] Structured logging of all LLM calls
- [ ] Cost tracking per invocation

Tasks:
- Review Bedrock boto3 SDK
- Configure AWS credentials in Lambda environment
- Implement prompt templates
- Add observability hooks
- Test with 100 concurrent requests

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/ai-agents/summarization-agent
Definition of Done:
- Code reviewed & approved
- Unit tests pass (>90% coverage)
- Integration test with Bedrock succeeds
- Documentation updated
""",
        "status": "To Do",
        "priority": "P0",
        "assignee": "Backend Engineer",
        "story_points": 5,
    },

    # Story 1.2: Multi-language support
    {
        "type": "Story",
        "key": "STORY-002",
        "parent": "FEATURE-001",
        "name": "Implement multi-language transcript support",
        "description": """
Technical Story: Support 6+ languages in summarization pipeline

Acceptance Criteria:
- [ ] Language detection works for EN, ES, FR, DE, PT, ZH
- [ ] Language-specific prompts optimize for each language
- [ ] Quality metrics comparable across all languages
- [ ] Translation validation (no degradation)
- [ ] Test with native speakers for 2 languages

Languages:
1. English (en)
2. Spanish (es)
3. French (fr)
4. German (de)
5. Portuguese (pt)
6. Mandarin Chinese (zh)

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/ai-agents/summarization-agent
Testing:
- Unit tests for language detection
- Native speaker validation
- Quality regression tests
""",
        "status": "To Do",
        "priority": "P1",
        "assignee": "Backend Engineer",
        "story_points": 8,
    },

    # Story 1.3: Summarization Service Lambda
    {
        "type": "Story",
        "key": "STORY-003",
        "parent": "FEATURE-001",
        "name": "Create Summarization Service Lambda & API Gateway",
        "description": """
Technical Story: Build serverless API for transcript summarization

API Endpoints:
POST /api/v1/summarization/create
- Input: { complaintId, transcript, language? }
- Output: { id, complaintId, executive, detailed, keyMetrics, confidenceScore, processingTimeMs }
- Response time: <5s p95

GET /api/v1/summarization/:id
- Retrieve stored summary

GET /api/v1/summarization
- List summaries with pagination, filtering

Architecture:
- Lambda: 1024 MB memory, 300s timeout
- API Gateway: Rate limiting, request validation
- DynamoDB: On-demand billing, TTL 90 days

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/backend/services/summarization-service

Acceptance Criteria:
- [ ] Lambda cold start <3s
- [ ] 1000 concurrent invocations succeed
- [ ] All endpoints documented
- [ ] Error codes (400, 404, 500) handled
- [ ] Request/response validation via Zod
""",
        "status": "To Do",
        "priority": "P0",
        "assignee": "Backend Engineer",
        "story_points": 8,
    },

    # ============================================================================
    # FEATURE: Resolution Recommendation Engine
    # ============================================================================
    {
        "type": "Feature",
        "key": "FEATURE-002",
        "parent": "EPIC-001",
        "name": "AI Resolution Recommendation Engine with RAG",
        "description": """
RAG-based resolution recommendation system leveraging historical complaint data

Requirements:
- Query historical 500K+ complaint cases
- Semantic similarity matching
- Top-3 ranked recommendations with confidence scores
- Citation of source cases (audit trail)
- Processing latency: <2 seconds
- Explainability: show reasoning for each recommendation

AWS Services:
- Bedrock (Claude 3 Opus)
- OpenSearch (vector DB)
- SageMaker (embeddings)
- DynamoDB (recommendation storage)
- Lambda (orchestration)

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/ai-agents/rag-orchestrator

Success Metrics:
- 85%+ acceptance rate of recommendations
- <5% false recommendations
- P95 latency: <2 seconds
- 99.9% uptime
""",
        "status": "To Do",
        "priority": "P0",
        "story_points": 34,
    },

    # Story 2.1: OpenSearch vector DB setup
    {
        "type": "Story",
        "key": "STORY-004",
        "parent": "FEATURE-002",
        "name": "Provision OpenSearch vector DB for historical cases",
        "description": """
Infrastructure Story: Set up OpenSearch domain for RAG embeddings

Requirements:
- OpenSearch domain (t3.medium, 3 nodes, multi-AZ)
- Vector index configuration (1536 dimensions, HNSW)
- Index 500K historical cases
- Auto-scaling policies
- Backup strategy (daily snapshots)
- Encryption at rest & in transit (TLS 1.3)

Acceptance Criteria:
- [ ] OpenSearch domain healthy (3 nodes, green status)
- [ ] Index size ~500K documents, ~750GB
- [ ] Search latency p95 <100ms
- [ ] Snapshots working, retention 30 days
- [ ] Monitoring dashboards setup

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/infrastructure/terraform/main.tf
Cost: ~$2K/month (production)
""",
        "status": "To Do",
        "priority": "P0",
        "assignee": "DevOps Engineer",
        "story_points": 8,
    },

    # Story 2.2: RAG pipeline
    {
        "type": "Story",
        "key": "STORY-005",
        "parent": "FEATURE-002",
        "name": "Implement RAG retrieval & ranking pipeline",
        "description": """
Technical Story: Build RAG orchestration for resolution recommendations

Workflow:
1. Query embedding generation (SageMaker endpoint)
2. Vector similarity search (OpenSearch KNN query)
3. Semantic filtering (similarity threshold > 0.65)
4. Historical case ranking
5. Context assembly for LLM
6. Bedrock invocation with citations
7. Response parsing & confidence scoring

Acceptance Criteria:
- [ ] Top-K retrieval works (K=5, max_distance=0.7)
- [ ] Ranking algorithm tested with 100 cases
- [ ] Citation links persist through pipeline
- [ ] Error handling for vector DB unavailability
- [ ] Telemetry: retrieval time, LLM latency, recommendation quality

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/ai-agents/rag-orchestrator/src/orchestrator.py

Testing:
- Unit tests for each stage
- Integration test with sample cases
- Load test (100 concurrent recommendations)
""",
        "status": "To Do",
        "priority": "P0",
        "assignee": "ML Engineer",
        "story_points": 13,
    },

    # Story 2.3: Resolution API
    {
        "type": "Story",
        "key": "STORY-006",
        "parent": "FEATURE-002",
        "name": "Create Resolution Service API & Lambda",
        "description": """
Technical Story: Build REST API for resolution recommendations

Endpoints:
POST /api/v1/resolutions/recommend
- Input: { complaintId, complainSummary }
- Output: { id, recommendations: [{ rank, resolution, confidence, citedCases }], reasoning }

GET /api/v1/resolutions/:id
- Retrieve stored recommendation

GET /api/v1/resolutions/complaint/:complaintId
- List all recommendations for complaint

Architecture:
- Lambda: 2048 MB memory, 30s timeout
- Async SQS processing for long-running jobs
- CloudWatch metrics for recommendation quality

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/backend/services/resolution-service

Acceptance Criteria:
- [ ] API handles 500 concurrent requests
- [ ] Recommendations returned <2s p95
- [ ] All endpoints have request validation
- [ ] Error responses include request ID for debugging
- [ ] Documentation with example requests
""",
        "status": "To Do",
        "priority": "P0",
        "assignee": "Backend Engineer",
        "story_points": 10,
    },

    # ============================================================================
    # FEATURE: Authentication & RBAC
    # ============================================================================
    {
        "type": "Feature",
        "key": "FEATURE-003",
        "parent": "EPIC-001",
        "name": "Enterprise Authentication & Role-Based Access Control",
        "description": """
Secure authentication and authorization system

Requirements:
- AWS Cognito for identity management
- JWT tokens with short expiry (15 min)
- Refresh token rotation
- Role-based access control (RBAC)
- Roles: Admin, Manager, Agent, Viewer
- Data isolation by role & customer
- Audit logging of all access
- MFA support (optional)

AWS Services:
- Cognito User Pools
- Cognito Identity Pools
- API Gateway authorizers
- IAM policies per role

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/backend/shared/utils

Success Metrics:
- 100% of API calls validated
- Zero unauthorized access incidents
- Auth latency <50ms
- 99.99% uptime
""",
        "status": "To Do",
        "priority": "P0",
        "story_points": 13,
    },

    # ============================================================================
    # FEATURE: Frontend Dashboard
    # ============================================================================
    {
        "type": "Feature",
        "key": "FEATURE-004",
        "parent": "EPIC-001",
        "name": "Enterprise Dashboard UI with Real-time Updates",
        "description": """
React-based SPA for complaint management and AI insights

Pages:
1. Dashboard (complaint list, real-time status)
2. Complaint Details (transcript, summary, resolution)
3. Analytics (complaint trends, resolution effectiveness)
4. Audit Trail (all operations logged)
5. Settings (user preferences, integrations)

Requirements:
- Responsive design (mobile, tablet, desktop)
- Real-time updates via WebSocket
- Dark/light theme support
- Accessibility (WCAG 2.1 AA)
- TypeScript + React 18
- TanStack Query for data fetching

AWS Services:
- CloudFront CDN
- S3 static hosting
- API Gateway for backend

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/frontend

Success Metrics:
- Lighthouse score >90
- Core Web Vitals excellent
- <1 second page load (p95)
- Mobile accessibility score 95+
""",
        "status": "To Do",
        "priority": "P0",
        "story_points": 21,
    },

    # ============================================================================
    # EPIC: Enterprise Ready
    # ============================================================================
    {
        "type": "Epic",
        "key": "EPIC-002",
        "name": "Enterprise Ready - Compliance, Security & Scalability",
        "description": """
Production hardening for enterprise deployment

Deliverables:
- SOC 2 Type II compliance
- HIPAA/GDPR ready
- Advanced monitoring & observability
- Disaster recovery setup
- Performance optimization
- Enterprise SLA targets (99.9% uptime)

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git
Timeline: Sprint 4-6 (12 weeks)
Priority: P1 High
Story Points: 144
""",
        "status": "To Do",
        "assignee": "Architecture Lead",
        "story_points": 144,
    },

    # FEATURE: Audit Logging & Compliance
    {
        "type": "Feature",
        "key": "FEATURE-005",
        "parent": "EPIC-002",
        "name": "Comprehensive Audit Logging & Compliance Reporting",
        "description": """
Immutable audit trail for SOC 2 compliance

Requirements:
- Log all API calls: user, timestamp, action, resource, result
- Log all AI decisions: prompt, model, output, confidence
- Log all data access: who, what, when, why
- Immutable storage (CloudTrail + RDS)
- 7-year retention
- Searchable & queryable
- Compliance reports (monthly, annual)

AWS Services:
- CloudTrail (API audit)
- RDS (application audit logs)
- Athena (querying)
- QuickSight (reports)

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/backend/services/audit-api

Success Metrics:
- 100% log capture
- <100ms audit write latency
- 0 data loss
- Full traceability of AI decisions
""",
        "status": "To Do",
        "priority": "P1",
        "story_points": 21,
    },

    # FEATURE: Advanced Monitoring & Alerting
    {
        "type": "Feature",
        "key": "FEATURE-006",
        "parent": "EPIC-002",
        "name": "Advanced Monitoring, Observability & Alerting",
        "description": """
Production-grade observability stack

Components:
1. CloudWatch dashboards
   - Request latency (p50, p95, p99)
   - Error rates & types
   - LLM token usage & costs
   - Database performance

2. X-Ray distributed tracing
   - Service dependencies
   - Latency bottlenecks
   - Error traces

3. Alarms & Escalation
   - API latency >2s
   - Error rate >0.1%
   - Token usage >80% budget
   - Vector DB indexing lag >5min

4. QuickSight reports
   - Executive dashboard
   - Complaint trends
   - AI accuracy metrics

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/infrastructure/cloudformation

Success Metrics:
- MTTR <15 minutes
- Alert accuracy >95%
- Dashboard load <2s
""",
        "status": "To Do",
        "priority": "P1",
        "story_points": 13,
    },

    # ============================================================================
    # EPIC: Scale & Optimize
    # ============================================================================
    {
        "type": "Epic",
        "key": "EPIC-003",
        "name": "Scale & Optimize - Performance & Cost",
        "description": """
High-scale optimization for mature product

Deliverables:
- 10K concurrent users support
- Sub-2s P95 latency
- 50% cost reduction
- Advanced caching strategies
- Database query optimization
- AI model optimization

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git
Timeline: Sprint 7+ (ongoing)
Priority: P2 Medium
Story Points: 89
""",
        "status": "To Do",
        "assignee": "Performance Lead",
        "story_points": 89,
    },
]

# Generate CSV for Jira bulk import
CSV_HEADER = "Type,Key,Parent,Name,Description,Status,Priority,Assignee,Story Points"

def generate_csv():
    """Generate CSV content for Jira import"""
    lines = [CSV_HEADER]
    
    for ticket in JIRA_TICKETS:
        parent = f'"{ticket.get("parent", "")}"' if ticket.get("parent") else '""'
        description = f'"{ticket["description"].strip()}"'
        priority = f'"{ticket.get("priority", "P0")}"'
        
        line = f"""{ticket["type"]},{ticket["key"]},{parent},"{ticket["name"]}",{description},{ticket["status"]},{priority},"{ticket.get("assignee", "")}",{ticket.get("story_points", 0)}"""
        lines.append(line)
    
    return "\n".join(lines)

if __name__ == "__main__":
    csv_content = generate_csv()
    
    # Save to file
    with open("jira_tickets.csv", "w") as f:
        f.write(csv_content)
    
    print(f"✓ Generated {len(JIRA_TICKETS)} Jira tickets")
    print(f"✓ Saved to jira_tickets.csv")
    print(f"\nTicket Summary:")
    print(f"- Epics: {sum(1 for t in JIRA_TICKETS if t['type'] == 'Epic')}")
    print(f"- Features: {sum(1 for t in JIRA_TICKETS if t['type'] == 'Feature')}")
    print(f"- Stories: {sum(1 for t in JIRA_TICKETS if t['type'] == 'Story')}")
    print(f"- Total Story Points: {sum(t.get('story_points', 0) for t in JIRA_TICKETS)}")
    print(f"\nGitHub Repo: https://github.com/Bidemiadedokun31/strategy_proj.git")
