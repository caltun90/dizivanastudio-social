"""Bolumun iki formatini uretir. Bolum klasorunun icinden:  python ../../../motor/uret.py <cikti_on_eki> [v|h]
  -> <cikti_on_eki>-dikey.mp4 ve <cikti_on_eki>-yatay.mp4   (sahneler paralel islenir)"""
import os, subprocess, sys
name = sys.argv[1]; fmts = sys.argv[2:] or ['v', 'h']
jobs = max(1, (os.cpu_count() or 2) // len(fmts))
ps = [subprocess.Popen([sys.executable, 'bolum.py', 'all', f"{name}-{'dikey' if f == 'v' else 'yatay'}.mp4"],
                       env=dict(os.environ, FMT=f, JOBS=str(jobs), PYTHONIOENCODING='utf-8')) for f in fmts]
sys.exit(max(p.wait() for p in ps))
