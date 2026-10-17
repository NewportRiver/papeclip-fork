from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from .service import AuthorizationError, CorporateMemoryService, ValidationError, token_roles


def tool_definitions() -> list[dict[str, Any]]:
    return [
        {"name": "search_knowledge", "description": "Search approved corporate knowledge.", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer"}}, "required": ["query"]}},
        {"name": "read_knowledge", "description": "Read one approved corporate record.", "inputSchema": {"type": "object", "properties": {"record_id": {"type": "string"}}, "required": ["record_id"]}},
        {"name": "propose_knowledge", "description": "Propose knowledge for review; never publishes directly.", "inputSchema": {"type": "object", "properties": {"title": {"type": "string"}, "body": {"type": "string"}, "domain": {"type": "string"}, "scope": {"type": "string"}, "classification": {"type": "string"}, "owner": {"type": "string"}, "source": {"type": "string"}, "rationale": {"type": "string"}, "evidence_class": {"type": "string"}}, "required": ["title", "body", "domain", "scope", "classification", "owner", "source", "rationale"]}},
        {"name": "review_knowledge", "description": "Approve or reject a pending proposal.", "inputSchema": {"type": "object", "properties": {"proposal_id": {"type": "string"}, "decision": {"type": "string", "enum": ["approve", "reject"]}, "notes": {"type": "string"}}, "required": ["proposal_id", "decision"]}},
        {"name": "publish_knowledge", "description": "Publish a reviewed and approved proposal.", "inputSchema": {"type": "object", "properties": {"proposal_id": {"type": "string"}}, "required": ["proposal_id"]}},
        {"name": "memory_health", "description": "Check database integrity and schema version.", "inputSchema": {"type": "object", "properties": {}}},
    ]


def result(value: Any) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": json.dumps(value, sort_keys=True)}]}


def main() -> None:
    db_path = Path(os.environ.get("CORPORATE_MEMORY_DB", "./data/corporate-memory.sqlite3"))
    roles = token_roles()
    token = os.environ.get("CORPORATE_MEMORY_ACCESS_TOKEN", "")
    if not roles or token not in roles:
        raise SystemExit("corporate memory MCP requires a configured access token")
    actor, role = roles[token]
    service = CorporateMemoryService(db_path, actor, role)
    try:
        for line in sys.stdin:
            if not line.strip():
                continue
            request = json.loads(line)
            request_id = request.get("id")
            try:
                method = request.get("method")
                params = request.get("params") or {}
                if method == "initialize":
                    value = {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "newport-river-corporate-memory", "version": "0.1.0"}}
                elif method == "notifications/initialized":
                    continue
                elif method == "tools/list":
                    value = {"tools": tool_definitions()}
                elif method == "tools/call":
                    name = params["name"]
                    args = params.get("arguments") or {}
                    if name == "search_knowledge": value = result(service.search(args["query"], args.get("limit", 20)))
                    elif name == "read_knowledge": value = result(service.read(args["record_id"]))
                    elif name == "propose_knowledge": value = result({"proposal_id": service.propose(**args)})
                    elif name == "review_knowledge": value = result(service.review(**args))
                    elif name == "publish_knowledge": value = result(service.publish(args["proposal_id"]))
                    elif name == "memory_health": value = result(service.health())
                    else: raise KeyError(name)
                else:
                    raise KeyError(method)
                response = {"jsonrpc": "2.0", "id": request_id, "result": value}
            except (AuthorizationError, ValidationError, KeyError, ValueError) as exc:
                response = {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32000, "message": str(exc)}}
            print(json.dumps(response), flush=True)
    finally:
        service.close()


if __name__ == "__main__":
    main()
