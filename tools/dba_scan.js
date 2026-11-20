// DBA scanner. Paste into javascript_tool on a dba.dk tab (own tab, user's Chrome).
// Reads every result page via same-origin fetch, returns only a compact summary.
window.dbaMon={jan:0,feb:1,mar:2,apr:3,maj:4,jun:5,juni:5,jul:6,juli:6,aug:7,sep:8,sept:8,okt:9,nov:10,dec:11};
window.dbaDate=function(s,now){ // returns {end:Date(end of day), raw}
  s=(s||'').trim().toLowerCase(); let m;
  if((m=s.match(/^(\d+)\s*(min|t)\b/))) return new Date(now-(m[2]==='t'?m[1]*3600e3:m[1]*60e3));
  if((m=s.match(/^(\d+)\s*dag/))) {const d=new Date(now);d.setDate(d.getDate()-(+m[1]));d.setHours(23,59,59);return d;}
  if(/^i går/.test(s)){const d=new Date(now);d.setDate(d.getDate()-1);d.setHours(23,59,59);return d;}
  if(/^i dag/.test(s)) return new Date(now);
  if((m=s.match(/^(\d{1,2})\.\s*([a-zæø]+)\.?(?:\s*(\d{2,4}))?$/))&&dbaMon[m[2]]!==undefined){let y=m[3]?(+m[3]<100?2000+ +m[3]:+m[3]):now.getFullYear();let d=new Date(y,dbaMon[m[2]],+m[1],23,59,59);if(!m[3]&&d>now)d=new Date(y-1,dbaMon[m[2]],+m[1],23,59,59);return d;}
  if((m=s.match(/^(\d{1,2})\.(\d{1,2})\.(\d{2,4})$/))){let y=+m[3]<100?2000+ +m[3]:+m[3];return new Date(y,+m[2]-1,+m[1],23,59,59);}
  return null;
};
window.dbaScan=async function(q,opt={}){
  const {cutoff,maxPrice,maxPages=60}=opt; const now=new Date(); const cut=cutoff?new Date(cutoff):null;
  const rows=new Map(); let total=null,ended=false,log=[],last=0;
  for(let p=1;p<=maxPages;p++){
    const url=location.origin+'/recommerce/forsale/search?q='+encodeURIComponent(q)+'&sort=PUBLISHED_DESC'+(p>1?'&page='+p:'');
    let h; try{const r=await fetch(url,{credentials:'include'}); if(!r.ok){log.push('p'+p+' HTTP '+r.status);break;} h=await r.text();}catch(e){log.push('p'+p+' '+e.message);break;}
    const d=new DOMParser().parseFromString(h,'text/html');
    if(total===null){const e=[...d.querySelectorAll('*')].find(e=>e.children.length===0&&/^[\d.]+\s*resultater?$/.test(e.textContent.trim()));total=e?+e.textContent.replace(/\D/g,''):null;}
    const cards=[...d.querySelectorAll('article')].filter(a=>a.querySelector('a[href*="/recommerce/forsale/item/"]'));
    if(!cards.length){ended=true;last=p-1;break;}
    let add=0;
    for(const c of cards){const id=(c.querySelector('a[href*="/recommerce/forsale/item/"]').getAttribute('href').match(/item\/(\d+)/)||[])[1]; if(!id||rows.has(id))continue;
      const sp=[...c.querySelectorAll('span')].map(x=>x.textContent.trim()).filter(Boolean);
      const price=sp.find(x=>/kr\.?$/.test(x)); const title=(c.querySelector('h2')||{}).textContent||'';
      const spans=sp.filter(x=>x!==price&&!/favorit|annoncen|Fiks|Betalt/i.test(x));
      const isDate=x=>/^(\d+\s*(min|t\.?|dag(e)?)\b|i går|i dag|\d{1,2}\.\s*[a-zæø]+\.?(\s*\d{2,4})?$|\d{1,2}\.\d{1,2}\.\d{2,4}$)/i.test(x);
      const di=spans.findIndex(isDate); const dateTxt=di>=0?spans[di]:''; const city=di>0?spans[di-1]:(spans[0]||''); const seller=spans.slice(di>=0?di+1:1).join(' / ');
      rows.set(id,{id,title:title.replace(/\s+/g,' ').trim(),price:price?+price.replace(/\D/g,''):null,city,dateTxt,seller,fiks:/Fiks færdig/.test(c.textContent)}); add++;}
    log.push(p); if(!add){log.push('repeat');last=p;break;} last=p;
  }
  const all=[...rows.values()]; let older=0,unk=0; const cand=[];
  for(const r of all){const d=dbaDate(r.dateTxt,now); if(!d)unk++; if(d&&cut&&d<cut){older++;continue;} if(maxPrice&&r.price!=null&&r.price>maxPrice)continue; cand.push(r);}
  return {q,total,read:all.length,pages:last,ended,older,unparsedDate:unk,candN:cand.length,cand};
};
window.dbaRun=async function(terms,opt){const out=[];for(const t of terms){const r=await dbaScan(t,opt);out.push(r);}return out;};
window.dbaFmt=function(res,lim=30){return res.map(r=>`## ${r.q}: læst ${r.read} af ${r.total}, sider ${r.pages}, slut nået ${r.ended?'ja':'NEJ'}, før cutoff ${r.older}, dato ikke tolket ${r.unparsedDate}, efter cutoff/prisfilter ${r.candN}\n`+r.cand.slice(0,lim).map(c=>`${c.id}|${c.price??'?'}|${c.title.slice(0,70)}|${c.city}|${c.dateTxt}${c.fiks?'|Fiks':''}`).join('\n')).join('\n');};
'ok'
