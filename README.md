# ILMORA 1.0 — Bento Edition (Alpha 3)

Akademik yozuvni o‘rganish, o‘qituvchilar uchun guruh va topshiriqlar, real vaqt o‘yinlari va AI yordamchisi. Bepul tariflarda ishlashga mo‘ljallangan. Bu **ishlab chiqishning birinchi ishlaydigan poydevori**; to‘liq 1.0 production relizi emas. Supabase SQL va Gemini integratsiyasi kodlangan, lekin haqiqiy tashqi akkauntlarda ishga tushirilmagan va yuklama sinovi bajarilmagan.

## 1. Birinchi ko‘rish (hech qanday akkaunt kerak emas)

1. ZIP arxivini oching.
2. `ILMORA-demo.html` faylini Chrome yoki Edge’da oching (arxivdan chiqarib, alohida fayl sifatida).
3. “Mahalliy demoni ko‘rish” tugmasini bosing. Demo brauzer xotirasida ishlaydi; login, multiplayer va Gemini haqiqiy emas. Demo ma’lumotlari haqiqiy akkauntga o‘tmaydi.
4. Yoki Windows’da `start.bat` faylini ishga tushiring (Python o‘rnatilgan bo‘lishi kerak); `http://localhost:8080` ni oching. `public` papkada `python -m http.server 8080` buyrug‘i ham ishlaydi.

## 2. Loyiha tarkibi

- `public/index.html`, `app.js`, `style.css`: responsiv asosiy interfeys. React o‘rniga modulga ajratilgan sof JavaScript ishlatilgan, chunki bu versiya npm paketlarisiz ham ishlaydi. `content.js` — 40 dars, 200 tushuncha, ularga asoslangan 1000 alohida test mashqi (5 turdagi savol variatsiyasi). 20 dars yuklangan 6 ma’ruza asosida, 20 dars qo‘shimcha material; o‘qituvchi ko‘rib chiqishi kerak.
- `public/config.js`: faqat Supabase public URL va publishable/anon kalit.
- `public/sw.js`, `manifest.webmanifest`, ikonalar: PWA, ilova qobig‘ini oflayn saqlash.
- `supabase/schema.sql`: jadval, RLS, auth trigger, o‘yin RPC, o‘qituvchi arizalari, baholash, AI kvota mexanizmi.
- `supabase/features.sql`: dars nashri va xavfsiz hujjat ulashish.
- `netlify/functions/ai.mjs`: autentifikatsiya, AI roziligi, kvota, Gemini ulanishi.
- `tests/`: kontent va oflayn brauzer testlari; `QA.md` — haqiqiy integratsiya testlari.
- `netlify.toml`: deploy sozlamalari. Build talab qilinmaydi.

## 3. Supabase (bepul)

1. https://supabase.com/dashboard saytida Free plan tanlang va yangi loyiha yarating. Parolni o‘zingiz saqlang.
2. SQL Editor → New query. `supabase/schema.sql` faylining hammasini nusxalab Run bosing. Faqat yangi loyiha uchun bir marta. Xato bo‘lsa, xabarni saqlang, aynan shu faylni qayta-qayta ishlatmang.
3. Keyingi yangi query’da `supabase/features.sql` ni to‘liq Run qiling.
4. Project Settings → API Keys (yoki Connect) orqali Project URL va **publishable/anon** kalitni oling. `public/config.js` da qiymatlarni yozing. Namuna:

```js
window.ILMORA_CONFIG={
  supabaseUrl:'https://YOUR_PROJECT.supabase.co',
  supabaseKey:'YOUR_PUBLISHABLE_OR_ANON_KEY'
};
```

**Service role yoki secret kalitni public/config.js ga yozish qat’iyan mumkin emas.** SDK CDN orqali yuklanadi, shuning uchun haqiqiy xizmat uchun internet kerak. Supabase Data API `public` sxemasini expose qilishi kerak. `ilmora_private` sxemasini expose qilmang.

5. Authentication → Providers → Email yoqilganini tekshiring. Email tasdiqlash va reset uchun Authentication → SMTP Settings orqali alohida bepul SMTP provayderini sozlang. Supabase standart email xizmati cheklangan; custom SMTP uchun provayderning yuboruvchi manzil/domen talabi bo‘lishi mumkin. O‘z domeningiz bo‘lmasa, avval Google login yoki faqat sinov akkauntlari bilan tekshiring. Haqiqiy institut foydalanuvchilariga chiqishdan oldin email yetkazilishini tekshiring. CAPTCHA va auth rate limitlarni yoqishni ko‘rib chiqing.
6. Realtime publication’da `public.live_signals` borligini tekshiring. SQL migratsiyasi uni qo‘shadi. O‘yin xavfsiz RPC orqali ishlaydi; realtime signalga qo‘shimcha polling ham mavjud.

## 4. GitHub → Netlify (bepul)

1. GitHub’da yangi repository oching, masalan `ilmora`. Private yoki public tanlash mumkin. ZIP ichidagi `ilmora` papkasining mazmunini repository ildiziga yuklang: `public/`, `netlify/`, `supabase/`, `netlify.toml`, `package.json`, `README.md`. Demo HTML ni yuklash shart emas. Barcha maxfiy kalitlarni repozitoriydan tashqarida saqlang.
2. https://app.netlify.com → Add new project → Import an existing project → GitHub → repozitoriy tanlang.
3. Free tarif. Base directory bo‘sh (repo ildizi), Build command bo‘sh, Publish directory `public`, Functions directory `netlify/functions`. `netlify.toml` shu sozlamalarni beradi. Deploy qiling.
4. Project configuration → Site name: `ilmora` band bo‘lmasa, `ilmora.netlify.app`; band bo‘lsa boshqa nom tanlang. Haqiqiy manzilni Netlify beradi. Domen sotib olish shart emas.
5. Supabase Authentication → URL Configuration: Site URL = aniq Netlify URL, masalan `https://YOUR_SITE.netlify.app`. Redirect URLs ro‘yxatiga `https://YOUR_SITE.netlify.app/` va agar mahalliy test kerak bo‘lsa `http://localhost:8080/` ni qo‘shing.
6. Faqat `public` ni Netlify Drop orqali joylash statik demo uchun yetadi, lekin AI server function deploy bo‘lmaydi. AI uchun GitHub importini ishlating.

## 5. Google login (bepul)

1. https://console.cloud.google.com → yangi Google Cloud project. Google Auth Platform / OAuth consent screen: nomi ILMORA. Sinov rejimida kerakli test foydalanuvchilarini qo‘shing; umumiy foydalanishdan oldin Google'ning publishing talablarini tekshiring.
2. OAuth Client → Web application. Supabase Authentication → Providers → Google sahifasidagi callback URL ni nusxalang: odatda `https://YOUR_PROJECT.supabase.co/auth/v1/callback`.
3. Google’dagi Authorized redirect URIs ga aynan shu callback URL ni kiriting. Authorized JavaScript origins ga Netlify URL ni kiriting.
4. Google Client ID va Secret ni **Supabase Authentication → Providers → Google** sahifasiga kiriting. Frontendga yozmang.
5. Netlify’da Google orqali kirishni sinang. Foydalanuvchi profili trigger orqali yaratiladi.

## 6. O‘zingizni admin qilish

Avval sayt orqali haqiqiy email bilan akkaunt yarating va emailni tasdiqlang yoki Google orqali kiring. Keyin Supabase SQL Editor’da (buni faqat loyiha egasi bajaradi):

```sql
update public.profiles
set role = 'admin'
where id = (select id from auth.users where email = 'YOUR_ACTUAL_EMAIL');
```

Saytdan chiqib qayta kiring. Admin paneli chiqadi. O‘qituvchi Profil → Ariza yuborish qiladi. Admin tasdiqlagandan keyin o‘qituvchi qayta kirishi kerak. Oddiy foydalanuvchi role ustunini o‘zgartira olmaydi.

## 7. Gemini AI ulash ($0, limitli)

1. https://aistudio.google.com saytida bepul API kalit yarating. **Billing yoqmang va paid tier tanlamang.** AI Studio’da ayni vaqtda bepul API uchun ruxsat berilgan modelni hamda haqiqiy kunlik/daqiqalik kvotalarni tekshiring. Model ID o‘zgarishi mumkin; shuning uchun kodga qat’iy model nomi kiritilmagan.
2. Netlify → Project configuration → Environment variables → Add a variable. Quyidagilarni server function uchun qo‘shing:

| Nom | Qiymat |
|---|---|
| `SUPABASE_URL` | Project URL |
| `SUPABASE_PUBLIC_KEY` | publishable/anon kalit |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase legacy service_role JWT (faqat serverda; yangi secret format bu implementatsiyada tekshirilmagan) |
| `GEMINI_API_KEY` | Google AI Studio kaliti |
| `GEMINI_MODEL` | AI Studio ko‘rsatgan bepul model ID, `models/` prefiksisiz |
| `AI_DAILY_LIMIT` | real bepul limitdan PAST butun son; masalan 10, lekin provayder kvotasi ruxsat bersa |

3. Deployni qaytadan ishga tushiring. AI sahifasida akademik yozuv bo‘yicha savol va rozilik belgilang. Test: “Ilmiy uslubga oid 3 savol yarat”.
4. Limit 60% o‘qituvchi, 30% talaba, 10% admin kvotasi asosida hisoblanadi (kichik limitda yaxlitlash bor); bir talaba kuniga 3, o‘qituvchi/admin 12 so‘rovgacha. Ustuvorlik kvotani bron qilish orqali; navbat tizimi emas. Gemini limitiga erishilganda mahalliy matn tahlili va dars ta’riflari ishlaydi. Xatoli so‘rov ham kvotadan joy olishi mumkin. Limitni o‘zgartirish Netlify env orqali.
5. Gemini free tier yuborilgan kontentdan mahsulotlarini takomillashtirishda foydalanishi mumkin. AI’ga shaxsiy yoki maxfiy ma’lumot yubormang. PDF yuklash 2 MB bilan cheklangan. AI javobi ilmiy manbani tekshiruvchi yoki rasmiy baholovchi emas. AI Test JSON qaytarsa Test studiyasiga import qilish mumkin; barcha javoblarni o‘qituvchi tekshiradi. AI Dars natijasini o‘qituvchi qo‘lda dars muharririga joylaydi va nashr qiladi.
6. Topshiriq kontekstini tanlasangiz, server topshiriqning AI siyosatini tekshiradi (off / guide / full). Bu umumiy AI chatidan foydalanishni butunlay to‘sadigan imtihon proktoringi emas. Yozma topshiriqni faqat o‘qituvchi baholaydi.

## 8. Jonli o‘yin sinovi

1. Netlify saytida akkauntga kiring → Test yaratish → mavzu va savollar sonini tanlang → test nomi → Jonli o‘yin ochish. Xona 6 xonali PIN beradi.
2. Ikkinchi qurilmada yoki boshqa brauzer profilida shu saytni oching → PIN orqali kirish → ism → O‘yinga kirish. Unga akkaunt kerak emas.
3. Host ekranda o‘yinni boshlaydi; talabada savol yoki variantlar chiqadi. Server deadline va indeksni tekshiradi, javobni bir marta qabul qiladi. To‘g‘ri javob 500–1000 ball; imtihonda 1000 ball. Host javobni ochadi yoki vaqt tugaydi. Avtomatik rejimda 7 soniyadan keyin navbatdagi savol ochiladi (faol mijozlar polling/Realtime orqali holatni yangilaydi).
4. Xonada 50 ishtirokchi limiti, 4 soat ichida yangi qo‘shilish, kech kirishni boshqarish, lobbida chiqarish, mehmon tokeni bilan qayta ulanish mavjud. PIN/havola orqali kirish. Xona tugaganda CSV hisobot, o‘yin tarixi. Server javob kalitini faol savolda qaytarmaydi; ommaviy o‘quv testlari javoblarini o‘quvchi oldindan bilishi mumkin (rasmiy yuqori xavfli imtihon uchun bu anti-cheat emas).
5. Dastlab ikki qurilma, keyin 5, 10, 30 va 50 ta qurilma bilan sinang. SQL va Realtime ishlashini haqiqiy Supabase'da tekshirmasdan institutga keng tarqatmang.

## 9. 0 dollar rejim va cheklovlar

- Netlify Free: 300 oylik kreditli tarifda hard limit bor. Limit tugasa sayt keyingi davrgacha pauzaga tushishi mumkin. https://www.netlify.com/pricing/
- Supabase Free: 200 concurrent Realtime ulanish (2026-11-18 da tekshirildi); 50 ta o‘yinchiga yetishi mumkin, ammo bu yuklama sinovi o‘rnini bosmaydi. https://supabase.com/docs/guides/realtime/limits
- Gemini Free: faqat tanlangan modellar va kvotalar; cheksiz emas. https://ai.google.dev/gemini-api/docs/pricing
- Pullik tariflar, billing va auto recharge yoqilmaydi. Xizmatlarning mavjud free limitlari o‘zgarishi mumkin. Supabase/Netlify dashboardlarda foydalanishni muntazam kuzating. SQLdagi 50 limit faqat bir xona uchun.
- Guest PIN orqali odamlar ulanishida suiiste’molni oldini olish uchun ishlab chiqarishda CAPTCHA, IP/rate-limit gateway, eski xona va signal yozuvlarini tozalash, moderatsiya va maxfiylik siyosati talab etiladi. Hozirgi SQLda 50 kishilik limit, nom takrorlanmasligi, tasodifiy PIN/token va server tekshiruvi bor; to‘liq DDoS himoyasi emas.

## 10. Hozirgi holat va keyingi ishlar

| Funksiya | Holat |
|---|---|
| Bosh sahifa, dashboard, 40 dars, 1000 savol, mustaqil test, kartochka, XP | Oflayn DOM testidan o‘tgan |
| Matn muharriri, statistika, shablon, DOCX, PDF uchun browser print | Oflayn tahlil va DOCX arxivi tekshirilgan; PDF print real brauzerda qo‘shimcha tekshiriladi |
| Kirish, Google, password reset, admin/o‘qituvchi rollari | Kod va SQL bor; tashqi konfiguratsiya va integratsiya testi kerak |
| Jonli o‘yin klassik/imtihon, single/multiple/boolean, PIN, auto/manual, media URL, guest, reyting, CSV | Frontend va SQL bor; haqiqiy multiplayer yuklama sinovi kerak |
| AI 16 vosita, tarix, kvota, fallback, PDF, quiz import | Frontend/server kod bor; haqiqiy Gemini va RLS testi kerak; demo fallback tekshirilgan |
| Guruh, email/kod bilan qo‘shilish, topshiriq, o‘qituvchi bahosi, dars nashri, hujjat havolasi | SQL va UI bor; integratsiya testi kerak |
| Sertifikat | 40 dars tugagach browser print; QR verifikatsiya hali yo‘q |
| Kutubxona | 4 shablon va ochiq tashqi resurs havolalari; rasmiy dastur va video materiallar qo‘shilmagan |
| PWA | Manifest, service worker mavjud; haqiqiy HTTPS qurilmalarda install testi kerak |
| Qo‘shimcha o‘yin rejimlari (team, duel, survivor...), barcha 12 savol turi, 5 maxsus mini-o‘yin | Hali tayyor emas |
| QR, musiqa, konfetti, kengaytirilgan analytics, yutuqlar, push notifications, rich text, versiyalar tarixi, server-side media upload, batafsil admin boshqaruv | Hali tayyor emas; sayt ichidagi notification, oddiy matn muharriri va CSV mavjud |

6 ta taqdimotdan 20 ta kichik dars qayta ishlab chiqildi va avvalgi 20 dars saqlandi. 1000 savol 200 tushunchaning beshtadan mashq ko‘rinishlari, professor tomonidan tasdiqlanmagan. Rasmiy 1.0 relizdan oldin o‘qituvchi ko‘rib chiqadi va fan dasturiga moslanadi. Mahalliy test uchun `npm run check` (Node.js, paket o‘rnatish talab qilinmaydi). Oflayn DOM test `python tests/browser_test.py` (Playwright va Chromium o‘rnatilgan maxsus test muhitida); real server testi emas.


## Bento Edition yangilanishi
- Yangi o‘rnatishda `supabase/schema.sql` va `supabase/features.sql` ni ketma-ket ishlating. Eski ILMORA bazasi mavjud bo‘lsa, **faqat** `supabase/bento-upgrade.sql` ni ishlating; avvalgi ma’lumotlar va dars identifikatorlari saqlanadi.
- 6 ta ma’ruza (20 kichik dars), 20 qo‘shimcha dars, 200 kartochka, 1000 mashq varianti. Darslarda manba va sahifa oralig‘i bor; original PDF tarqatilmaydi. `netlify/functions/lecture-context.mjs` server tomonidagi qisqa qayta ishlangan mazmun; AI so‘rovi uchun eng yaqin 5 dars tanlanadi.
- Mahalliy imlo/ uslub vositalari cheklangan qoidaviy tahlil, AI emas. Konspekt va xatolar daftari qurilmada saqlanadi. Nutq treneri vaqt va reja bilan ishlaydi, audio baholamaydi.
- 3D CSS shakllar, animatsiyalar, mobil pastki menyu; reduced-motion sozlamasi hisobga olinadi.
- Klassik va imtihon jonli rejimlarining ko‘rinishi farqlanadi. Boshqa multiplayer rejimlari, push bildirishnomalari, QR-sertifikat va to‘liq boy matn muharriri hali yakunlanmagan. Real multiplayer, Auth va Gemini uchun sozlash hamda server sinovi zarur.
- Oraliq testlar: 1–3-ma’ruza, yakuniy: 1–6-ma’ruza. Bu o‘quv mashqlari, rasmiy imtihon savollari emas.
