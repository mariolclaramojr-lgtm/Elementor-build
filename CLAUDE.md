# Project notes for Claude

## When the user pastes a `claude mcp add ...` command

The user regularly pastes a command like:

    claude mcp add --transport http --scope user <name> <url> --header "Authorization: Basic ..."

Every time this happens, do all of this without asking:

1. Run the command exactly as pasted, then `claude mcp list` to confirm it shows **Connected**.
2. Servers only load when a session starts, so its tools will NOT appear in the current
   session. Do not stop there or tell the user to restart. Instead, use it right away through
   the helper, which reads the URL and headers from `~/.claude.json`:

       python3 tools/mcp_call.py <name> list
       python3 tools/mcp_call.py <name> schema <tool>
       python3 tools/mcp_call.py <name> call <tool> '<json args>'   # or @file.json

3. Make a first real call to prove it works (for `cs-mcp`: `cs_environment`), then report
   back briefly: connected, site/versions, and the tools available.
4. Follow the server's own `instructions` (returned by `initialize`) when using its tools.

Never write the pasted Authorization header or password into any file in this repo, commit
message, or other outside service. It lives only in `~/.claude.json` inside the container.

## cs-mcp (Themeco Pro / Cornerstone)

Usual server: `cs-mcp` at `https://<site>/wp-json/cs-mcp/v1/mcp` (the user's CSMCP plugin).
Workflow: `cs_environment` → `cs_element_catalog` → `cs_get_element_tree` on a reference page,
copy real element shapes, write (backups are automatic, new pages are drafts), then
`cs_purge_cache`. See `HTML-TO-CORNERSTONE.md` for conversion notes.
