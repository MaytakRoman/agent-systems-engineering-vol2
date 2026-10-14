"""Run the 42 Python listings and validate the four JSON documents."""
from pathlib import Path
import hashlib
import json
import os
import platform
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent

def main():
    logs=ROOT/'execution_logs';logs.mkdir(exist_ok=True)
    names=['framework.py']+[p.name for p in sorted(ROOT.glob('*.py')) if p.name not in ('framework.py','run_all.py')]
    report={'python':platform.python_version(),'platform':platform.platform(),'runs':[],'json_files':[]}
    for name in names:
        t=time.perf_counter()
        r=subprocess.run([sys.executable,str(ROOT/name)],cwd=ROOT,capture_output=True,text=True,
                         encoding='utf-8',env={**os.environ,'PYTHONIOENCODING':'utf-8'})
        (logs/(Path(name).stem+'.txt')).write_text(r.stdout+r.stderr,encoding='utf-8')
        report['runs'].append({'file':name,'returncode':r.returncode,'seconds':round(time.perf_counter()-t,4),'stdout':r.stdout,'stderr':r.stderr})
        print(name,r.returncode,flush=True)
    for p in sorted(ROOT.glob('*_schema.json')):
        obj=json.loads(p.read_text(encoding='utf-8'))
        report['json_files'].append({'file':p.name,'valid_json':True,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    report['passed']=sum(x['returncode']==0 for x in report['runs']);report['total']=len(names)
    (ROOT/'execution_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return int(report['passed']!=report['total'])

if __name__=='__main__':sys.exit(main())
