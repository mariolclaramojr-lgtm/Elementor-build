"""Usage: EDW_MEDIA=media.json python3 run.py <step>  (steps: component, home)"""
import json, os, sys, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
spec = importlib.util.spec_from_file_location('m', os.environ['EDW_MCP']); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
STATE = os.environ.get('EDW_STATE', 'state.json')
st = json.load(open(STATE)) if os.path.exists(STATE) else {}
def tool(name, **args):
    r = m.call('tools/call', {'name': name, 'arguments': args})
    if 'error' in r: raise SystemExit(f"{name} ERROR {r['error']}")
    t = r['result']['content'][0]['text']
    if r['result'].get('isError'): raise SystemExit(f"{name} isError: {t[:1500]}")
    try: return json.loads(t)
    except Exception: return t
import home
step = sys.argv[1]
if step == 'component':
    args = dict(title='Visit Us – Service Times, Contact + Map', elements=home.visit_component)
    if st.get('visit_component'): args['id'] = st['visit_component']
    r = tool('cs_save_component', **args); print(json.dumps(r)[:600])
    st['visit_component'] = r.get('id') or r.get('component_id') or st.get('visit_component')
elif step == 'home':
    if not st.get('home_draft'):
        r = tool('cs_create_page', title='Home (Redesign Draft)', status='draft', slug='home-redesign-draft'); print(json.dumps(r)[:400])
        st['home_draft'] = r.get('id')
    r = tool('cs_save_element_tree', id=st['home_draft'], tree=home.home_tree(st['visit_component'])); print(json.dumps(r)[:800])
    print(json.dumps(tool('cs_purge_cache', id=st['home_draft']))[:200])
json.dump(st, open(STATE, 'w'), indent=1)
print('state', st)
