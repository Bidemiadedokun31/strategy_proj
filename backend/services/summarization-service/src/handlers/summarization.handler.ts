import { APIGatewayProxyHandler } from 'aws-lambda';
import { Logger } from '../../../shared/utils/logger';
import { SummarizationService } from './services/summarization.service';
import { validateSummarizationRequest } from './validators/summarization.validator';

const logger = new Logger('SummarizationHandler');
const summarizationService = new SummarizationService();

/**
 * Lambda handler for creating call transcript summaries
 * Input: Call recording or transcript text
 * Output: Multi-tier summary (executive, detailed, metrics)
 */
export const createSummary: APIGatewayProxyHandler = async (event) => {
  try {
    logger.info('Summarization request received', {
      path: event.path,
      method: event.httpMethod,
      correlationId: event.requestContext.requestId,
    });

    // Parse and validate request
    const body = JSON.parse(event.body || '{}');
    const validationResult = validateSummarizationRequest(body);

    if (!validationResult.success) {
      return {
        statusCode: 400,
        body: JSON.stringify({
          error: 'Invalid request',
          details: validationResult.errors,
        }),
      };
    }

    // Create summary
    const summary = await summarizationService.summarize(validationResult.data);

    logger.info('Summary created successfully', {
      summaryId: summary.id,
      complaintId: summary.complaintId,
      processingTimeMs: summary.processingTimeMs,
    });

    return {
      statusCode: 201,
      headers: {
        'Content-Type': 'application/json',
        'X-Request-ID': event.requestContext.requestId,
      },
      body: JSON.stringify(summary),
    };
  } catch (error) {
    logger.error('Error creating summary', {
      error: error instanceof Error ? error.message : String(error),
      correlationId: event.requestContext.requestId,
    });

    return {
      statusCode: 500,
      body: JSON.stringify({
        error: 'Internal server error',
        requestId: event.requestContext.requestId,
      }),
    };
  }
};

/**
 * Lambda handler for retrieving summary
 */
export const getSummary: APIGatewayProxyHandler = async (event) => {
  try {
    const summaryId = event.pathParameters?.id;

    if (!summaryId) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Summary ID is required' }),
      };
    }

    const summary = await summarizationService.getSummary(summaryId);

    if (!summary) {
      return {
        statusCode: 404,
        body: JSON.stringify({ error: 'Summary not found' }),
      };
    }

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(summary),
    };
  } catch (error) {
    logger.error('Error retrieving summary', {
      error: error instanceof Error ? error.message : String(error),
    });

    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Internal server error' }),
    };
  }
};

/**
 * Lambda handler for listing summaries
 */
export const listSummaries: APIGatewayProxyHandler = async (event) => {
  try {
    const complaintId = event.queryStringParameters?.complaintId;
    const limit = parseInt(event.queryStringParameters?.limit || '20', 10);
    const offset = parseInt(event.queryStringParameters?.offset || '0', 10);

    const summaries = await summarizationService.listSummaries({
      complaintId,
      limit,
      offset,
    });

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(summaries),
    };
  } catch (error) {
    logger.error('Error listing summaries', {
      error: error instanceof Error ? error.message : String(error),
    });

    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Internal server error' }),
    };
  }
};
