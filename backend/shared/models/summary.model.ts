import { z } from 'zod';

export const SummaryRequestSchema = z.object({
  complaintId: z.string().min(1, 'Complaint ID is required'),
  transcript: z.string().min(50, 'Transcript must be at least 50 characters'),
  language: z.enum(['en', 'es', 'fr', 'de', 'pt', 'zh']).optional().default('en'),
});

export type SummaryRequest = z.infer<typeof SummaryRequestSchema>;

export interface IKeyMetrics {
  issueCategory: string;
  sentiment: 'positive' | 'neutral' | 'negative';
  resolutionStatus: 'resolved' | 'escalated' | 'pending';
  callDuration?: string;
  agentName?: string;
}

export interface ISummary {
  id: string;
  complaintId: string;
  transcript: string;
  language: string;
  executive: string;
  detailed: string;
  keyMetrics: IKeyMetrics;
  sentiment: 'positive' | 'neutral' | 'negative';
  confidenceScore: number;
  createdAt: string;
  processingTimeMs: number;
}
