import { BedrockRuntimeClient, InvokeModelCommand } from '@aws-sdk/client-bedrock-runtime';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, GetCommand, PutCommand, QueryCommand } from '@aws-sdk/lib-dynamodb';
import { Logger } from '../../../shared/utils/logger';
import { ISummary, SummaryRequest } from '../../../shared/models/summary.model';
import { nanoid } from 'nanoid';

const logger = new Logger('SummarizationService');
const bedrockClient = new BedrockRuntimeClient({ region: process.env.AWS_REGION || 'us-east-1' });
const ddbClient = new DynamoDBClient({ region: process.env.AWS_REGION || 'us-east-1' });
const docClient = DynamoDBDocumentClient.from(ddbClient);

const SUMMARIES_TABLE = process.env.SUMMARIES_TABLE || 'smartresolve-summaries';
const MODEL_ID = process.env.BEDROCK_MODEL_ID || 'anthropic.claude-3-sonnet-20240229-v1:0';

export class SummarizationService {
  /**
   * Summarize a call transcript into multiple tiers
   */
  async summarize(request: SummaryRequest): Promise<ISummary> {
    const startTime = Date.now();

    try {
      logger.info('Starting summarization', {
        complaintId: request.complaintId,
        transcriptLength: request.transcript?.length || 0,
      });

      // Call Bedrock to generate summary
      const bedrockResponse = await this.callBedrockSummarization(request);
      const parsedSummary = JSON.parse(bedrockResponse);

      // Create summary object
      const summary: ISummary = {
        id: nanoid(),
        complaintId: request.complaintId,
        transcript: request.transcript || '',
        language: request.language || 'en',
        executive: parsedSummary.executive,
        detailed: parsedSummary.detailed,
        keyMetrics: parsedSummary.keyMetrics,
        sentiment: parsedSummary.sentiment,
        confidenceScore: parsedSummary.confidenceScore,
        createdAt: new Date().toISOString(),
        processingTimeMs: Date.now() - startTime,
      };

      // Store in DynamoDB
      await this.storeSummary(summary);

      logger.info('Summary created successfully', {
        summaryId: summary.id,
        processingTimeMs: summary.processingTimeMs,
      });

      return summary;
    } catch (error) {
      logger.error('Summarization failed', {
        error: error instanceof Error ? error.message : String(error),
        complaintId: request.complaintId,
      });
      throw error;
    }
  }

  /**
   * Call Bedrock Claude for summarization
   */
  private async callBedrockSummarization(request: SummaryRequest): Promise<string> {
    const prompt = this.buildPrompt(request);

    const command = new InvokeModelCommand({
      modelId: MODEL_ID,
      contentType: 'application/json',
      accept: 'application/json',
      body: JSON.stringify({
        anthropic_version: 'bedrock-2023-06-01',
        max_tokens: 2048,
        messages: [
          {
            role: 'user',
            content: prompt,
          },
        ],
      }),
    });

    const response = await bedrockClient.send(command);
    const body = JSON.parse(new TextDecoder().decode(response.body));
    
    return body.content[0].text;
  }

  /**
   * Build prompt for Bedrock
   */
  private buildPrompt(request: SummaryRequest): string {
    return `Analyze the following call transcript and provide a structured summary in JSON format.

TRANSCRIPT:
${request.transcript}

Please respond with ONLY valid JSON (no markdown, no code blocks) with this exact structure:
{
  "executive": "Brief 1-2 sentence summary of the key issue",
  "detailed": "Comprehensive 3-5 paragraph analysis of the complaint, resolution discussion, and outcome",
  "keyMetrics": {
    "issueCategory": "e.g., Billing, Technical Support, Refund, etc.",
    "sentiment": "positive|neutral|negative",
    "resolutionStatus": "resolved|escalated|pending",
    "callDuration": "HH:MM:SS format",
    "agentName": "if mentioned"
  },
  "sentiment": "positive|neutral|negative",
  "confidenceScore": 0.95
}`;
  }

  /**
   * Store summary in DynamoDB
   */
  private async storeSummary(summary: ISummary): Promise<void> {
    const command = new PutCommand({
      TableName: SUMMARIES_TABLE,
      Item: {
        id: summary.id,
        complaintId: summary.complaintId,
        executive: summary.executive,
        detailed: summary.detailed,
        keyMetrics: summary.keyMetrics,
        sentiment: summary.sentiment,
        confidenceScore: summary.confidenceScore,
        createdAt: summary.createdAt,
        processingTimeMs: summary.processingTimeMs,
        ttl: Math.floor(Date.now() / 1000) + 90 * 24 * 60 * 60, // 90 days
      },
    });

    await docClient.send(command);
  }

  /**
   * Retrieve summary by ID
   */
  async getSummary(summaryId: string): Promise<ISummary | null> {
    const command = new GetCommand({
      TableName: SUMMARIES_TABLE,
      Key: { id: summaryId },
    });

    const response = await docClient.send(command);
    return response.Item as ISummary | undefined || null;
  }

  /**
   * List summaries with pagination
   */
  async listSummaries(options: {
    complaintId?: string;
    limit: number;
    offset: number;
  }): Promise<{ items: ISummary[]; total: number }> {
    const { complaintId, limit, offset } = options;

    if (!complaintId) {
      return { items: [], total: 0 };
    }

    const command = new QueryCommand({
      TableName: SUMMARIES_TABLE,
      IndexName: 'complaintId-createdAt-index',
      KeyConditionExpression: 'complaintId = :complaintId',
      ExpressionAttributeValues: {
        ':complaintId': complaintId,
      },
      Limit: limit,
      ExclusiveStartKey: offset > 0 ? { offset } : undefined,
      ScanIndexForward: false, // Most recent first
    });

    const response = await docClient.send(command);

    return {
      items: (response.Items as ISummary[]) || [],
      total: response.Count || 0,
    };
  }
}
