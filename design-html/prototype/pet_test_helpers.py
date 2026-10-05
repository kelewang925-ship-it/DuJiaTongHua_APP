URL='http://127.0.0.1:8765/pages/'
def go(p,n,query=''):p.goto(URL+f'm07-p{n:02}.html'+query)
def seed(p,**changes):
 p.goto('http://127.0.0.1:8765/prototype/review.html');pet=dict(id='pet-life',name='团团',kind='小狗',status='active',adoptedDate='2026-09-01',energy=82,satiety=76,mood=70,affinity=0,food=[12,5,1],gifts=1,coins=20,stars=30,owned=['小花围巾'],outfit=None,room={},claims=[],logs=[dict(id='first',type='adopt',text='共同领养了团团',actor='阿舟',date='2026-09-01',at=1)],care=True,settings=dict(reminder=True,time='20:30',notice=True,stories=True));pet.update(changes)
 p.evaluate('(pet)=>{localStorage.clear();sessionStorage.clear();sessionStorage.setItem("dujia-prototype-today","2026-10-05");localStorage.setItem("dujia-prototype-relationship",JSON.stringify({bound:true,partner:"阿舟"}));localStorage.setItem("dujia-profile",JSON.stringify({nickname:"小满"}));localStorage.setItem("dujia-prototype-records","[]");localStorage.setItem("dujia-prototype-anniversaries","[]");localStorage.setItem("dujia-prototype-moments","[]");localStorage.setItem("dujia-prototype-pet",JSON.stringify(pet));}',pet)
def value(p):return p.evaluate('JSON.parse(localStorage.getItem("dujia-prototype-pet"))')
def fail(p,operation):p.evaluate('(op)=>sessionStorage.setItem("dujia-prototype-fail-next",op)',operation)
