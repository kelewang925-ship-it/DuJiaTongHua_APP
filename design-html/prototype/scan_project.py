"""Capture existing prototype before changing product behavior. Run from any cwd."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import re
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]; self.nodes=[]; self.scripts=[]; self.styles=[]; self.resources=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        parent=self.stack[-1] if self.stack else None
        node={'tag':tag,'attrs':attrs,'text':'','parent':parent}
        self.nodes.append(node)
        if tag not in VOID: self.stack.append(node)
        for key in ('src','href'):
            if attrs.get(key): self.resources.append({'tag':tag,'attribute':key,'value':attrs[key]})
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if self.stack and self.stack[-1]['tag']==tag: self.stack.pop()
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i]['tag']==tag:
                node=self.stack[i]
                if tag=='script': self.scripts.append(node['text'])
                if tag=='style': self.styles.append(node['text'])
                del self.stack[i:]; break
    def handle_data(self,data):
        for node in self.stack: node['text']+=data

def tidy(text): return re.sub(r'\s+',' ',text).strip()
def safe(text): return str(text).replace('|','／').replace('\n',' ')
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    pages=[]; edges=[]; all_ids={m['id'] for m in manifest}
    for entry in manifest:
        page_id=entry['id']; path=ROOT/'custom'/f'{page_id}.html'
        raw=path.read_text(encoding='utf-8'); parsed=Page(); parsed.feed(raw)
        js='\n'.join(parsed.scripts)
        controls=[]; hidden=[]
        for node in parsed.nodes:
            tag=node['tag']; a=node['attrs']; text=tidy(node['text'])
            interactive=(tag in {'button','a','input','textarea','select'} or a.get('role') in {'button','switch','checkbox','tab'} or 'onclick' in a)
            if interactive:
                selector='#'+a['id'] if a.get('id') else tag+''.join('.'+c for c in a.get('class','').split())
                form=node['parent']
                while form and form['tag']!='form': form=form['parent']
                handler=a.get('onclick') or a.get('onchange') or a.get('onsubmit') or ''
                label=a.get('aria-label') or text or a.get('placeholder') or a.get('name') or a.get('title') or '(图标/无名称)'
                native=tag in {'input','textarea','select'}
                routes=sorted(set(re.findall(r'm\d{2}-p\d{2}(?=\.html)',handler+' '+a.get('href',''))))
                controls.append({'index':len(controls)+1,'selector_hint':selector,'tag':tag,'label':label,'attributes':a,'inline_handler':handler,'inline_routes':routes,'form_id':form['attrs'].get('id') if form else None,'native_input':native,'behavior_review':'native-input' if native else 'explicit-inline' if handler or a.get('href') else 'requires-handler-review'})
            if a.get('role') in {'dialog','alertdialog','status','alert'} or a.get('hidden') is not None or 'hidden' in a or any(k in a.get('class','').lower() for k in ['modal','sheet','toast','empty','loading','error','dialog']):
                hidden.append({'tag':tag,'id':a.get('id'),'class':a.get('class'),'role':a.get('role'),'text':text[:220]})
        refs=sorted(set(re.findall(r'm\d{2}-p\d{2}(?=\.html)',raw)))
        for target in refs: edges.append({'from':page_id,'to':target,'source':'HTML / inline JS literal; inspect handler for condition'})
        resources=parsed.resources+[{'tag':'css','attribute':'url','value':v} for v in re.findall(r'url\([\"\x27]?([^\)\"\x27]+)',raw)]
        missing=[]
        for r in resources:
            v=r['value'].split('?')[0].split('#')[0]
            if v and not re.match(r'^(data:|https?:|blob:|mailto:|javascript:|\$)',v) and not (path.parent/v).exists() and '${' not in v: missing.append(r)
        title=next((tidy(n['text']) for n in parsed.nodes if n['tag']=='h1'),entry['title'])
        primary=page_id in {'m03-p02','m04-p01','m05-p01','m06-p01','m07-p01','m07-p03','m08-p01'}
        forms=[{'id':n['attrs'].get('id'),'attributes':n['attrs']} for n in parsed.nodes if n['tag']=='form']
        pages.append({'id':page_id,'module':entry['module'],'title':title,'design_title':entry['title'],'type':'一级入口' if primary else '表单/任务' if forms or any(c['tag'] in {'input','textarea','select'} and c['attributes'].get('type')!='hidden' for c in controls) else '详情/状态/列表（逐页确认）','sha256':digest(path),'controls':controls,'forms':forms,'outgoing':refs,'states':hidden,'resources':resources,'missing_resources':missing,'script':js,'storage_keys':sorted(set(re.findall(r'(?:getItem|setItem|removeItem)\([\"\x27]([^\"\x27]+)',js))),'native_dialogs':{k:len(re.findall(r'\b'+k+r'\(',raw)) for k in ['alert','confirm','prompt']},'inline_style_bytes':sum(len(s.encode()) for s in parsed.styles),'inline_script_bytes':len(js.encode())})
    incoming={id:[] for id in all_ids}
    for edge in edges:
        if edge['to'] in incoming: incoming[edge['to']].append(edge['from'])
    for p in pages: p['incoming']=sorted(set(incoming[p['id']]))
    files=[]
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix.lower() in {'.html','.css','.js','.png','.webp','.svg','.ttf','.woff','.woff2'}:
            files.append({'path':str(path.relative_to(ROOT)).replace('\\','/'),'bytes':path.stat().st_size,'sha256':digest(path)})
    summary={'pages':len(pages),'controls':sum(len(p['controls']) for p in pages),'route_edges':len(edges),'no_incoming':[p['id'] for p in pages if not p['incoming']],'no_outgoing':[p['id'] for p in pages if not p['outgoing']],'native_dialog_counts':{k:sum(p['native_dialogs'][k] for p in pages) for k in ['alert','confirm','prompt']},'resource_types':dict(Counter(Path(f['path']).suffix for f in files))}
    (OUT/'baseline-inventory.json').write_text(json.dumps({'summary':summary,'pages':pages,'edges':edges,'files':files},ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# 交互原型初始扫描：114 页','', '本文件由 scan_project.py 从改动前的 custom 页面生成。行为分类是静态发现，不代表交互验收通过；JS 事件绑定与运行时数据需逐页复核。','', '## 页面、入口和出口','', '| ID | 页面 | 类型 | 入口 | 出口 | 控件数 |','| --- | --- | --- | --- | --- | ---: |']
    for p in pages: lines.append('| '+' | '.join(map(safe,[p['id'],p['title'],p['type'],', '.join(p['incoming']) or '目录直达',', '.join(p['outgoing']) or '无静态跳转',len(p['controls'])]))+' |')
    lines+=['','## 每页控件及已有状态','']
    for p in pages:
        lines += [f"### {p['id']} · {p['title']}",'',f"原稿：{p['design_title']}；现有本地数据键：{', '.join(p['storage_keys']) or '无'}。",'', '| 序号 | 控件定位提示 | 名称 | 静态行为 | 处理代码/出口 |','| ---: | --- | --- | --- | --- |']
        for c in p['controls']: lines.append('| '+' | '.join(map(safe,[c['index'],c['selector_hint'],c['label'],c['behavior_review'],c['inline_handler'] or c['attributes'].get('href') or ('原生输入/选择' if c['native_input'] else '详见页面脚本，需要人工匹配事件')]))+' |')
        lines+=['', '已有弹层/状态：'+('；'.join(safe(str(s)) for s in p['states']) or '未发现具名状态节点'),'']
    (OUT/'BASELINE_PAGES.md').write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8')
    graph=['# 初始导航关系','', '静态 literal 边包含条件、返回和跨页操作；动态拼接导航需另外核对。','', '```mermaid','flowchart TD']
    for p in pages: graph.append(f"  {p['id'].replace('-','_')}[\"{p['id']} {p['title'].replace(chr(34),'')}\"]")
    for e in edges: graph.append(f"  {e['from'].replace('-','_')} --> {e['to'].replace('-','_')}")
    graph+=['```','']
    (OUT/'BASELINE_NAVIGATION.md').write_text('\n'.join(graph),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
