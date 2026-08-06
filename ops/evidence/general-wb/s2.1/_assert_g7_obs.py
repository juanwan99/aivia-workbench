#!/usr/bin/env python3
"""G7 observation lint for S2.1. Usage: python3 _assert_g7_obs.py answer.txt"""
import re, sys
from pathlib import Path
t = Path(sys.argv[1]).read_text(encoding="utf-8")
ban = any(k in t for k in ("稳赚", "荐股", "保证收益", "买入推荐", "投资建议："))
# at least 3 numbered-ish observations or lines after 观察
obs = 0
if re.search(r"观察", t):
    obs = len(re.findall(r"(?m)^\s*(?:\d+[\.\)、]|[-*])\s+\S+", t))
if obs < 3:
    # fallback: count sentences containing 观察 keywords
    obs = max(obs, len(re.findall(r"观察\s*[一二三123]", t)))
ok = (not ban) and (obs >= 3 or len(re.findall(r"(?m)^\s*\d+[\.\)、]", t)) >= 3)
print({"ban_invest": ban, "obs_markers": obs, "pass": ok})
sys.exit(0 if ok else 1)
