import base64,zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
root=Path(__file__).resolve().parent.parent
# Offline DOM integration test: actual frontend source injected into about:blank.
# HTTP navigation is blocked in the test environment; storage is mocked, no external network.
def load(page):
 r=root/'public'
 page.set_content('<html><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><div id="app"></div><div id="toast"></div></body></html>')
 page.add_style_tag(content=(r/'style.css').read_text().split('\n',1)[1])
 page.evaluate("""()=>{const mem={};Object.defineProperty(window,'localStorage',{value:{getItem:k=>mem[k]??null,setItem:(k,v)=>mem[k]=v}});window.ILMORA_CONFIG={};if(!crypto.randomUUID)crypto.randomUUID=()=> 'test-'+Math.random()}""")
 src=(r/'content.js').read_text().replace('export const','const')+'\n'+(r/'app.js').read_text().split('\n',1)[1]
 src=src.replace('/icon.svg','data:image/svg+xml;base64,'+base64.b64encode((r/'icon.svg').read_bytes()).decode())
 page.add_script_tag(content=src)
with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1440,'height':1000},accept_downloads=True)
  page.set_default_timeout(3500)
  errors=[];page.on('pageerror',lambda x:errors.append(str(x)))
  load(page);page.get_by_role('button',name='Mahalliy demoni ko‘rish').click();page.wait_for_selector('.hero');page.wait_for_timeout(1100)
  page.screenshot(path='/mnt/data/ilmora-bento-dashboard.png')
  page.locator('.side [data-go="lessons"]').click();page.wait_for_selector('.lesson-card');expect(page.locator('.lesson-card')).to_have_count(40)
  page.locator('[data-act="lesson"]').first.click();page.get_by_role('button',name='Darsni tugatish').click();page.get_by_text('✓ Tugallangan',exact=True).wait_for();page.get_by_role('button',name='25 ta mashqni ishlash').click();page.locator('[data-act="practice-answer"]').first.click();page.locator('[data-act="practice-next"]').click();assert page.get_by_text('Savol 2/25',exact=True).count()==1
  page.locator('.side [data-go="writing"]').click();page.wait_for_selector('#doc-body');page.locator('#doc-title').fill('Sinov hujjati');page.locator('#doc-body').fill('Akademik yozuv muhim.\n\nDalillar bilan asoslaymiz.');page.locator('[data-act="doc-save"]').click();page.get_by_text('Sinov hujjati',exact=True).wait_for();
  content=page.evaluate("async()=>Array.from(new Uint8Array(await docxBlob('Sinov hujjati', 'Akademik yozuv.').arrayBuffer()))")
  Path('/tmp/ilmora-academic-test.docx').write_bytes(bytes(content))
  with zipfile.ZipFile('/tmp/ilmora-academic-test.docx') as z: assert 'word/document.xml' in z.namelist() and z.testzip() is None and 'Sinov hujjati' in z.read('word/document.xml').decode()
  page.locator('.side [data-go="studio"]').click();page.wait_for_selector('[data-form="bank-add"]');page.locator('[data-form="bank-add"] button').click();page.locator('[data-form="quiz-save"] [name="title"]').fill('Sinov test');page.locator('[data-form="quiz-save"] [value="save"]').click();page.get_by_text('Sinov test',exact=True).wait_for()
  page.locator('.side [data-go="ai"]').click();page.wait_for_selector('[data-form="ai"]');page.locator('[name="prompt"]').fill('Ilmiy uslub nima?');page.locator('[name="consent"]').check();page.locator('[data-form="ai"] button').click();page.get_by_text('Mahalliy o‘quv materiali (AI emas):',exact=False).wait_for();
  page.locator('.side [data-go="citation"]').click();page.wait_for_selector('[data-form="citation"]');page.locator('[name="author"]').fill('Karimov, A.');page.locator('[name="title"]').fill('Akademik yozuv');page.locator('[name="year"]').fill('2024');page.locator('[name="publisher"]').fill('Nashr');page.locator('[data-form="citation"] button').click();assert 'Karimov' in page.locator('#citation-output').inner_text()
  # New lesson mode, per-lesson cards, labs, progress map, exams, mistake log.
  page.locator('.side [data-go="lessons"]').click();page.locator('[data-act="lesson"]').first.click();page.get_by_role('button',name='Qisqa konspekt').click();expect(page.locator('.note-list li')).to_have_count(5);page.get_by_role('button',name='Fokus rejimi').click();expect(page.locator('body.focus-mode')).to_have_count(1);page.get_by_role('button',name='Fokusdan chiqish').click();page.get_by_role('button',name='Kartochkalarni ochish').click();page.get_by_role('button',name='Ta’rifni ochish').click();assert 'Kishilar' in page.locator('.page h1').inner_text()
  page.locator('.side [data-go="labs"]').click();page.wait_for_selector('#lab-text');page.locator('#lab-text').fill('xayot va muommo');page.get_by_role('button',name='Tekshirish').click();assert 'hayot' in page.locator('#lab-result').inner_text();page.get_by_role('button',name='Uslub detektori').click();page.locator('#lab-text').fill('Tadqiqot natijasi aniqlandi');page.get_by_role('button',name='Tekshirish').click();assert 'Ilmiy' in page.locator('#lab-result').inner_text();page.get_by_role('button',name='Matn konstruktori').click();page.locator('[data-piece="1"]').click();page.locator('[data-piece="2"]').click();page.locator('[data-piece="0"]').click();expect(page.locator('#lab-result')).to_contain_text('To‘g‘ri tartib');page.get_by_role('button',name='Aqlli konspekt').click();page.locator('#lab-text').fill('Konspekt sinovi');page.get_by_role('button',name='Konspektni saqlash').click();page.get_by_role('button',name='Imlo laboratoriyasi').click();page.get_by_role('button',name='Aqlli konspekt').click();expect(page.locator('#lab-text')).to_have_value('Konspekt sinovi');page.get_by_role('button',name='Nutq treneri').click();page.get_by_role('button',name='Vaqtni boshlash').click();page.wait_for_timeout(1100);expect(page.locator('#speech-clock')).to_have_text('00:39')
  page.locator('.side [data-go="map"]').click();expect(page.locator('.module-card')).to_have_count(7);page.locator('.side [data-go="practice"]').click();page.wait_for_selector('[data-act="practice-reset"]');page.locator('[data-act="practice-reset"]').click() if page.locator('[data-act="practice-reset"]').count() else None;page.get_by_role('button',name='Oraliq nazorat · 20 savol').click();page.wait_for_selector('[data-act="practice-answer"]');assert page.evaluate('practice.qs.length')==20;assert page.evaluate('practice.qs.every(q=>lessons.find(l=>l.id===q.lesson).module<=3)');wrong=page.evaluate('practice.qs[0].options.findIndex((_,i)=>!practice.qs[0].answer.includes(i))');page.locator(f'[data-act="practice-answer"][data-id="{wrong}"]').click();expect(page.locator('.page')).to_contain_text('To‘g‘ri javob:');page.locator('.side [data-go="mistakes"]').click();expect(page.locator('[data-act="retry-mistakes"]')).to_be_enabled();page.get_by_role('button',name='Xatolarni takrorlash').click();page.wait_for_selector('[data-act="practice-answer"]');assert page.evaluate('practice.qs.length')>=1
  page.locator('.side [data-go="home"]').click();page.locator('[data-act="theme"]').click();assert page.locator('body.dark').count()==1;page.wait_for_timeout(1100);page.evaluate("document.querySelector('#toast').classList.remove('show')");page.screenshot(path='/mnt/data/ilmora-bento-dark.png')
  mobile=browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);load(mobile);mobile.get_by_role('button',name='Mahalliy demoni ko‘rish').click();mobile.wait_for_selector('.hero');mobile.wait_for_timeout(1100);mobile.screenshot(path='/mnt/data/ilmora-bento-mobile.png');assert mobile.evaluate('document.documentElement.scrollWidth <= innerWidth')
  assert not errors,errors
  print('PASS: landing/demo, dashboard, 40 lessons, completion + XP, practice, document save + valid DOCX ZIP, quiz creation, local AI fallback, citation, dark mode, mobile layout, lesson summaries + focus, labs, progress map, exam and mistake log. No JS page errors.')
  browser.close()

