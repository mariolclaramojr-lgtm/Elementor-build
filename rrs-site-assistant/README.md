# RRS Site Assistant

**One plugin.** It adds a chat window in WordPress that edits a Themeco Pro / Cornerstone site for the
logged-in admin. The admin types "Change the Sunday service time on the home page to 10:30am" and the
assistant does it.

It includes **CSMCP 0.8.0** (the Cornerstone tools: pages, element trees, menus, forms, media,
backups, SEO fields). Nothing else needs to be installed.

The site's editors need nothing: no Claude account and no setup. The agency's Anthropic API key is set
once per site, and every site's usage is billed to that one agency account.

```
Chat bubble (wp-admin + live site, admins only)
   → /wp-json/rrs-ai/v1/*        (as the logged-in user)
   → Claude API                  (agency API key)
   → bundled CSMCP tools, called directly in PHP
```

## Install (per site)

1. Upload `rrs-site-assistant.zip` (Plugins → Add New → Upload) and activate it.
   If the separate **CSMCP** plugin is active, it is switched off automatically. Its settings,
   activity log, backups and SEO fields carry over. You can then delete it.
2. Add the API key to `wp-config.php` (preferred), or paste it in **Settings → Site Assistant**:
   ```php
   define( 'RRS_AI_API_KEY', 'sk-ant-...' );
   ```
3. **Settings → Site Assistant** should show the key as saved and "33 tools available".
4. A blue chat bubble appears at the bottom right for admins, in wp-admin and on the live site.

## Admin screens

| Where | What |
|---|---|
| **Settings → Site Assistant** | API key, model, effort, monthly token cap, Claude Code endpoint on/off |
| **Settings → CSMCP** | Turn tools on/off, read-only mode, **activity log and backups**, Application Password for Claude Code |

Tools switched off in Settings → CSMCP, and read-only mode, apply to the chat too.

## Who can use the chat

Users with `manage_options` (Administrators). To change that:

```php
add_filter( 'rrs_ai_capability', fn() => 'edit_pages' ); // Editors too
```

Tools run as the logged-in user, so CSMCP's per-post permission checks still apply.

## Safety

| What | How |
|---|---|
| Undo | Every page write is backed up first. Ask the assistant to "undo that" (it uses `cs_list_backups` / `cs_restore_backup`), or use Settings → CSMCP → Activity & backups. |
| Big changes | The assistant asks before deleting or unpublishing pages, replacing a whole page, or changing headers, global CSS/JS, menus or site options. Small edits go straight through. |
| New pages | Created as drafts, with a preview link. |
| Audit trail | Every write is listed in Settings → CSMCP → Activity (user, tool, page). |
| Read-only switch | Settings → CSMCP lets the assistant look but not change anything. |
| Cost | Monthly token cap (default 5M tokens). Usage is shown on the settings page. |
| Key | Never sent to the browser. In wp-config it never touches the database. |

## Claude Code (team builds)

The MCP endpoint `/wp-json/cs-mcp/v1/mcp` still works for building sites with Claude Code, as in
`HTML-TO-CORNERSTONE.md`. Connect with an Application Password from Settings → CSMCP. Switch the endpoint
off in Settings → Site Assistant on sites where nobody builds with Claude Code. The chat doesn't use it.

## Files

| File | What |
|---|---|
| `rrs-site-assistant.php` | Loads everything and switches off a standalone CSMCP on activation |
| `includes/csmcp/` | CSMCP 0.8.0, unchanged (class names, options and meta kept for compatibility) |
| `includes/class-tools-bridge.php` | Gives the CSMCP tools to the chat (tool list, calls, 80k-character output limit) |
| `includes/class-claude.php` | Claude Messages API call through `wp_remote_post`. Uses prompt caching and `fallbacks: "default"` (beta `server-side-fallback-2026-07-01`). It doesn't use the Composer SDK because bundled Guzzle versions clash between WordPress plugins. |
| `includes/class-chat.php` | REST routes and system prompt (filter `rrs_ai_system_prompt`; CSMCP's own Cornerstone notes are added to it). The browser drives the loop one step at a time (`/message`, then `/continue`), so no PHP request runs longer than one model call plus its tools. That keeps it under WP Engine's 60-second limit. |
| `includes/class-settings.php` | Settings page and usage counter |
| `assets/chat.js`, `chat.css` | The chat bubble, with no dependencies. It isn't loaded inside iframes, such as the Cornerstone preview. |

## Known limits (v0.2)

- One conversation per user.
- One model step must finish within the host's request timeout. Very large page rebuilds at high
  effort can hit it. If that happens, press **Retry** or use `low` / `medium` effort.
- Don't re-activate a standalone CSMCP while this plugin is active. WordPress will refuse with a
  "fatal error" message, because both contain the same classes. The site itself is not affected.
