/**
 * Opt-in, company/agent-scoped Paperclip CEO decision delegation.
 *
 * Formal Decisions remain board-only by default. An owner-configured CEO run
 * may READ queue metadata and decide only effect-free routine coordination
 * decisions. No board identity, credentials or permission is inherited.
 */
export const CEO_ROUTINE_RULE_KEY = "project_billion.routine_coordination.v1";

export type CeoDecisionMode = "off" | "read" | "routine";
export type CeoDelegationActor = {
  type: string;
  agentId?: string | null;
  companyId?: string | null;
  runId?: string | null;
  source?: string | null;
};
export type RoutineDecisionCandidate = {
  status: string;
  ruleKey: string | null;
  originAgentId: string;
  bundleId?: string | null;
  options: Array<{ id: string; effects: unknown[] }>;
  inputs?: unknown[] | null;
  targetSnapshots: Record<string, unknown>;
  metadata?: Record<string, unknown> | null;
  expiresAt: Date;
};

export function ceoDecisionMode(env: NodeJS.ProcessEnv = process.env): CeoDecisionMode {
  const mode = env.PAPERCLIP_CEO_DECISIONS_MODE ?? "off";
  return mode === "read" || mode === "routine" ? mode : "off";
}

/**
 * Requires genuine run-scoped JWT, explicitly configured company + CEO.
 * Never treats a local-trusted request, static agent key, or board cookie
 * as delegation to the CEO.
 */
export function isConfiguredCeoRun(
  actor: CeoDelegationActor,
  companyId: string,
  action: "read" | "routine",
  env: NodeJS.ProcessEnv = process.env,
): boolean {
  const mode = ceoDecisionMode(env);
  if (mode === "off" || (action === "routine" && mode !== "routine")) return false;
  const allowedCompanyId = env.PAPERCLIP_CEO_DECISIONS_COMPANY_ID;
  const allowedAgentId = env.PAPERCLIP_CEO_DECISIONS_AGENT_ID;
  if (!allowedCompanyId || !allowedAgentId || companyId !== allowedCompanyId) return false;
  return actor.type === "agent"
    && actor.source === "agent_jwt"
    && actor.companyId === companyId
    && actor.agentId === allowedAgentId
    && typeof actor.runId === "string"
    && actor.runId.length > 0;
}

/**
 * Deliberately narrow: metadata-only routine vote, no generated effects,
 * no archive proposal, no free-text inputs, no linked mutation targets,
 * no bundles, no self-approval. A result is NOT authorization to bypass any
 * broker, security, spending, approval or execution gateway.
 */
export function isCeoDelegableRoutineDecision(
  decision: RoutineDecisionCandidate,
  ceoAgentId: string,
  now = new Date(),
): boolean {
  if (decision.status !== "open" || decision.ruleKey !== CEO_ROUTINE_RULE_KEY) return false;
  if (decision.originAgentId === ceoAgentId || decision.bundleId) return false;
  if (!(decision.expiresAt instanceof Date) || decision.expiresAt.getTime() <= now.getTime()) return false;
  if (!decision.metadata || decision.metadata.kind !== "routine_coordination") return false;
  if (Object.keys(decision.metadata).some((key) => key !== "kind")) return false;
  if (!decision.targetSnapshots || Object.keys(decision.targetSnapshots).length !== 0) return false;
  if (decision.inputs && decision.inputs.length !== 0) return false;
  if (!Array.isArray(decision.options) || decision.options.length < 2) return false;
  return decision.options.every((option) => typeof option.id === "string"
    && option.id.length > 0 && Array.isArray(option.effects) && option.effects.length === 0);
}
