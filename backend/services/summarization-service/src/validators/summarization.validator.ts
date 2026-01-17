import { SummaryRequestSchema, type SummaryRequest } from '../../shared/models/summary.model';

export interface ValidationResult<T> {
  success: boolean;
  data?: T;
  errors?: Record<string, string[]>;
}

export function validateSummarizationRequest(
  data: unknown
): ValidationResult<SummaryRequest> {
  try {
    const validData = SummaryRequestSchema.parse(data);
    return {
      success: true,
      data: validData,
    };
  } catch (error) {
    if (error instanceof Error && 'errors' in error) {
      const zodErrors = error as any;
      const errorMap: Record<string, string[]> = {};

      zodErrors.errors?.forEach((err: any) => {
        const path = err.path.join('.');
        if (!errorMap[path]) {
          errorMap[path] = [];
        }
        errorMap[path].push(err.message);
      });

      return {
        success: false,
        errors: errorMap,
      };
    }

    return {
      success: false,
      errors: { general: ['Unknown validation error'] },
    };
  }
}
