BASE='http://127.0.0.1:8765/'
def seed(p,books=None,records=None):
    p.goto(BASE+'prototype/review.html')
    p.evaluate('''data=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem('dujia-prototype-today','2026-10-05');localStorage.setItem('dujia-prototype-books',JSON.stringify(data.books));localStorage.setItem('dujia-prototype-records',JSON.stringify(data.records));localStorage.setItem('dujia-profile',JSON.stringify({nickname:'小满'}));localStorage.setItem('dujia-prototype-relationship',JSON.stringify({bound:true,partner:'阿舟'}));}''',{'books':books or [],'records':records or []})
def go(p,n,query=''):p.goto(BASE+f'pages/m08-p{n:02}.html'+query)
def value(p):return p.evaluate("JSON.parse(localStorage.getItem('dujia-prototype-books'))")
def fail(p,operation):p.evaluate("op=>sessionStorage.setItem('dujia-prototype-fail-next',op)",operation)
def fixture(id='book-state'):
    return dict(id=id,name='共同测试册',dates=['2026.10','2026.10'],start='materials',theme='花园午后',coverPhoto=False,status='published',chapters=[dict(id='chapter-state',name='第一章')],pages=[dict(id='page-state',source=dict(kind='diary',id='source-state'),chapterId='chapter-state',template='日记摘录')],selected=[dict(kind='diary',id='source-state')],bookmarks=[],lastPage=None,archived=False,createdAt=1791158400000,updatedAt=1791158400000)
def records():return [dict(id='source-state',type='diary',title='共同正文',body='SOURCE-SECRET',date='2026-10-04',visibility='shared',status='published',author='小满')]
