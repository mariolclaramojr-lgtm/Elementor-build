import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from logo2 import font,text,svg
ARCH='M6 55V24a18 18 0 0 1 36 0v31'
def frame(c,sw): return f'<path d="{ARCH}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/><path d="M2 55h44" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"/>'
def sunrise(c,a,sw=2.2):
    return frame(c,sw)+(f'<path d="M14 55a10 10 0 0 1 20 0" fill="{a}"/>'
      f'<g stroke="{a}" stroke-width="{sw}" stroke-linecap="round"><path d="M24 39v-8"/><path d="M14.2 43.2l-4.6-4.6"/><path d="M33.8 43.2l4.6-4.6"/></g>')
def flame(c,a,sw=2.2):
    return frame(c,sw)+(f'<path d="M24 20c1.5 7 9 10.5 9 19.5a9 9 0 0 1-18 0c0-4.5 2.4-7.4 4.3-9.6.4 3 1.8 4.8 3.6 5.6-1-6.2.3-11 1.1-15.5z" fill="{a}"/>')
def sprout(c,a,sw=2.2):
    return frame(c,sw)+(f'<path d="M24 55V33" stroke="{a}" stroke-width="{sw}" stroke-linecap="round"/>'
      f'<path d="M24 38c0-7-5-11-12-11 0 7 5 11 12 11z" fill="{a}"/>'
      f'<path d="M24 33c0-8 5-13 12-13 0 8-5 13-12 13z" fill="{a}"/>')
def dove(c,a,sw=2.2):
    return frame(c,sw)+(f'<path d="M12 41c6 1 10-1 13-5l-5-11c5 1 8 4 10 8l3-4c2-2 5-2 6 0l-3 2c0 6-4 12-11 14-5 1.5-10 .5-13-4z" fill="{a}"/>')
def lockup(markfn,word,sub,acc):
    fr=font('Fraunces',wght=560,opsz=72,SOFT=0,WONK=0); dm=font('DMSans',wght=600,opsz=14)
    p1,w1=text('Hayford',fr,40,66,33,track=-0.01); p2,w2=text('CHURCH',dm,9,67.5,56,track=0.62)
    return svg(66+max(w1,w2)+2,58,f'<g transform="translate(0 1)">{markfn(word,acc)}</g><path d="{p1}" fill="{word}"/><path d="{p2}" fill="{sub}"/>')
if __name__=='__main__':
    out=os.path.join(os.path.dirname(os.path.abspath(__file__)),'logo3');os.makedirs(out,exist_ok=True)
    for n,f in [('1-sunrise',sunrise),('2-flame',flame),('3-sprout',sprout),('4-dove',dove)]:
        open(f'{out}/{n}-light.svg','w').write(lockup(f,'#0E1013','#3B55E6','#3B55E6'))
        open(f'{out}/{n}-dark.svg','w').write(lockup(f,'#FFFFFF','#AFBDFF','#AFBDFF'))
        open(f'{out}/{n}-mark.svg','w').write(svg(48,58,f'<g transform="translate(0 1)">{f("#0E1013","#3B55E6")}</g>'))
    rows=''.join(f'<div class="r"><div class="t">{n[0]}</div><div class="l"><img src="{n}-light.svg"></div><div class="d"><img src="{n}-dark.svg"></div><div class="l"><img class="m" src="{n}-mark.svg"></div></div>' for n in ['1-sunrise','2-flame','3-sprout','4-dove'])
    open(f'{out}/sheet.html','w').write('<html><body style="margin:0"><style>.r{display:grid;grid-template-columns:80px 1fr 1fr 180px}.r>div{display:flex;align-items:center;justify-content:center;height:160px}.l{background:#F4F5F7}.d{background:#0E1013}.t{font:700 34px sans-serif;color:#555}img{height:62px}img.m{height:110px}</style>'+rows+'</body></html>')
    print('ok')
