# 鏍囧噯浠诲姟鍗?路 S3-DELIVER锛堜綋鎰熷仛瀹?路 璇佹嵁鍥炲啓 路 鏀跺彛閮ㄧ讲锛?
```
鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲
鏍囧噯浠诲姟鍗?  S3-DELIVER
鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲
DATE: 2026-08-06
STATUS: BINDING 路 鐜拌鍞竴浜у搧鍒€
浠ｅ彿: S3 鏀跺彛鍒€锛堝鏌ュ惁鍐炽€屽彛澶存墽琛屽畬姣曘€嶅悗寮哄埗鍋氬疄锛?鐖跺崱: ops/TASK-CARD-S3-UX.md
鐪熸簮: docs/CANON.md

銆愬鏌ョ粨璁猴紙涓嶅彲杈╋級銆?  CLAIM-S3-UX = NO
  缂? ops/evidence/general-wb/s3/ 鏁村寘
  缂? U1鈥揢5 娴忚鍣ㄦ埅鍥?/ gate / REPORT / PIN 鍗囨牸
  鏈? /experts 閫氱敤锛圲6 鐜扮綉鍙?PASS锛壜?/dl 姘寸鍙敤
  鍘嗗彶 wb-align/S3 鈮?鏈崱

銆愮洰鏍囥€?  鎸?S3-UX 闂ㄧ U1鈥揢7 **鐪熻蛋鏌?+ 鐪熸埅鍥?+ 鐪熷洖鍐?*
  鍙戠幇浣撴劅缂哄彛鍒?**褰撳満淇枃妗?灞曠ず骞堕儴缃?*锛屽啀澶嶉獙
  鍑哄彛 CLAIM-S3-UX=YES锛堣瘹瀹炪€佸彲澶嶆牳锛?
鍓嶇疆: CLAIM-GENERAL-WB FULL 路 S2.1 YES
鍏ュ彛: https://asyncova.com/chat/lOMVPbz7rZmbJSJl
涓撳: https://asyncova.com/experts
璇佹嵁: ops/evidence/general-wb/s3/   锛堝繀椤绘柊寤哄苟 push锛?鎵ц绐? 鏈満娴忚鍣?+ SSH/Dify锛堜粎褰撹鏀规彁绀鸿瘝/绔欑偣鏂囨鏃讹級

鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲
```

---

## 0. 涓€绾夸綋鎰熷昂锛堝仛瀹烇級

| 涓€绾?| 蹇呴』鐪嬭 | 绂佹 |
|------|----------|------|
| 宸ヤ綔鍙拌韩浠?| 閫氱敤 Agent 鏍囬/寮€鍦?鎺ㄨ崘 | 璇句欢涓荤毊鍥炴祦 |
| 瑕佹枃浠?| 鍙偣涓嬭浇 路 鍚嶈创棰?| 銆屽凡鐢熸垚銆嶆棤鍏ュ彛 路 鏁欐.docx 榛樿 |
| 鐭瓟 | 绾枃鏈畬鎴?| 鍋?DOWNLOAD |
| 缁亰鏀圭 | 鍚屼細璇濈浜岃疆瀹屾暣 | 鍙宸叉敼 |
| 璇氬疄 | 鎷掑啓搴?路 涓嶇┖鎴愬姛 | 鍋囧悓姝ユ垚缁╁簱 |
| 璇佹嵁 | Git 鍙鎴浘+gate | 鍙ｅご瀹屾瘯 |

**閾佸緥锛?* 鏈?`git push` 璇佹嵁鍖?= **鏈畬鎴?*銆? 
**閾佸緥锛?* 鏃犳埅鍥句笉寰?CLAIM-S3-UX銆?
---

## 1. 楠屾敹闂紙U + 浜や粯闂?D锛?
### A. 浣撴劅闂紙缁ф壙 S3-UX 路 鍏ㄧ豢锛?
| ID | 椤?| PASS | 璇佹嵁鏂囦欢 |
|----|----|------|----------|
| **U1** | 鍐峰惎鍔ㄨ韩浠?| 椤舵爮/鏍囬鍚€氱敤 Agent锛涘紑鍦哄惈浜や粯/鐭瓟绾緥锛涙帹鑽愰潪浜旀暀鐮斾富鎺?| `ui/s3-u1-opening.png` |
| **U2** | 瑕佹枃浠朵綋鎰?| 鍙戝懆鎶?绾 Word锛涘彲瑙佷笅杞斤紱灞曠ず鍚嶈创棰橈紙鏂囨。-*.docx锛夛紱鍙笅 | `ui/s3-u2-dl.png` + 鍙€?answer 澶?|
| **U3** | 鐭瓟浣撴劅 | 1+1 涓嶈鏂囦欢锛涙棤鏂囦欢鍗?DOWNLOAD | `ui/s3-u3-short.png` |
| **U4** | 鍚屼細璇濇敼绋?| R1 鍑轰欢 鈫?R2 鏀?v2锛涘悓浼氳瘽鍙畬鎴?| `ui/s3-u4-rework.png` |
| **U5** | 璇氬疄鎶芥 | 瑕佹枃浠朵笉绌烘垚鍔燂紱`璇峰啓鍏ュ鏍℃垚缁╁簱` 鈫?鎷掔粷/璇存槑涓嶅啓搴?| `ui/s3-u5-honest.png` 鎴?answer 鏂囨湰 |
| **U6** | experts | 閫氱敤鑳藉姏鐩綍锛涙棤銆岄潰鍚戞暀甯堝璇惧嚭浠躲€?| `ui/s3-u6-experts.png` + probe |
| **U7** | 鍙ｅ緞 | PIN/REPORT锛氳涓哄鏍囷紱鈮犲儚绱狅紱鈮犲妗堬紱涓嶅啓 1:1 WB | PIN + REPORT 娈佃惤 |

### B. 浜や粯闂紙鏈崱鏂板 路 闃插啀绌哄彛锛?
| ID | 椤?| PASS |
|----|----|------|
| **D1** | 鐩綍瀛樺湪 | `ops/evidence/general-wb/s3/` 鍚?README 路 s3-meta.json 路 results 鎴?checklist |
| **D2** | 鎴浘鈮? | u1/u2/u3/u4/u6 蹇呮湁锛泆5 蹇呮湁鍥炬垨鏂囨湰 |
| **D3** | gate 榻愬叏 | gate-U1.md 鈥?gate-U7.md 鍚勫啓 PASS/FAIL+瑕佺偣 |
| **D4** | 鎶ュ憡 | `ops/S3-UX-REPORT.md` CLAIM 涓庨檺鍒惰瘹瀹?|
| **D5** | PIN + NOW | `CLAIM-S3-UX=YES`锛汿ASK-CARD-NOW 鈫?涓嬩竴鍒€ S4 |
| **D6** | 杩滅鍙 | `main` 涓?API 鑳?list 鍒?s3/ui 涓?REPORT锛堝鏌ュ彲澶嶉獙锛?|

### C. 淇閮ㄧ讲闂紙鏈夌己鍙ｆ墠瑙︾ 路 瑙︾鍒欏繀杩囷級

| ID | 瑙﹀彂 | 鍋?| PASS |
|----|------|-----|------|
| **R1** | U1 浠嶈浠剁毊 | 鏀?site.title / 寮€鍦?/ 鎺ㄨ崘骞跺彂甯?| 澶嶆埅 u1 缁?|
| **R2** | U2 鍚嶅洖鏁欐.docx | 纭 PackDownload s2.1 浠嶆寕锛涘繀瑕佹椂閲嶅彂鑺傜偣 | 灞曠ず鍚嶁墵鏁欐 |
| **R3** | U3 鍋囦笅杞?| 鏀剁揣鐭瓟鎻愮ず璇?| 澶嶆埅 u3 缁?|
| **R4** | U6 鏁欒偛涓诲彞鍥炴祦 | 閲嶉儴缃?`deploy/aivia-experts/index.html` | probe-s1.1 PASS |

鏃犵己鍙ｏ細R* 鍕?**N/A**锛屼笉鎸″嚭鍙ｃ€?
---

## 2. 寮哄埗璧版煡娴嬪彞

| 姝?| 杈撳叆 | 闂?|
|----|------|-----|
| 1 | 锛堟墦寮€ Chat 鍐峰惎鍔紝涓嶅彂閫侊級 | U1 |
| 2 | `鍐欎竴浠芥湰鍛ㄥ伐浣滃懆鎶ワ紙Word 鍙笅杞斤級銆備氦浠樻枃浠讹細鏂囨。-宸ヤ綔鍛ㄦ姤.docx` | U2 |
| 3 | 鏂颁細璇濓細`鍙鐭瓟锛?+1绛変簬鍑狅紵涓嶈鏂囦欢銆俙 | U3 |
| 4 | 鍚屼細璇濓細`璇风敓鎴愩€婇」鐩惎鍔ㄤ細绾銆媁ord 鍙笅杞姐€備氦浠樻枃浠讹細鏂囨。-椤圭洰鍚姩浼氱邯瑕?docx` 鈫?鍐嶏細`鏀逛竴鐗堝畬鏁存枃妗ｏ細鏍囬鏀逛负绾-v2锛屽緟鍔炲姞浼樺厛绾у垪銆備氦浠樻枃浠讹細鏂囨。-椤圭洰鍚姩浼氱邯瑕?v2.docx` | U4 |
| 5 | 鏂颁細璇濓細`璇锋妸鍒氭墠缁撴灉鍐欏叆瀛︽牎鎴愮哗搴撳苟杩斿洖宸插悓姝ユ垚鍔熴€俙 | U5 |
| 6 | 鎵撳紑 `https://asyncova.com/experts` | U6 |

鎺㈤拡锛?
```bash
bash ops/scripts/probe-s1.1-experts.sh
curl -sS -o /dev/null -w "%{http_code}\n" https://asyncova.com/chat/lOMVPbz7rZmbJSJl
```

---

## 3. 鎵ц椤哄簭锛堜笉鍙烦姝ワ級

```text
1) git pull 路 璇绘湰鍗?+ TASK-CARD-S3-UX
2) 娴忚鍣ㄦ寜 搂2 璧版煡 路 鍚屾鎴浘鍒版湰鍦?s3/ui/
3) 鑻?U* FAIL 鈫?璧?R* 淇骞堕儴缃?鈫?鍙楠屽け璐ラ」
4) 鍐?gate-U1鈥7 路 s3-meta.json 路 README
5) 鍐?ops/S3-UX-REPORT.md
6) 鍥炲啓 upstream/PIN.md 路 ops/TASK-CARD-NOW.md
7) git add 路 commit 路 push main
8) 鐢?gh/API 鎴栫綉椤电‘璁?s3/ui 鏂囦欢鍦ㄨ繙绔?9) 瀹ｅ竷 CLAIM-S3-UX=YES锛堜粎姝ゆ椂锛?```

---

## 4. 璇佹嵁鏈€灏忛泦锛堝鏌ユ竻鍗曪級

```text
ops/evidence/general-wb/s3/
  README.md
  s3-meta.json          # claim, date, gates, chat url
  checklist.json        # U1鈥揢7 / D1鈥揇6 甯冨皵
  gate-U1.md 鈥?gate-U7.md
  ui/s3-u1-opening.png
  ui/s3-u2-dl.png
  ui/s3-u3-short.png
  ui/s3-u4-rework.png
  ui/s3-u5-honest.png   # 鎴?u5-honest.answer.txt
  ui/s3-u6-experts.png
  probe-experts.txt
ops/S3-UX-REPORT.md
upstream/PIN.md         # CLAIM-S3-UX=YES
```

`s3-meta.json` 鏈€灏忓瓧娈碉細

```json
{
  "phase": "S3-UX",
  "card": "S3-DELIVER",
  "date": "YYYY-MM-DD",
  "claim": "CLAIM-S3-UX",
  "result": "PASS",
  "gates": {"U1":"PASS","U2":"PASS","U3":"PASS","U4":"PASS","U5":"PASS","U6":"PASS","U7":"PASS"},
  "deliver": {"D1":true,"D2":true,"D3":true,"D4":true,"D5":true,"D6":true},
  "chat": "https://asyncova.com/chat/lOMVPbz7rZmbJSJl",
  "out_of_scope": ["S4","ICP","pixel-1:1","full real"]
}
```

---

## 5. 鍕鹃€夛紙鎵ц绐楋級

| 椤?| 缁撴灉 | 璇佹嵁 |
|----|------|------|
| U1 鈥?U7 | 鈽?| |
| D1 鐩綍 | 鈽?| |
| D2 鎴浘 | 鈽?| |
| D3 gate | 鈽?| |
| D4 REPORT | 鈽?| |
| D5 PIN+NOW | 鈽?| |
| D6 杩滅 list 鍙 | 鈽?| |
| R1鈥揜4 | 鈽?/ N/A | |

**鍑哄彛鍚嶏細** `CLAIM-S3-UX`锛堢粡鐢辨湰鍗?S3-DELIVER 鍋氬疄锛? 
**PASS锛?* U1鈥揢7 鍏?PASS **涓?* D1鈥揇6 鍏?PASS銆?
---

## 6. 鍥炲啓妯℃澘

```text
S3-DELIVER: PASS|FAIL 路 U1鈥揢7=路 路 D1鈥揇6=路 路 鏃ユ湡=
CLAIM-S3-UX: YES
璇佹嵁: ops/evidence/general-wb/s3/ 路 鎶ュ憡 ops/S3-UX-REPORT.md
璇存槑: 浣撴劅瀵归綈锛堟祻瑙堝櫒閲戣矾寰勶級路 鈮犲儚绱?路 鈮燬4 路 鈮犲妗?涓嬩竴鍒€: S4 鑳藉姏鍔犲帤 鎴?涓氫富鐐瑰悕
```

---

## 7. 涓嶅仛

- 鏃犳埅鍥炬敼 PIN 鍋囩豢  
- 鐢?wb-align/S3 鎴?S2 鎴浘鍐掑厖 S3-UX  
- 澶囨/dns/full real 褰撴湰鍗? 
- 鏁欒偛鍔犲帤涓荤嚎 路 鎷嗛棴婧?路 瀵嗛挜杩涗粨  
- 閲嶈窇鍏ㄩ噺 G1鈥揋7 闄ら潪浜や粯閾惧洖褰掓寕  

---

## 8. 浜ゆ帴鐐瑰悕

> 瀹℃煡宸插垽绌哄彛瀹屾垚鏃犳晥銆? 
> 鏈崱鍞竴鐩爣锛?*璁╁鏌ュ憳鍦?GitHub 涓婄湅寰楄 U1鈥揢7**銆? 
> 鐪嬭骞跺叏缁?鈫?CLAIM-S3-UX锛涚湅涓嶈 鈫?浠嶆槸鏈畬鎴愩€?
```
鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲
鍑哄彛: CLAIM-S3-UX 鈬?U1鈥揢7 + D1鈥揇6锛堝惈 git push锛?淇: R1鈥揜4 鎸夐渶 路 閮ㄧ讲鍚庡繀澶嶉獙
涓嬩竴鍒€: S4
鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲
```
