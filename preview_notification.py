"""Manual installation check with actual current counters; does not change hourly schedule."""
import json
from pathlib import Path
from urllib.request import urlopen

base=Path(__file__).resolve().parent
config=json.loads((base/'config.json').read_text(encoding='utf-8'))
with urlopen(f"http://127.0.0.1:{config['port']}/api/status",timeout=5) as response:
    state=json.load(response)
body={'preview':True,'before':{'processed':0,'chunks':0},
      'after':{'processed':state['processed'],'chunks':state['chunks']},
      'delta':{'processed':state['processed'],'errors':state['errors_total']},
      'pending':state['counts'].get('pending',0),'progress':state['progress'],
      'active_seconds':state['active_seconds'],'phase':'Проверка окна; реальные текущие показатели'}
(base/'data/notification-preview.json').write_text(json.dumps(body,ensure_ascii=False),encoding='utf-8')
