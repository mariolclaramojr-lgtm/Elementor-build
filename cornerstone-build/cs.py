import json, os, sys, urllib.request, base64
URL=os.environ.get("CS_MCP_URL","https://rrnewlewisthem.wpenginepowered.com/wp-json/cs-mcp/v1/mcp")
AUTH=os.environ["CS_MCP_AUTH"]  # "Basic <base64 user:application-password>"
_id=[0]
def call(_tool, **args):
    name=_tool
    _id[0]+=1
    body=json.dumps({"jsonrpc":"2.0","id":_id[0],"method":"tools/call","params":{"name":name,"arguments":args}}).encode()
    req=urllib.request.Request(URL,data=body,headers={"Authorization":AUTH,"Content-Type":"application/json","Accept":"application/json, text/event-stream","User-Agent":"curl/8.5.0"})
    with urllib.request.urlopen(req,timeout=300) as r:
        d=json.loads(r.read())
    if "error" in d: raise RuntimeError(d["error"])
    res=d["result"]
    txt="".join(c.get("text","") for c in res.get("content",[]))
    if res.get("isError"): raise RuntimeError(txt)
    try: return json.loads(txt)
    except Exception: return txt
if __name__=="__main__":
    print(json.dumps(call(sys.argv[1], **json.loads(sys.argv[2] if len(sys.argv)>2 else "{}")),indent=1)[:int(sys.argv[3]) if len(sys.argv)>3 else 100000])
