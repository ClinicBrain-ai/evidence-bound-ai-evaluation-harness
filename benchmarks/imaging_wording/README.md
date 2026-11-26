# 換個說法，工具還認得嗎？ · Imaging wording challenge

同一次就診的合成來源寫「今日已完成 46 根尖片拍攝。」兩句摘要都引用這一行。先判斷「已拍攝 46 根尖片」和「已拍攝 45 根尖片」哪句可以通過。

<details><summary>看答案 · Reveal answer</summary>

46 號牙有文字支持；45 號牙需要覆核。現行工具遇到這句來源的語序，兩句都送人工。它把錯的那句攔下來，卻也讓審閱者多查了一句正確摘要。The same note supports tooth 46 only. The checker abstains on both because it cannot parse the source wording.

</details>

### 結果 · Results at the initial run (2026-11-26)

| 案例 / Set | 錯誤摘要被放過 / False passes | 正確摘要被送審 / Extra reviews | 成功解析 / Parsed coverage |
| --- | ---: | ---: | ---: |
| 新寫法 / Challenge | 0/6 | 6/6 | 0/12 |
| 既有句型 / Controls | 0/1 | 0/1 | 2/2 |

分母依序是缺乏支持的摘要、有支持的摘要、全部摘要。涵蓋一筆需要成功解析摘要及其所有引用。12 筆新寫法全部送覆核。零誤放在這裡無法證明工具辨識出矛盾。

Each of six invented notes has a supported summary and an unsupported contrast. Three source notes are in Traditional Chinese and three in English. Each challenge pair introduces wording outside the original examples in the source or summary. The two in-grammar controls are scored separately. Coverage means the checker parsed an event in the claim and in every cited note; a parsed contradiction counts toward coverage. The semantic labels were written before running the checker. This is a small, deliberately difficult synthetic set, without independent clinician annotation or estimates of population performance.

### 重跑與回報 · Reproduce and report

From the checked-out feature branch with the project installed, run:

```bash
python -m benchmarks.imaging_wording.score
python -m evidence_bound_ai_evaluation_harness check benchmarks/imaging_wording/packet.json --json
```

第二行有需覆核的項目時結束碼為 1。找出結果中的 `z2-a` 與 `z2-b`，比較兩筆的 `reason` 和來源文字。The second command intentionally exits 1 for review. Compare its per-claim results with the [semantic labels](labels.json) and [input packet](packet.json).

[回報合成反例 · Report a synthetic counterexample](https://github.com/ClinicBrain-ai/evidence-bound-ai-evaluation-harness/issues/new). 請附自編來源、摘要、就診代號、預期判定及實際 reason，並註明使用的版本。Include invented text only, the visit, expected decision, observed reason and revision.
