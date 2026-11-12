import { describe, expect, it } from "vitest";
import {
  CEO_ROUTINE_RULE_KEY,
  ceoDecisionMode,
  isCeoDelegableRoutineDecision,
  isConfiguredCeoRun,
} from "./ceo-decision-delegation.js";

const COMPANY = "dcb9fb2c-78cb-42ee-8a41-87fc6595d5ab";
const CEO = "f63771b3-68ea-4f92-8f9b-8d7cba2679f2";
const OTHER = "afb18681-64a3-4c13-ae30-1cd17dfb80d4";
const config = {
  PAPERCLIP_CEO_DECISIONS_MODE: "routine",
  PAPERCLIP_CEO_DECISIONS_COMPANY_ID: COMPANY,
  PAPERCLIP_CEO_DECISIONS_AGENT_ID: CEO,
};
const actor = { type: "agent", agentId: CEO, companyId: COMPANY, runId: "run-1", source: "agent_jwt" };
const decision = () => ({
  status: "open", ruleKey: CEO_ROUTINE_RULE_KEY, originAgentId: OTHER,
  bundleId: null,
  options: [{ id: "proceed", effects: [] }, { id: "revise", effects: [] }],
  inputs: null, targetSnapshots: {},
  metadata: { kind: "routine_coordination" },
  expiresAt: new Date(Date.now() + 60_000),
});

describe("CEO formal Decision delegation: identity", () => {
  it("is off by default and rejects missing configuration", () => {
    expect(ceoDecisionMode({})).toBe("off");
    expect(isConfiguredCeoRun(actor, COMPANY, "read", {})).toBe(false);
  });
  it("permits only configured, genuine CEO JWTs from the right company", () => {
    expect(isConfiguredCeoRun(actor, COMPANY, "read", config)).toBe(true);
    expect(isConfiguredCeoRun(actor, COMPANY, "routine", config)).toBe(true);
    expect(isConfiguredCeoRun({ ...actor, source: "agent_key" }, COMPANY, "routine", config)).toBe(false);
    expect(isConfiguredCeoRun({ ...actor, runId: null }, COMPANY, "routine", config)).toBe(false);
    expect(isConfiguredCeoRun({ ...actor, agentId: OTHER }, COMPANY, "routine", config)).toBe(false);
    expect(isConfiguredCeoRun({ ...actor, type: "board" }, COMPANY, "routine", config)).toBe(false);
    expect(isConfiguredCeoRun(actor, "other-company", "routine", config)).toBe(false);
  });
  it("read-only mode cannot resolve decisions", () => {
    const read = { ...config, PAPERCLIP_CEO_DECISIONS_MODE: "read" };
    expect(isConfiguredCeoRun(actor, COMPANY, "read", read)).toBe(true);
    expect(isConfiguredCeoRun(actor, COMPANY, "routine", read)).toBe(false);
  });
  it("ignores invalid modes and missing agent identity", () => {
    expect(isConfiguredCeoRun(actor, COMPANY, "read", { ...config, PAPERCLIP_CEO_DECISIONS_MODE: "all" })).toBe(false);
    expect(isConfiguredCeoRun(actor, COMPANY, "read", { ...config, PAPERCLIP_CEO_DECISIONS_AGENT_ID: "" })).toBe(false);
  });
});

describe("CEO formal Decision delegation: limited routine eligibility", () => {
  it("permits genuine effect-free routine coordination decisions", () => {
    expect(isCeoDelegableRoutineDecision(decision(), CEO)).toBe(true);
  });
  it("rejects all actions that could carry executable effects", () => {
    expect(isCeoDelegableRoutineDecision({ ...decision(), options: [{ id: "proceed", effects: [{ type: "create_issue" }] }, { id: "reject", effects: [] }] }, CEO)).toBe(false);
    expect(isCeoDelegableRoutineDecision({ ...decision(), targetSnapshots: { protectedIssue: {} } }, CEO)).toBe(false);
    expect(isCeoDelegableRoutineDecision({ ...decision(), inputs: [{ id: "budget" }] }, CEO)).toBe(false);
    expect(isCeoDelegableRoutineDecision({ ...decision(), metadata: { kind: "attention_archive_proposal" } }, CEO)).toBe(false);
    expect(isCeoDelegableRoutineDecision({ ...decision(), metadata: { kind: "routine_coordination", governedActionId: "secret" } }, CEO)).toBe(false);
  });
  it("preserves the board boundary for arbitrary, bundled, expired and self-created decisions", () => {
    expect(isCeoDelegableRoutineDecision({ ...decision(), ruleKey: "trading.live_execution" }, CEO)).toBe(false);
    expect(isCeoDelegableRoutineDecision({ ...decision(), bundleId: "bundle" }, CEO)).toBe(false);
    expect(isCeoDelegableRoutineDecision({ ...decision(), expiresAt: new Date(0) }, CEO)).toBe(false);
    expect(isCeoDelegableRoutineDecision({ ...decision(), originAgentId: CEO }, CEO)).toBe(false);
    expect(isCeoDelegableRoutineDecision({ ...decision(), status: "decided" }, CEO)).toBe(false);
  });
});
