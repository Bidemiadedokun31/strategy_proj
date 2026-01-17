"""
Jira Ticket Creator via REST API
Creates Epics, Features, and Stories with full hierarchy
GitHub Repo: https://github.com/Bidemiadedokun31/strategy_proj.git
"""

import requests
import json
from typing import Dict, Optional
import time

class JiraTicketCreator:
    def __init__(self, cloud_id: str, base_url: str, api_token: str):
        self.cloud_id = cloud_id
        self.base_url = f"{base_url}/rest/api/3"
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }
        self.project_key = "SCRUM"
        self.created_tickets = {}

    def create_epic(self, name: str, description: str, story_points: int = 0) -> Optional[str]:
        """Create an Epic in Jira"""
        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "issuetype": {"name": "Epic"},
                "summary": name,
                "description": {
                    "version": 1,
                    "type": "doc",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "customfield_10016": name,  # Epic Name field
            }
        }
        
        if story_points > 0:
            payload["fields"]["customfield_10021"] = story_points  # Story Points
        
        response = requests.post(
            f"{self.base_url}/issue",
            json=payload,
            headers=self.headers
        )
        
        if response.status_code == 201:
            ticket_id = response.json()["id"]
            ticket_key = response.json()["key"]
            print(f"✓ Created Epic: {ticket_key}")
            return ticket_key
        else:
            print(f"✗ Failed to create Epic: {response.text}")
            return None

    def create_feature(
        self,
        name: str,
        description: str,
        epic_key: Optional[str] = None,
        priority: str = "Medium",
        story_points: int = 0
    ) -> Optional[str]:
        """Create a Feature in Jira"""
        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "issuetype": {"name": "Feature"},
                "summary": name,
                "description": {
                    "version": 1,
                    "type": "doc",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "priority": {"name": priority},
            }
        }
        
        if epic_key:
            payload["fields"]["customfield_10020"] = epic_key  # Epic Link field
        
        if story_points > 0:
            payload["fields"]["customfield_10021"] = story_points  # Story Points
        
        response = requests.post(
            f"{self.base_url}/issue",
            json=payload,
            headers=self.headers
        )
        
        if response.status_code == 201:
            ticket_key = response.json()["key"]
            print(f"✓ Created Feature: {ticket_key}")
            return ticket_key
        else:
            print(f"✗ Failed to create Feature: {response.text}")
            return None

    def create_story(
        self,
        name: str,
        description: str,
        parent_key: Optional[str] = None,
        priority: str = "Medium",
        story_points: int = 0
    ) -> Optional[str]:
        """Create a Story in Jira"""
        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "issuetype": {"name": "Story"},
                "summary": name,
                "description": {
                    "version": 1,
                    "type": "doc",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "priority": {"name": priority},
            }
        }
        
        if parent_key:
            payload["fields"]["customfield_10020"] = parent_key  # Epic/Feature Link field
        
        if story_points > 0:
            payload["fields"]["customfield_10021"] = story_points  # Story Points
        
        response = requests.post(
            f"{self.base_url}/issue",
            json=payload,
            headers=self.headers
        )
        
        if response.status_code == 201:
            ticket_key = response.json()["key"]
            print(f"✓ Created Story: {ticket_key}")
            return ticket_key
        else:
            print(f"✗ Failed to create Story: {response.text}")
            return None

    def create_tickets(self):
        """Create all SmartResolve project tickets"""
        
        print("\n" + "="*80)
        print("SmartResolve - Jira Ticket Creation")
        print("="*80)
        print(f"GitHub Repo: https://github.com/Bidemiadedokun31/strategy_proj.git\n")
        
        # ========================================================================
        # EPIC 1: MVP - Core Platform & AI Agents
        # ========================================================================
        print("\n[EPIC 1] Creating MVP Epic...")
        epic1_key = self.create_epic(
            name="MVP - Core Platform & AI Agents Foundation",
            description="""Enterprise AI Complaint Intelligence Platform MVP

Deliverables:
- Core microservices architecture
- Summarization Agent with Bedrock integration
- Resolution Agent with RAG
- Basic web UI dashboard
- Authentication & RBAC
- AWS infrastructure foundation

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git
Timeline: Sprint 1-3 (8 weeks)
Priority: P0 Critical""",
            story_points=89
        )
        
        if epic1_key:
            self.created_tickets["EPIC-001"] = epic1_key
            
            # FEATURE 1: Summarization Service
            print("\n[FEATURE 1] Creating Summarization Feature...")
            feature1_key = self.create_feature(
                name="Call Transcript Summarization Engine",
                description="""Multi-tier AI-powered summarization of customer support call transcripts

Requirements:
- Support for 30+ minute call transcripts
- Multi-language support (EN, ES, FR, DE, PT, ZH)
- Executive summary (1-2 sentences)
- Detailed analysis (3-5 paragraphs)
- Key metrics extraction (issue type, sentiment, duration)
- Confidence scoring
- Processing latency: <10 seconds

AWS Services: Bedrock (Claude 3 Sonnet), DynamoDB, S3, Lambda

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/ai-agents/summarization-agent""",
                epic_key=epic1_key,
                priority="High",
                story_points=21
            )
            
            if feature1_key:
                self.created_tickets["FEATURE-001"] = feature1_key
                
                # Story 1.1
                print("\n[STORY 1.1] Creating Bedrock Integration Story...")
                self.create_story(
                    name="Integrate with AWS Bedrock for Claude 3 access",
                    description="""Technical Story: Set up Bedrock client library and authentication

Acceptance Criteria:
- [ ] Bedrock client initialized with correct region & model ID
- [ ] IAM role has Bedrock invoke permissions
- [ ] Model invocation succeeds with test prompt
- [ ] Error handling for rate limits & timeouts
- [ ] Structured logging of all LLM calls
- [ ] Cost tracking per invocation

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/ai-agents/summarization-agent""",
                    parent_key=feature1_key,
                    priority="High",
                    story_points=5
                )
                
                # Story 1.2
                print("[STORY 1.2] Creating Multi-language Support Story...")
                self.create_story(
                    name="Implement multi-language transcript support",
                    description="""Technical Story: Support 6+ languages in summarization pipeline

Languages: EN, ES, FR, DE, PT, ZH

Acceptance Criteria:
- [ ] Language detection works for all 6 languages
- [ ] Language-specific prompts optimize for each language
- [ ] Quality metrics comparable across all languages
- [ ] Test with native speakers for 2 languages

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/ai-agents/summarization-agent""",
                    parent_key=feature1_key,
                    priority="High",
                    story_points=8
                )
                
                # Story 1.3
                print("[STORY 1.3] Creating Summarization API Story...")
                self.create_story(
                    name="Create Summarization Service Lambda & API Gateway",
                    description="""Technical Story: Build serverless API for transcript summarization

API Endpoints:
- POST /api/v1/summarization/create
- GET /api/v1/summarization/:id
- GET /api/v1/summarization

Architecture: Lambda (1024MB, 300s timeout), API Gateway, DynamoDB

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/backend/services/summarization-service""",
                    parent_key=feature1_key,
                    priority="High",
                    story_points=8
                )
            
            # FEATURE 2: Resolution Engine
            print("\n[FEATURE 2] Creating Resolution Feature...")
            feature2_key = self.create_feature(
                name="AI Resolution Recommendation Engine with RAG",
                description="""RAG-based resolution recommendation system leveraging historical complaint data

Requirements:
- Query historical 500K+ complaint cases
- Semantic similarity matching
- Top-3 ranked recommendations with confidence scores
- Citation of source cases (audit trail)
- Processing latency: <2 seconds
- Explainability: show reasoning for each recommendation

AWS Services: Bedrock, OpenSearch, SageMaker, DynamoDB, Lambda

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/ai-agents/rag-orchestrator""",
                epic_key=epic1_key,
                priority="High",
                story_points=34
            )
            
            if feature2_key:
                self.created_tickets["FEATURE-002"] = feature2_key
                
                # Story 2.1
                print("\n[STORY 2.1] Creating OpenSearch Setup Story...")
                self.create_story(
                    name="Provision OpenSearch vector DB for historical cases",
                    description="""Infrastructure Story: Set up OpenSearch domain for RAG embeddings

Requirements:
- OpenSearch domain (t3.medium, 3 nodes, multi-AZ)
- Vector index configuration (1536 dimensions, HNSW)
- Index 500K historical cases
- Auto-scaling policies
- Backup strategy (daily snapshots)
- Encryption at rest & in transit (TLS 1.3)

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/infrastructure/terraform/main.tf""",
                    parent_key=feature2_key,
                    priority="High",
                    story_points=8
                )
                
                # Story 2.2
                print("[STORY 2.2] Creating RAG Pipeline Story...")
                self.create_story(
                    name="Implement RAG retrieval & ranking pipeline",
                    description="""Technical Story: Build RAG orchestration for resolution recommendations

Workflow:
1. Query embedding generation
2. Vector similarity search
3. Semantic filtering
4. Historical case ranking
5. Context assembly for LLM
6. Bedrock invocation with citations
7. Response parsing & confidence scoring

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/ai-agents/rag-orchestrator/src/orchestrator.py""",
                    parent_key=feature2_key,
                    priority="High",
                    story_points=13
                )
                
                # Story 2.3
                print("[STORY 2.3] Creating Resolution API Story...")
                self.create_story(
                    name="Create Resolution Service API & Lambda",
                    description="""Technical Story: Build REST API for resolution recommendations

Endpoints:
- POST /api/v1/resolutions/recommend
- GET /api/v1/resolutions/:id
- GET /api/v1/resolutions/complaint/:complaintId

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/backend/services/resolution-service""",
                    parent_key=feature2_key,
                    priority="High",
                    story_points=10
                )
            
            # FEATURE 3: Authentication
            print("\n[FEATURE 3] Creating Authentication Feature...")
            feature3_key = self.create_feature(
                name="Enterprise Authentication & Role-Based Access Control",
                description="""Secure authentication and authorization system

Requirements:
- AWS Cognito for identity management
- JWT tokens with short expiry (15 min)
- Refresh token rotation
- Role-based access control (RBAC)
- Roles: Admin, Manager, Agent, Viewer
- Data isolation by role & customer
- Audit logging of all access
- MFA support (optional)

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/backend/shared/utils""",
                epic_key=epic1_key,
                priority="High",
                story_points=13
            )
            
            if feature3_key:
                self.created_tickets["FEATURE-003"] = feature3_key
            
            # FEATURE 4: Frontend Dashboard
            print("\n[FEATURE 4] Creating Frontend Feature...")
            feature4_key = self.create_feature(
                name="Enterprise Dashboard UI with Real-time Updates",
                description="""React-based SPA for complaint management and AI insights

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

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/frontend""",
                epic_key=epic1_key,
                priority="High",
                story_points=21
            )
            
            if feature4_key:
                self.created_tickets["FEATURE-004"] = feature4_key
        
        # ========================================================================
        # EPIC 2: Enterprise Ready
        # ========================================================================
        print("\n\n[EPIC 2] Creating Enterprise Ready Epic...")
        epic2_key = self.create_epic(
            name="Enterprise Ready - Compliance, Security & Scalability",
            description="""Production hardening for enterprise deployment

Deliverables:
- SOC 2 Type II compliance
- HIPAA/GDPR ready
- Advanced monitoring & observability
- Disaster recovery setup
- Performance optimization
- Enterprise SLA targets (99.9% uptime)

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git
Timeline: Sprint 4-6 (12 weeks)
Priority: P1 High""",
            story_points=144
        )
        
        if epic2_key:
            self.created_tickets["EPIC-002"] = epic2_key
            
            # FEATURE 5: Audit Logging
            print("\n[FEATURE 5] Creating Audit Logging Feature...")
            feature5_key = self.create_feature(
                name="Comprehensive Audit Logging & Compliance Reporting",
                description="""Immutable audit trail for SOC 2 compliance

Requirements:
- Log all API calls: user, timestamp, action, resource, result
- Log all AI decisions: prompt, model, output, confidence
- Log all data access: who, what, when, why
- Immutable storage (CloudTrail + RDS)
- 7-year retention
- Searchable & queryable
- Compliance reports (monthly, annual)

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/backend/services/audit-api""",
                epic_key=epic2_key,
                priority="High",
                story_points=21
            )
            
            if feature5_key:
                self.created_tickets["FEATURE-005"] = feature5_key
            
            # FEATURE 6: Monitoring
            print("\n[FEATURE 6] Creating Monitoring Feature...")
            feature6_key = self.create_feature(
                name="Advanced Monitoring, Observability & Alerting",
                description="""Production-grade observability stack

Components:
1. CloudWatch dashboards
2. X-Ray distributed tracing
3. Alarms & Escalation
4. QuickSight reports

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git/blob/main/infrastructure/cloudformation""",
                epic_key=epic2_key,
                priority="High",
                story_points=13
            )
            
            if feature6_key:
                self.created_tickets["FEATURE-006"] = feature6_key
        
        # ========================================================================
        # EPIC 3: Scale & Optimize
        # ========================================================================
        print("\n\n[EPIC 3] Creating Scale & Optimize Epic...")
        epic3_key = self.create_epic(
            name="Scale & Optimize - Performance & Cost",
            description="""High-scale optimization for mature product

Deliverables:
- 10K concurrent users support
- Sub-2s P95 latency
- 50% cost reduction
- Advanced caching strategies
- Database query optimization
- AI model optimization

GitHub: https://github.com/Bidemiadedokun31/strategy_proj.git
Timeline: Sprint 7+ (ongoing)
Priority: P2 Medium""",
            story_points=89
        )
        
        if epic3_key:
            self.created_tickets["EPIC-003"] = epic3_key
        
        # Summary
        print("\n" + "="*80)
        print("TICKET CREATION SUMMARY")
        print("="*80)
        print(f"\nTotal Tickets Created: {len(self.created_tickets)}")
        print("\nTicket Mapping:")
        for ref_key, jira_key in sorted(self.created_tickets.items()):
            print(f"  {ref_key:15} → {jira_key}")
        print(f"\nGitHub Repository: https://github.com/Bidemiadedokun31/strategy_proj.git")
        print(f"Jira Project: SCRUM")
        print("\n" + "="*80)


if __name__ == "__main__":
    import sys
    
    # Get API token from environment or prompt
    api_token = input("Enter your Jira API Token (or press Enter to skip creation): ").strip()
    
    if api_token:
        creator = JiraTicketCreator(
            cloud_id="dbb52282-32f0-4f01-ad01-c5d16ef9a7a4",
            base_url="https://bidemiadedokun07.atlassian.net",
            api_token=api_token
        )
        creator.create_tickets()
    else:
        print("\n⚠ Skipped ticket creation. To create tickets, provide your Jira API token.")
        print("\nYou can generate an API token at: https://id.atlassian.com/manage-profile/security/api-tokens")
