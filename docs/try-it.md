# 這句摘要有根據嗎？ · Does the note support the summary?

四句摘要都附有引用。讀完每題，先選「吻合」或「需覆核」，再點開答案。V1 是前一次就診，V2 是後一次；36、16 是牙位編號。

Each summary cites a synthetic note. Pick **Match** or **Needs review**, then tap to reveal. V1 is the earlier visit, V2 the later visit. The numbers 36 and 16 identify teeth.

### 1 · c02

**引用紀錄 · Cited note (s1, V1)**<br>
預計下次回診拍攝 36 根尖片。<br>
*An X-ray of tooth 36 is planned for the next visit.*

**摘要 · Summary (V1)**<br>
已拍攝 36 根尖片。<br>
*The X-ray of tooth 36 was taken.*

<details>
<summary>查看答案 · Reveal answer</summary>

**需覆核 · Needs review** (`status_mismatch`)<br>
V1 的紀錄寫「預計」，摘要把同一件事寫成「已拍攝」。The V1 note records a plan. The summary claims completion.

[引用原文 · Source](../benchmarks/temporal_fidelity/packet.json#L3-L7) · [摘要原文 · Claim](../benchmarks/temporal_fidelity/packet.json#L51-L56) · [預期結果 · Label](../benchmarks/temporal_fidelity/expected.json#L3)

</details>

### 2 · c03

**引用紀錄 · Cited note (s2, V2)**<br>
A periapical radiograph for tooth 36 was taken.<br>
*已拍攝 36 根尖片。*

**摘要 · Summary (V2)**<br>
已拍攝 36 根尖片。<br>
*The X-ray of tooth 36 was taken.*

<details>
<summary>查看答案 · Reveal answer</summary>

**吻合 · Match** (`status_match`)<br>
這次摘要描述 V2，引用的也是 V2 紀錄。兩者都寫 36 號牙已拍攝。Both statements refer to V2 and document the same X-ray as completed.

[引用原文 · Source](../benchmarks/temporal_fidelity/packet.json#L8-L12) · [摘要原文 · Claim](../benchmarks/temporal_fidelity/packet.json#L57-L62) · [預期結果 · Label](../benchmarks/temporal_fidelity/expected.json#L4)

</details>

### 3 · c04

**引用紀錄 · Cited note (s2, V2)**<br>
A periapical radiograph for tooth 36 was taken.<br>
*已拍攝 36 根尖片。*

**摘要 · Summary (V1)**<br>
已拍攝 36 根尖片。<br>
*The X-ray of tooth 36 was taken.*

<details>
<summary>查看答案 · Reveal answer</summary>

**需覆核 · Needs review** (`visit_mismatch`)<br>
跟上一題相比，這份摘要改為描述較早的 V1。引用仍是後一次就診 V2 的紀錄。The cited note documents completion at V2. The summary moves it back to V1.

[引用原文 · Source](../benchmarks/temporal_fidelity/packet.json#L8-L12) · [摘要原文 · Claim](../benchmarks/temporal_fidelity/packet.json#L63-L68) · [預期結果 · Label](../benchmarks/temporal_fidelity/expected.json#L5)

</details>

### 4 · c10

**引用紀錄 · Cited note (s4, V1)**<br>
16 根尖片完成與否未記載。<br>
*The note leaves completion of the X-ray of tooth 16 undocumented.*

**摘要 · Summary (V1)**<br>
A periapical radiograph for tooth 16 was not taken.<br>
*16 號牙未拍攝根尖片。*

<details>
<summary>查看答案 · Reveal answer</summary>

**需覆核 · Needs review** (`status_mismatch`)<br>
紀錄把是否完成留為未知。摘要卻斷言「未拍攝」。The note leaves the outcome unknown. The summary gives a definite negative answer.

[引用原文 · Source](../benchmarks/temporal_fidelity/packet.json#L18-L22) · [摘要原文 · Claim](../benchmarks/temporal_fidelity/packet.json#L99-L104) · [預期結果 · Label](../benchmarks/temporal_fidelity/expected.json#L11)

</details>

離線報告收錄全部 18 句摘要和它們引用的原文。儲存 HTML 後即可用瀏覽器開啟。Save the HTML report to inspect all 18 claims and their cited notes offline. [下載覆核報告 · Download the HTML report](review-example.html?raw=true)

想補一題？請提供一則自編的引用紀錄、一句摘要、各自的就診代號，及你預期的結果。To suggest a case, share one invented note, one summary, their visit IDs, and your expected decision. [提交案例 · Suggest a case](https://github.com/ClinicBrain-ai/evidence-bound-ai-evaluation-harness/issues)
