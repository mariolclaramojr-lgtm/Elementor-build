"""Hayford Cornerstone build helpers: JSON-RPC client + global ids."""
import json,urllib.request,time
_cfg=json.load(open('/root/.claude.json'))['mcpServers']['cs-mcp']
_H={'Authorization':_cfg['headers']['Authorization'],'Content-Type':'application/json','Accept':'application/json, text/event-stream','User-Agent':'curl/8.5.0'}
def call(name,args=None,quiet=False):
    body=json.dumps({'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':name,'arguments':args or {}}}).encode()
    for attempt in range(3):
        try:
            t=urllib.request.urlopen(urllib.request.Request(_cfg['url'],body,_H),timeout=300).read().decode();break
        except Exception as e:
            if attempt==2: raise
            time.sleep(3)
    d=json.loads(t[t.find('{'):])
    if 'error' in d: raise RuntimeError(d['error'])
    txt=''.join(c.get('text','') for c in d['result'].get('content',[]))
    if d['result'].get('isError'): raise RuntimeError(txt[:2000])
    try: return json.loads(txt)
    except Exception: return txt

# Global colour ids (existing ids kept so earlier references stay valid)
C=dict(white='6dda5a93-484f-4597-9c18-c4bee57d7b0e', black='7b712075-ae81-4c02-b53f-34100a786994',
       ink='4272616e64205072696d617279', ink_soft='4272616e64205365636f6e64617279',
       link='4c696e6b', link_alt='4c696e6b20496e746572616374696f6e', accent='fd0f76da-a9d9-4855-b526-e420c3cd4cd8',
       ink2='68662d696e6b2d32', paper='68662d7061706572', sand='68662d73616e64', muted='68662d6d75746564',
       accent_dark='68662d616363656e742d6461726b', accent_light='68662d616363656e742d6c69676874',
       line='68662d6c696e65', line_dark='68662d6c696e652d6461726b', live='68662d6c697665')
def gc(k,alpha=None): return f'global-color:{C[k]}'+(f':{alpha}' if alpha is not None else '')
F=dict(body='426f647920436f7079', head='48656164696e6773', serif='416363656e74205365726966')
