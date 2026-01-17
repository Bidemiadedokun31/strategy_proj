"""
RAG Orchestrator for Resolution Recommendations

Orchestrates the Retrieval-Augmented Generation pipeline:
1. Query embedding generation
2. Vector similarity search on historical cases
3. Context assembly
4. LLM inference with citations
5. Confidence scoring
"""

import json
import os
from typing import Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

import boto3
from opensearchpy import OpenSearch, helpers

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AWS Clients
bedrock_client = boto3.client('bedrock-runtime', region_name=os.getenv('AWS_REGION', 'us-east-1'))
sagemaker_client = boto3.client('sagemaker-runtime', region_name=os.getenv('AWS_REGION', 'us-east-1'))

# OpenSearch client
opensearch_client = OpenSearch(
    hosts=[os.getenv('OPENSEARCH_ENDPOINT', 'localhost:9200')],
    http_auth=(os.getenv('OPENSEARCH_USER', 'admin'), os.getenv('OPENSEARCH_PASSWORD', 'admin')),
    use_ssl=True,
    verify_certs=False,
    ssl_show_warn=False,
)


@dataclass
class HistoricalCase:
    """Historical case from RAG database"""
    case_id: str
    complaint_type: str
    resolution: str
    outcome: str
    embedding: list
    similarity_score: float
    metadata: dict


@dataclass
class ResolutionRecommendation:
    """Resolution recommendation with citations"""
    id: str
    complaint_id: str
    recommendations: list
    primary_recommendation: str
    confidence_score: float
    cited_cases: list
    reasoning: str
    created_at: str
    processing_time_ms: float


class RAGOrchestrator:
    """Orchestrates RAG pipeline for resolution recommendations"""
    
    def __init__(self):
        self.model_id = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
        self.embedding_endpoint = os.getenv('SAGEMAKER_ENDPOINT', 'smartresolve-embeddings')
        self.opensearch_index = os.getenv('OPENSEARCH_INDEX', 'historical-cases')
        
    def generate_recommendation(self, complaint_summary: str, complaint_id: str) -> ResolutionRecommendation:
        """Generate resolution recommendation using RAG pipeline"""
        
        import time
        start_time = time.time()
        
        try:
            logger.info(f"Generating recommendation for complaint {complaint_id}")
            
            # Step 1: Generate embedding for query
            query_embedding = self._generate_embedding(complaint_summary)
            
            # Step 2: Retrieve similar historical cases
            similar_cases = self._retrieve_similar_cases(query_embedding, top_k=5)
            
            if not similar_cases:
                logger.warning(f"No similar cases found for complaint {complaint_id}")
                similar_cases = []
            
            # Step 3: Generate prompt with context
            prompt = self._build_recommendation_prompt(complaint_summary, similar_cases)
            
            # Step 4: Call Bedrock for recommendations
            llm_response = self._call_bedrock(prompt)
            recommendations = self._parse_llm_response(llm_response)
            
            # Step 5: Create recommendation object
            processing_time = (time.time() - start_time) * 1000
            
            recommendation = ResolutionRecommendation(
                id=self._generate_id(),
                complaint_id=complaint_id,
                recommendations=recommendations.get('recommendations', []),
                primary_recommendation=recommendations.get('primary', ''),
                confidence_score=recommendations.get('confidence', 0.8),
                cited_cases=[asdict(case) for case in similar_cases],
                reasoning=recommendations.get('reasoning', ''),
                created_at=datetime.utcnow().isoformat(),
                processing_time_ms=processing_time,
            )
            
            logger.info(f"Recommendation generated in {processing_time:.0f}ms")
            return recommendation
            
        except Exception as e:
            logger.error(f"Error generating recommendation: {str(e)}")
            raise
    
    def _generate_embedding(self, text: str) -> list:
        """Generate embedding using SageMaker endpoint"""
        try:
            response = sagemaker_client.invoke_endpoint(
                EndpointName=self.embedding_endpoint,
                ContentType='text/plain',
                Body=text.encode('utf-8')
            )
            
            embedding = json.loads(response['Body'].read().decode('utf-8'))
            return embedding['embedding']
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            # Return zero vector as fallback
            return [0.0] * 1536
    
    def _retrieve_similar_cases(self, query_embedding: list, top_k: int = 5) -> list[HistoricalCase]:
        """Search OpenSearch for similar cases using vector similarity"""
        try:
            search_body = {
                "size": top_k,
                "query": {
                    "knn": {
                        "embedding": {
                            "vector": query_embedding,
                            "k": top_k
                        }
                    }
                }
            }
            
            response = opensearch_client.search(
                index=self.opensearch_index,
                body=search_body
            )
            
            cases = []
            for hit in response['hits']['hits']:
                case_data = hit['_source']
                cases.append(HistoricalCase(
                    case_id=case_data['case_id'],
                    complaint_type=case_data['complaint_type'],
                    resolution=case_data['resolution'],
                    outcome=case_data['outcome'],
                    embedding=case_data.get('embedding', []),
                    similarity_score=hit['_score'],
                    metadata=case_data.get('metadata', {})
                ))
            
            logger.info(f"Retrieved {len(cases)} similar cases")
            return cases
            
        except Exception as e:
            logger.error(f"Error retrieving similar cases: {str(e)}")
            return []
    
    def _build_recommendation_prompt(self, complaint_summary: str, similar_cases: list[HistoricalCase]) -> str:
        """Build prompt with complaint and historical context"""
        
        context = "HISTORICAL SIMILAR CASES:\n"
        for i, case in enumerate(similar_cases, 1):
            context += f"""
Case {i} (Similarity: {case.similarity_score:.2f}):
- Type: {case.complaint_type}
- Resolution Applied: {case.resolution}
- Outcome: {case.outcome}
- Details: {json.dumps(case.metadata)}
"""
        
        prompt = f"""You are an expert customer service resolution advisor. Analyze the complaint and recommend optimal resolutions based on historical precedents.

CURRENT COMPLAINT:
{complaint_summary}

{context}

Based on the complaint and historical cases, provide:
1. Top 3 resolution recommendations (ranked by effectiveness)
2. Confidence score (0-1) for the primary recommendation
3. Reasoning that cites specific historical cases
4. Expected outcome

Respond with ONLY valid JSON (no markdown):
{{
  "recommendations": [
    {{"rank": 1, "resolution": "...", "expectedOutcome": "...", "implementation": "..."}},
    {{"rank": 2, "resolution": "...", "expectedOutcome": "...", "implementation": "..."}},
    {{"rank": 3, "resolution": "...", "expectedOutcome": "...", "implementation": "..."}}
  ],
  "primary": "...",
  "confidence": 0.85,
  "reasoning": "..."
}}"""
        
        return prompt
    
    def _call_bedrock(self, prompt: str) -> str:
        """Call Bedrock Claude for recommendations"""
        try:
            response = bedrock_client.invoke_model(
                modelId=self.model_id,
                contentType='application/json',
                accept='application/json',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-06-01",
                    "max_tokens": 1500,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                })
            )
            
            body = json.loads(response['body'].read())
            return body['content'][0]['text']
        except Exception as e:
            logger.error(f"Error calling Bedrock: {str(e)}")
            raise
    
    def _parse_llm_response(self, response: str) -> dict:
        """Parse JSON response from LLM"""
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                logger.warning("No JSON found in LLM response")
                return {"recommendations": [], "primary": "", "confidence": 0.5, "reasoning": ""}
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing LLM response: {str(e)}")
            return {"recommendations": [], "primary": "", "confidence": 0.5, "reasoning": ""}
    
    def _generate_id(self) -> str:
        """Generate unique ID"""
        import uuid
        return str(uuid.uuid4())


# Lambda handler
def lambda_handler(event, context):
    """AWS Lambda handler for recommendation generation"""
    try:
        body = json.loads(event.get('body', '{}'))
        complaint_summary = body.get('complainSummary', '')
        complaint_id = body.get('complaintId', '')
        
        if not complaint_summary or not complaint_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required fields'})
            }
        
        orchestrator = RAGOrchestrator()
        recommendation = orchestrator.generate_recommendation(complaint_summary, complaint_id)
        
        return {
            'statusCode': 201,
            'body': json.dumps(asdict(recommendation))
        }
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.stringify({'error': 'Internal server error'})
        }


if __name__ == '__main__':
    # Development testing
    print("RAG Orchestrator initialized")
