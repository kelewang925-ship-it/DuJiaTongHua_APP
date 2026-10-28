"""Generate the 21 memory-book DOM pages; existing controllers own business behavior."""
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
def button(label, cls='', attrs=''):
    return f'<button type="button" class="{cls}" {attrs}>{label}</button>'
def field(label, cls='', id='', multiline=False):
    attrs=f'class="{cls}"'+(f' id="{id}"' if id else '')+f' aria-label="{label}"'
    control=f'<textarea {attrs} maxlength="500" rows="6"></textarea>' if multiline else f'<input {attrs} maxlength="100">'
    return f'<label class="v2-field"><span>{label}</span>{control}</label>'
def choices(values, attribute, cls, tabs=False):
    return f'<div class="{cls}">'+''.join(button(v, '', f'{attribute}="{v}" '+('role="tab" aria-selected="false"' if tabs else 'aria-pressed="false"')) for v in values)+'</div>'

def template_choices():
    """Decorative layout sketches; controller data and accessible names stay stable."""
    values=[('日记摘录','diary'),('照片故事','photos'),('重要时刻','moment'),('工坊作品','work'),('宠物成长','pet'),('章节扉页','chapter')]
    cards=[]
    for label,kind in values:
        sketch=f'<span class="v2-template-preview" data-preview="{kind}" aria-hidden="true"><span class="v2-mini-heading"></span><span class="v2-mini-copy"></span><span class="v2-mini-photo"></span><span class="v2-mini-mark">♡</span></span>'
        cards.append(button(sketch+f'<span>{label}</span>','',f'data-template="{label}" aria-pressed="false"'))
    return '<div class="templates v2-template-grid">'+''.join(cards)+'</div><p class="v2-note">版式示意，内容由你选择的共同回忆填入。</p>'
def heading(title, copy=''):
    return f'<div class="v2-intro"><p class="v2-eyebrow">OUR MEMORY BOOK</p><h1>{title}</h1><p class="v2-description">{copy}</p></div>'

content={
1:('', '', ''),
2:('回忆册',heading('故事，从第一本开始','把共同经历的小事，慢慢收藏成一本书。')+'<div class="v2-empty-book" aria-hidden="true"><span>我们的故事</span><i>♡</i></div>',button('新建第一本回忆册','new v2-primary')),
3:('挑选共同回忆',heading('有些日子，值得装订','从已经记录的共同片段开始。')+'<p class="month"></p>',button('开始制作','confirm v2-primary')+button('返回书架','skip')),
4:('新建回忆册',heading('先为故事，取一个名字','01 定封面　 /　 02 选回忆　 /　 03 排成书')+field('书名','book-name')+'<div class="dates v2-columns">'+field('开始月份')+field('结束月份')+'</div><p class="v2-note">月份格式：2026.10。只挑选这段时间的共同回忆。</p><h2>想从哪里开始？</h2><div class="options v2-choice-grid">'+button('挑选共同素材','','data-start="materials" aria-pressed="true"')+button('空白回忆册','','data-start="blank" aria-pressed="false"')+'</div>',button('下一步 · 设计封面','next v2-primary')),
5:('设计封面',heading('让故事，有自己的模样','选择纸张与封面，也可以放上一张共同照片。')+'<h2 id="coverName" class="cover-name"></h2><div class="v2-hero-slot"></div>'+choices(['花园午后','旅行手札','暖灯日常'],'data-theme','themes v2-choice-grid')+'<div class="v2-setting-row"><div><h2>共同照片封面</h2><p class="photo-copy"></p></div>'+button('选择照片','toggle','role="switch" aria-checked="false" aria-label="使用封面照片"')+'</div>',button('保存封面 · 继续','next v2-primary')),
6:('挑选回忆',heading('把喜欢的片段，放进来','只展示日期范围内共同可见的内容。')+choices(['全部','日记','照片','时刻','工坊','宠物'],'data-type','tabs v2-tabs',True)+'<div class="items"></div>', '<p class="v2-selection-count">已选 <strong id="selectedCount">0</strong> 份回忆</p>'+button('下一步 · 编排回忆','next v2-primary')),
7:('预览回忆',heading('这一段，放进书里吧','')+'<p class="subtitle"></p><article class="v2-preview-paper"><p class="date"></p><h2 class="diary-title"></h2><p class="copy"></p></article>',button('放进回忆册','add v2-primary')+button('暂不放入','skip')),
8:('选择书页版式',heading('同一段回忆，不同的表达','先选一种版式，内容和装饰都可以继续调整。')+template_choices(),button('使用这个版式','use v2-primary')),
9:('编辑日记书页',heading('把那天的心情，留在纸上','内容独立编辑，原始记录保持完整。')+'<div class="v2-live-preview" aria-label="书页实时预览"></div>'+field('书页标题','field title-input','page-title')+field('日记摘录','field excerpt','excerpt',True)+field('书页日期','field date','date')+field('书页寄语','field message','message')+'<div class="v2-inline-tools">'+button('更换摘录','','id="changeExcerpt"')+button('选择照片','','id="changePhoto"')+button('更换版式','','id="changeTemplate"')+'</div>',button('保存这一页','done v2-primary')),
10:('编辑照片故事',heading('照片之外，还有想说的话','最多三张共同照片，保留原图与裁剪位置。')+field('书页标题','page-title')+field('书页日期','date')+'<div class="v2-photo-slot"></div><div class="v2-inline-tools">'+''.join(button(f'照片 {i+1} · 裁剪或替换','crop '+c) for i,c in enumerate(['one','two','three']))+'</div><p class="help"></p>'+field('这一页的想法','caption',multiline=True)+'<p class="caption-count"><span id="len">0</span> / 500</p><div class="toolbar v2-inline-tools">'+''.join(button(v,'',f'data-tool="{v}"') for v in ['添加照片','添加文字','添加贴纸','更换模板'])+'</div>'+button('预览这一页','preview'),button('保存这一页','done v2-primary')),
11:('编辑重要时刻',heading('重要的日子，单独留一页','选择真实的共同时刻，再添上一句寄语。')+'<p class="selected"></p>'+button('选择重要时刻','select-action')+field('时刻名称','moment')+field('日期','date')+'<div class="v2-photo-slot"></div>'+button('更换照片','change-photo')+'<blockquote id="quote" class="quote"></blockquote>'+button('添加一句话','quote-action'),button('保存这一页','done v2-primary')),
12:('编辑成长与作品',heading('小小成长，也是我们的故事','珍藏工坊作品，或宠物成长的瞬间。')+choices(['工坊作品','宠物成长'],'data-tab','tabs v2-tabs',True)+'<h2 class="pet-name"></h2><p class="milestone"></p><p class="date"></p><div class="v2-photo-slot"></div>'+field('成长说明','caption')+'<div class="actions v2-inline-tools">'+''.join(button(v,'',f'data-action="{v}"') for v in ['换内容','换照片','添加说明'])+'</div>',button('保存这一页','done v2-primary')),
13:('整理书页',heading('让回忆，慢慢连成故事','长按拖动调整顺序，也可以使用每页的操作菜单。'),button('新增章节','add')+button('保存排列','save v2-primary')),
14:('回忆已成册',heading('故事，已经装订好了','现在就翻开看看，也可以继续把日常放进来。')+'<div class="v2-empty-book v2-complete-book" aria-hidden="true"><i>♡</i></div><p id="bookName" class="book-name"></p><p class="stats"></p>',button('开始翻阅','read v2-primary')+button('继续整理','continue')),
15:('回忆册目录','<h1 id="coverTitle"></h1><p class="cover-sub"></p><p class="tag"></p>',button('从第一页翻阅','start v2-primary')),
16:('沉浸翻阅','',''),
17:('阅读工具',heading('在这一页，停留一会儿','')+'<p class="page-label"></p><h2 class="story-title"></h2><p class="story-copy"></p><div class="tools v2-menu-list">'+''.join(button(v) for v in ['全书目录','我的书签','添加补页','整理书页','管理这本书'])+'</div>',''),
18:('留一张补页',heading('你的回应，也是一段回忆','给这一页添一张注笺，不改变原来的故事。')+'<p class="page-label"></p><p class="date"></p><p class="page-copy"></p>'+button('查看目录','toc')+choices(['写几句话','送一个表情','附上一张照片'],'data-kind','choices v2-choice-grid'),button('下一步 · 写补页','next v2-primary')),
19:('写一张补页',heading('留一点此刻的心情','')+'<h2 class="title"></h2><p class="author"></p>'+field('补页文字','message',multiline=True)+'<div class="emojis v2-inline-tools">'+''.join(button(e,'',f'data-emoji="{e}" aria-label="{v}" aria-pressed="false"') for e,v in [('💗','爱心'),('⭐','星星'),('😊','微笑'),('🌸','花朵')])+'</div><p class="emoji-preview"></p><label class="v2-upload"><span class="photo-label">附上照片</span><input type="file" accept="image/*" aria-label="补页照片"></label><div class="v2-photo-slot"></div><p class="stamp"></p>',button('放入回忆书','submit v2-primary')),
20:('阅读与补页','',''),
21:('管理回忆册',heading('好好收藏，也好好整理','')+'<div class="v2-hero-slot"></div><h2 class="book-name"></h2><p class="cover-title"></p><p class="created"></p><div class="actions v2-menu-list">'+button('修改书名','rename')+button('整理页序')+button('归档回忆册','archive')+button('删除这本回忆册','show-delete v2-danger')+'</div>',''),
}

SCRIPTS=['prototype-ui','prototype-records','prototype-preferences','prototype-dates','prototype-pet-store','prototype-pet-life-store','prototype-book-store','prototype-book-editors','prototype-book-structure','prototype-book-v2','prototype-book-reader','prototype-book']
def build(pages=None):
    for n,(title,body,actions) in content.items():
        if pages is not None and n not in pages:continue
        page=f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="description" content="独家童话 · 把共同日常装订成册"><title>{title or '回忆册'} · 独家童话</title>
<link rel="stylesheet" href="../assets/ui-foundation.css"><link rel="stylesheet" href="../assets/prototype-ui.css"><link rel="stylesheet" href="../assets/prototype-book-v2.css"></head>
<body><main class="screen book-v2" aria-label="{title or '回忆册书架'}" data-book-page="{n}"><header class="v2-header">{button('‹ 返回','back','aria-label="返回"')}<span>{title}</span><span class="v2-header-end">♡</span></header><section class="v2-content">{body}</section><footer class="v2-actions">{actions}</footer><div class="v2-extras"></div></main>
{''.join(f'<script src="../assets/{s}.js"></script>' for s in SCRIPTS)}
</body></html>
'''
        for folder in ['custom','pages']:
            (ROOT/folder/f'm08-p{n:02}.html').write_text(page,encoding='utf-8')
    if pages is not None:
        print('Built selected memory-book pages; other pages and artwork preserved.')
        return
    assets=ROOT/'assets'/'book-v2';assets.mkdir(exist_ok=True)
    for source,target in [('backgrounds/cream-paper-texture-v1.png','paper.webp'),('illustrations/couple-space-cover-v1.png','garden.webp'),('illustrations/album-cover-v1.png','journey.webp'),('illustrations/home-cover-v1.png','everyday.webp')]:
        with Image.open(ROOT.parent/'assets'/'images'/source) as image:
            image.save(assets/target,format='WEBP',quality=90,method=6)
    print('Built 21 scoped memory-book pages and copied four existing design assets.')

if __name__=='__main__':build()
