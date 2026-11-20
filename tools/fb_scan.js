// Facebook Marketplace scanner (testet 2026-11-20). Kør i javascript_tool på fanen efter navigation til søgesiden.
// Navigér først til:
//   https://www.facebook.com/marketplace/copenhagen/search/?query=<søgeord>&radius=500&sortBy=creation_time_descend&exact=false
// Scriptet starter i baggrunden (45 s grænse pr. kald). Hent resultatet bagefter med: for(let i=0;i<40&&!window.__q;i++)await new Promise(r=>setTimeout(r,1000));window.__q||'pending'
// Læs ALDRIG document.body.innerText videre end 'No listings found'-tjekket: siden kan indeholde brugerens private Messenger-vindue.
window.__q=null;(async()=>{
 const L='SØGEORD', rx=/titelfilter/i, mp=2000;  // rx: streng titelregex for målet; mp: maksimumpris
 await new Promise(r=>setTimeout(r,3500));
 if(/checkpoint|login/.test(location.pathname)){window.__q='LOGIN/CHECKPOINT';return;}
 const seen=new Map();let st=0,n=0;
 const col=()=>document.querySelectorAll('a[href*="/marketplace/item/"]').forEach(a=>{const id=(a.getAttribute('href').match(/item\/(\d+)/)||[])[1];if(!id||seen.has(id))return;let p=a.innerText.split('\n').map(s=>s.trim()).filter(Boolean);if(/^DKK/.test(p[1]||''))p.splice(1,1);seen.set(id,{id,pr:+(p[0]||'').replace(/\D/g,''),t:p[1]||'',c:p[2]||''});});
 const none=document.body.innerText.includes('No listings found');
 for(;n<40;n++){const b=seen.size;col();window.scrollTo(0,document.body.scrollHeight);await new Promise(r=>setTimeout(r,1800));col();if(seen.size===b){if(++st>=3)break;}else st=0;}
 const h=[...seen.values()].filter(x=>rx.test(x.t)&&(!mp||!x.pr||x.pr<=mp));
 window.__q=L+': læst '+seen.size+', runder '+n+', ingen '+none+', match '+h.length+'\n'+h.slice(0,15).map(x=>x.id+'|'+x.pr+'|'+x.t.slice(0,45)+'|'+x.c).join('\n');
})();'started'
