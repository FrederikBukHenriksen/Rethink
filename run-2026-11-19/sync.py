import json, sys
q=json.load(open('queue.json'))
doc={"category":"alle","date":"2026-11-19T21:35:00+01:00","status":"kører","heartbeat":q['heartbeat'],
 "trigger":"planlagt søgekørsel (bruger-anmodning 19. nov. 21:34)","platforms":q['platformOrder'],"platformOrder":q['platformOrder'],
 "searched":q['searched'],"progress":q['progress'],"units":q['units'],
 "sections":[{"title":"Status","items":[l for l in sys.argv[1:]]}]}
json.dump(doc,open('run-doc.json','w'),ensure_ascii=False)
print(sum(1 for x in q['units'].values() if x['status']=='færdig'),'færdig;',sum(1 for x in q['units'].values() if x['status']=='kører'),'kører;',sum(1 for x in q['units'].values() if x['status']=='åben'),'åben')
