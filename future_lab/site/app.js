let PASSPORTS=[];

function values(){
  const xs=document.getElementById('series').value.split(',').map(x=>Number(x.trim()));
  if(!xs.length||xs.some(x=>!Number.isFinite(x)))throw new Error('Введите корректный числовой ряд');
  return xs;
}
function calc(xs,m){
  if(m==='naive')return xs.at(-1);
  if(m==='mean')return xs.reduce((a,b)=>a+b,0)/xs.length;
  if(m==='drift'){
    if(xs.length<2)throw new Error('Drift требует минимум два наблюдения');
    return xs.at(-1)+(xs.at(-1)-xs[0])/(xs.length-1);
  }
  if(m==='ses'){
    let l=xs[0];
    for(let i=1;i<xs.length;i++)l=.5*xs[i]+.5*l;
    return l;
  }
  throw new Error('Неизвестный метод');
}
function run(){
  const box=document.getElementById('result');
  try{
    const xs=values(),m=document.getElementById('method').value,y=calc(xs,m);
    box.textContent='Метод: '+m+'\nНаблюдений: '+xs.length+'\nПрогноз следующего значения: '+y.toFixed(4)+'\n\nВажно: это расчёт метода, а не доказательство его пригодности. Выбор метода должен подтверждаться предпосылками и backtesting.';
  }catch(e){box.textContent='Ошибка: '+e.message}
}
function esc(s){return String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function list(xs){return '<ul>'+(xs||[]).map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>'}
function badgeClass(e){return e==='NON_SCIENTIFIC'?'culture':(e==='SCIENTIFIC_A'||e==='SCIENTIFIC_B'?'science':'planned')}
function fillFilters(){
  const fam=[...new Set(PASSPORTS.map(x=>x.family))].sort();
  const sts=[...new Set(PASSPORTS.map(x=>x.status))].sort();
  const fs=document.getElementById('familyFilter'), ss=document.getElementById('statusFilter');
  fam.forEach(x=>fs.insertAdjacentHTML('beforeend','<option value="'+esc(x)+'">'+esc(x)+'</option>'));
  sts.forEach(x=>ss.insertAdjacentHTML('beforeend','<option value="'+esc(x)+'">'+esc(x)+'</option>'));
}
function renderStats(){
  const box=document.getElementById('passportStats');
  if(!box)return;
  const runnable=PASSPORTS.filter(x=>x.status==='RUNNABLE').length;
  const discovered=PASSPORTS.filter(x=>x.status==='DISCOVERED').length;
  const designed=PASSPORTS.filter(x=>x.status==='DESIGNED').length;
  const nonSci=PASSPORTS.filter(x=>x.evidence_class==='NON_SCIENTIFIC').length;
  const families=new Set(PASSPORTS.map(x=>x.family)).size;
  box.innerHTML=
    '<div class="stat"><b>'+PASSPORTS.length+'</b>паспортов</div>'+
    '<div class="stat"><b>'+families+'</b>направлений</div>'+
    '<div class="stat"><b>'+runnable+'</b>RUNNABLE</div>'+
    '<div class="stat"><b>'+discovered+'</b>DISCOVERED</div>'+
    '<div class="stat"><b>'+designed+'</b>DESIGNED</div>'+
    '<div class="stat"><b>'+nonSci+'</b>NON_SCIENTIFIC</div>';
}
function passportCard(p){
  return '<article class="passport-card">'+
   '<div class="passport-meta"><span class="badge '+badgeClass(p.evidence_class)+'">'+esc(p.evidence_class)+'</span><span class="badge planned">'+esc(p.status)+'</span><span class="badge">'+esc(p.family)+'</span></div>'+
   '<h3>'+esc(p.name)+'</h3><small>'+esc(p.id)+'</small>'+
   '<p><span class="passport-k">Что даёт:</span> '+esc((p.purpose?.predicts||[]).join(', '))+'</p>'+
   '<p><span class="passport-k">Алгоритм:</span> '+esc(p.algorithm)+'</p>'+
   '<details><summary>Паспорт метода</summary>'+
   '<p class="passport-k">Входные данные</p>'+list(p.inputs)+
   '<p class="passport-k">Применение</p>'+list(p.applications)+
   '<p class="passport-k">Предпосылки</p>'+list(p.assumptions)+
   '<p class="passport-k">Ограничения</p>'+list(p.limitations)+
   '<p class="passport-k">Когда не применять</p>'+list(p.unsuitable_when)+
   '<p class="passport-k">Проверка / метрики</p>'+list(p.verification?.metrics)+
   '<p><span class="passport-k">Код:</span> '+esc(p.verification?.code||'ещё не реализован')+'</p>'+
   '<p><span class="passport-k">Unit tests:</span> '+(p.verification?.unit_tests?'есть':'ещё нет')+'</p>'+
   '<p><span class="passport-k">Источники:</span> '+esc((p.sources||[]).join(', ')||'нужно дополнить')+'</p>'+
   '<div class="passport-conclusion"><b>Практический вывод:</b> '+esc(p.conclusion)+'</div>'+
   '</details></article>';
}
function renderCatalog(){
  const box=document.getElementById('passportCatalog'); if(!box)return;
  const q=(document.getElementById('methodSearch')?.value||'').toLowerCase().trim();
  const fam=document.getElementById('familyFilter')?.value||'';
  const st=document.getElementById('statusFilter')?.value||'';
  const rows=PASSPORTS.filter(p=>{
    const hay=JSON.stringify(p).toLowerCase();
    return (!q||hay.includes(q))&&(!fam||p.family===fam)&&(!st||p.status===st);
  });
  box.innerHTML=rows.length?rows.map(passportCard).join(''):'<div class="card">По выбранным фильтрам методы не найдены.</div>';
}
async function loadPassports(){
  try{
    const r=await fetch('method-passports.v1.json',{cache:'no-store'});
    const data=await r.json();
    PASSPORTS=data.passports||[];
    fillFilters(); renderStats(); renderCatalog();
  }catch(e){
    const box=document.getElementById('passportCatalog');
    if(box)box.innerHTML='<div class="card">Не удалось загрузить каталог паспортов: '+esc(e.message)+'</div>';
  }
}
document.addEventListener('DOMContentLoaded',loadPassports);
