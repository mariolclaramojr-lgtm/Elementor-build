"""Add the footer overlay Global Color, save the Footer component and the site-wide footer layout."""
import json, os, sys, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
spec = importlib.util.spec_from_file_location('m', os.environ['EDW_MCP']); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
STATE = os.environ['EDW_STATE']; st = json.load(open(STATE))
def tool(n, **a):
    r = m.call('tools/call', {'name': n, 'arguments': a}); t = r['result']['content'][0]['text']
    if r['result'].get('isError'): raise SystemExit(n + ' ERROR ' + t[:1500])
    try: return json.loads(t)
    except Exception: return t
def unslash(s): return s.replace('\\\\', '\x00').replace('\\"', '"').replace('\x00', '\\')
def slash(s): return s.replace('\\', '\\\\').replace('"', '\\"')
raw = tool('cs_get_option', name='cornerstone_color_items')['value']; items = json.loads(unslash(raw))
if not any(i['_id'] == 'edwards-overlay-footer' for i in items):
    items.append({'title': 'Edwards Overlay – Footer', 'value': 'linear-gradient(180deg, rgba(34, 45, 56, 0.8) 0%, rgba(34, 45, 56, 0.9) 45%, rgba(34, 45, 56, 0.97) 100%)', '_id': 'edwards-overlay-footer'})
    tool('cs_update_option', name='cornerstone_color_items', value=slash(json.dumps(items, separators=(',', ':')))); print('overlay colour added')
import footer
args = dict(title='Footer – Edwards', elements=footer.footer_component)
if st.get('footer_component'): args['id'] = st['footer_component']
r = tool('cs_save_component', **args); st['footer_component'] = r['id']; print('component', r['id'])
args = dict(type='footer', title='Edwards Footer', regions=footer.footer_regions(st['footer_component']),
            settings={'assignments': [{'group': True, 'condition': 'site:entire-site', 'value': ''}], 'assignment_priority': 10})
if st.get('footer_layout'): args['id'] = st['footer_layout']
r = tool('cs_save_layout', **args); st['footer_layout'] = r['id']; print('footer layout', r['id'], json.dumps(r)[:300])
json.dump(st, open(STATE, 'w'), indent=1)
