# RRS Site Assistant

A chat window in WordPress that edits a Cornerstone site for the logged-in user. The user types
"Change the Sunday service time on the home page to 10:30am" and it does it, using the tools the
**CSMCP** plugin already provides (pages, element trees, menus, forms, backups).

The site's editors need nothing: no Claude account and no setup. The agency's Anthropic API key is set
once per site, and every site's usage is billed to that one agency account.

```
Chat bubble (wp-admin + front end, admins only)
   → /wp-json/rrs-ai/v1/*        (this plugin, as the logged-in user)
   → Claude API                  (agency API key)
   → CSMCP tools, called inside WordPress (no loopback HTTP, no application password)
```

## Install (per site)

1. Install and activate **CSMCP** (`pro-extended`).
2. Upload `rrs-site-assistant.zip` (Plugins → Add New → Upload) and activate it.
3. Add the API key to `wp-config.php` (preferred), or paste it in **Settings → Site Assistant**:
   ```php
   define( 'RRS_AI_API_KEY', 'sk-ant-...' );
   ```
4. Open **Settings → Site Assistant**. Status should show *API key ✅* and *N tools found ✅*.
5. A blue chat bubble appears at the bottom right for admins, in wp-admin and on the live site.

## Who can use it

Users with `manage_options` (Administrators). To change that, use a filter in a small mu-plugin:

```php
add_filter( 'rrs_ai_capability', fn() => 'edit_pages' ); // Editors too
```

All tool calls run as the logged-in user, so CSMCP's own permission checks still apply.

## Safety

| What | How |
|---|---|
| Undo | CSMCP backs up every page write. Ask the assistant to "undo that" (it uses `cs_list_backups` / `cs_restore_backup`). |
| Big changes | The system prompt makes it ask first before deleting or unpublishing pages, replacing a whole page, or changing headers, global CSS/JS, menus or site options. Small edits go straight through. |
| New pages | Created as drafts, with a preview link. |
| Audit trail | Every write is logged under **Tools → Assistant Log** (user, tool, input, result). |
| Cost | Monthly token cap in Settings (default 5M tokens). Usage is shown on the settings page. |
| Key | Never sent to the browser. In wp-config it never touches the database. |

## Settings

| Setting | Default | Notes |
|---|---|---|
| Model | `claude-opus-5-5` | Any Claude model ID. |
| Effort | `medium` | `low` is faster and cheaper; `high` is more careful on big builds. |
| CSMCP REST route | `/cs-mcp/v1/mcp` | Change only if CSMCP uses a different route. |
| Monthly token cap | 5,000,000 | 0 = no cap. |

## How it works (for developers)

- `includes/class-mcp-bridge.php`: speaks MCP JSON-RPC (`initialize` → `tools/list` / `tools/call`)
  to CSMCP through `rest_do_request()`, in the same PHP process, as the current user. Tool list is
  cached for 1 hour (cleared when settings are saved). Tool output over 80k characters is cut off,
  with a note telling the model to ask for less.
- `includes/class-claude.php`: one Messages API call through `wp_remote_post`. It uses prompt caching
  and `fallbacks: "default"` (beta `server-side-fallback-2026-07-01`), which re-runs a declined turn
  on a fallback model. It doesn't use the Composer SDK because bundled Guzzle versions clash between
  WordPress plugins.
- `includes/class-chat.php`: REST routes, the system prompt (filter `rrs_ai_system_prompt`), and the
  write log. **The browser drives the loop one step at a time** (`/message`, then `/continue` until
  `done`), so no PHP request runs longer than one model call plus its tools. That keeps it under
  WP Engine's 60-second limit. The conversation is stored per user in user meta; "New chat" clears it.
- `assets/chat.js` / `chat.css`: the bubble widget, with no dependencies. It is not loaded inside iframes,
  such as the Cornerstone preview.

## Known limits (v0.1)

- One conversation per user.
- One model step must finish within the host's request timeout. Very large page rebuilds at high
  effort can hit it. If that happens, press **Retry** or use `low` / `medium` effort.
- If CSMCP only accepts Application-Password requests (not the logged-in user), the settings page
  will show the error. CSMCP then needs to allow `current_user_can( 'manage_options' )`.
