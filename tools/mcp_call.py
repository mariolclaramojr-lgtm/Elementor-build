#!/usr/bin/env python3
"""Call an HTTP MCP server registered with `claude mcp add` directly, for when its
tools were not loaded into the current session (servers only load at session start).

Reads the URL and headers from ~/.claude.json, so no credentials live in this repo.

Usage:
  python3 tools/mcp_call.py <server> list
  python3 tools/mcp_call.py <server> call <tool> '<json args>'
  python3 tools/mcp_call.py <server> call <tool> @args.json
"""
import json, os, subprocess, sys

def server_config(name):
    cfg = json.load(open(os.path.expanduser('~/.claude.json')))
    servers = dict(cfg.get('mcpServers', {}))
    for proj in cfg.get('projects', {}).values():
        servers.update(proj.get('mcpServers', {}))
    if name not in servers:
        sys.exit(f"MCP server '{name}' not found. Known: {', '.join(servers) or 'none'}")
    return servers[name]

def rpc(srv, method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
    cmd = ['curl', '-sS', '-X', 'POST', srv['url'],
           '-H', 'Content-Type: application/json',
           '-H', 'Accept: application/json, text/event-stream', '--data-binary', '@-']
    for k, v in srv.get('headers', {}).items():
        cmd += ['-H', f'{k}: {v}']
    out = subprocess.run(cmd, input=body, capture_output=True, text=True).stdout
    if out.lstrip().startswith(('event:', 'data:')):  # SSE response
        out = next(l[5:] for l in out.splitlines() if l.startswith('data:'))
    return json.loads(out)

def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    srv = server_config(sys.argv[1])
    if sys.argv[2] == 'list':
        for t in rpc(srv, 'tools/list', {})['result']['tools']:
            print(f"- {t['name']}: {(t.get('description') or '').splitlines()[0][:120]}")
        return
    if sys.argv[2] == 'schema':
        for t in rpc(srv, 'tools/list', {})['result']['tools']:
            if t['name'] == sys.argv[3]:
                print(json.dumps(t, indent=1))
        return
    tool = sys.argv[3]
    raw = sys.argv[4] if len(sys.argv) > 4 else '{}'
    args = json.load(open(raw[1:])) if raw.startswith('@') else json.loads(raw)
    r = rpc(srv, 'tools/call', {"name": tool, "arguments": args})
    res = r.get('result')
    if isinstance(res, dict) and 'content' in res:
        for c in res['content']:
            print(c.get('text', json.dumps(c)))
        if res.get('isError'):
            sys.exit(1)
    else:
        print(json.dumps(r, indent=1))
        sys.exit(1)

if __name__ == '__main__':
    main()
