import {
  apiClient,
} from '@/api/client'
import type {
  AmbiguityDetectionResult,
  ConflictAnalysisResult,
  GeneratePolicyRequest,
  GeneratePolicyResult,
  TestCaseGenerationResult,
} from '@/types/ai'

export async function generatePolicy(
  payload: GeneratePolicyRequest,
): Promise<GeneratePolicyResult> {
  const response =
    await apiClient.post<GeneratePolicyResult>(
      '/ai/policies/generate',
      payload,
    )

  return response.data
}

export async function clarifyPolicy(
  policyText: string,
): Promise<AmbiguityDetectionResult> {
  const response =
    await apiClient.post<AmbiguityDetectionResult>(
      '/ai/policies/clarify',
      {
        policy_text: policyText,
      },
    )

  return response.data
}

export async function checkPolicyConflicts(
  policyA: string,
  policyB: string,
): Promise<ConflictAnalysisResult> {
  const response =
    await apiClient.post<ConflictAnalysisResult>(
      '/ai/policies/check-conflicts',
      {
        policy_a: policyA,
        policy_b: policyB,
      },
    )

  return response.data
}

export async function generatePolicyTests(
  policyDefinition: string,
): Promise<TestCaseGenerationResult> {
  const response =
    await apiClient.post<TestCaseGenerationResult>(
      '/ai/policies/generate-tests',
      {
        policy_definition:
          policyDefinition,
      },
    )

  return response.data
}
