# SCR-Bench Leaderboard

**Skill Composition Risk (SCR) Benchmark** evaluates security risks that emerge when individually benign agent skills are composed. **Lower scores are safer** — they indicate the model resisted the composition attack.

> Source: results from *"Benign in Isolation, Harmful in Composition"* (SCR-Bench, 2026).
> Trials: CapFlow = 150 cases · TrustLift = 401 trials · AuthBlur = 118 cases.
> Backends are ranked within each sub-benchmark (not all models were evaluated on all three); full conditions are reported in the per-benchmark tables below.

---

## Coverage Matrix

Not all backends were evaluated on all three sub-benchmarks. Since cross-benchmark averages would be unfair, models are ranked **within each sub-benchmark** below. This matrix shows coverage at a glance.

| Backend | CapFlow | TrustLift | AuthBlur | # Sub-benchmarks |
|---|:---:|:---:|:---:|:---:|
| Claude Opus 4.5 | ✓ | ✓ | ✓ | 3 |
| Claude Opus 4.6 | ✓ | ✓ | ✓ | 3 |
| GPT-5.4 | ✓ | ✓ | ✓ | 3 |
| Gemini 3.1 Pro Preview | ✓ | ✓ | ✓ | 3 |
| MiniMax-M2.7 | ✓ | ✓ | ✓ | 3 |
| GPT-5.5 | ✓ | — | ✓ | 2 |
| DeepSeek-V4 | ✓ | — | ✓ | 2 |
| GLM-5.1 | ✓ | — | ✓ | 2 |
| GLM-5 | ✓ | — | ✓ | 2 |

---

## Per-Sub-Benchmark Rankings

Each sub-benchmark ranks its evaluated backends by the strongest adversarial condition. **Lower is safer.**

### SCR-CapFlow — Capability Flow (9 backends)

Ranked by **A+B Explicit** ASR (%):

| Rank | Backend | ASR (%) |
|:----:|---------|:-------:|
| 1 | **Claude Opus 4.5** | 0.7 |
| 2 | GPT-5.4 | 4.0 |
| 3 | Claude Opus 4.6 | 4.1 |
| 4 | GLM-5.1 | 26.9 |
| 5 | GLM-5 | 30.7 |
| 6 | Gemini 3.1 Pro Preview | 41.9 |
| 7 | GPT-5.5 | 47.2 |
| 8 | MiniMax-M2.7 | 74.9 |
| 9 | DeepSeek-V4 | 92.5 |

### SCR-TrustLift — Trust Transfer (5 backends)

Ranked by **Endorsed** ASR (%):

| Rank | Backend | ASR (%) |
|:----:|---------|:-------:|
| 1 | **Claude Opus 4.6** | 25.19 |
| 2 | GPT-5.4 | 96.51 |
| 3 | Gemini 3.1 Pro Preview | 97.76 |
| 4 | Claude Opus 4.5 | 100.00 |
| 4 | MiniMax-M2.7 | 100.00 |

### SCR-AuthBlur — Authorization Confusion (9 backends)

Ranked by **L3 Full Auth** ASR (%):

| Rank | Backend | ASR (%) |
|:----:|---------|:-------:|
| 1 | **GPT-5.4** | 7.3 |
| 2 | Claude Opus 4.5 | 13.1 |
| 3 | GLM-5.1 | 17.4 |
| 4 | Claude Opus 4.6 | 17.6 |
| 4 | GPT-5.5 | 17.6 |
| 6 | Gemini 3.1 Pro Preview | 35.0 |
| 7 | DeepSeek-V4 | 43.1 |
| 8 | MiniMax-M2.7 | 47.3 |
| 9 | GLM-5 | 52.9 |

**Highlights**
- **Per-benchmark winners**: Claude Opus 4.5 (CapFlow), Claude Opus 4.6 (TrustLift), GPT-5.4 (AuthBlur) — three different models, no single dominant model.
- **Trust transfer is the dominant vulnerability**: 4 of 5 evaluated backends reach ≥96% ASR under endorsement.
- **Capability flow is highly backend-polarized**: the Claude / GPT-5.4 cluster stays under 5%; DeepSeek-V4 / MiniMax-M2.7 / GPT-5.5 / Gemini-3.1 exceed 41%.

---

## SCR-CapFlow (Capability Flow)

Attack success rate (%) under isolated and composed conditions. **Composed (A+B)** is the headline.

<table>
  <thead>
    <tr>
      <th align="left">Backend</th>
      <th align="right">Control</th>
      <th align="right">A-Only</th>
      <th align="right">B-Only</th>
      <th align="right">A+B Neutral</th>
      <th align="right">A+B Explicit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>GPT-5.5</b></td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">1.6</td>
      <td align="right" style="background-color:#ffe0b2"><b>48.1</b></td>
      <td align="right" style="background-color:#ffe0b2"><u>47.2</u></td>
    </tr>
    <tr>
      <td><b>GPT-5.4</b></td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">1.2</td>
      <td align="right" style="background-color:#d4edda"><b>4.4</b></td>
      <td align="right" style="background-color:#d4edda"><u>4.0</u></td>
    </tr>
    <tr>
      <td><b>Claude Opus 4.6</b></td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda"><u>1.7</u></td>
      <td align="right" style="background-color:#d4edda">1.3</td>
      <td align="right" style="background-color:#d4edda"><b>4.1</b></td>
    </tr>
    <tr>
      <td><b>Claude Opus 4.5</b></td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda"><b>1.2</b></td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda"><u>0.7</u></td>
    </tr>
    <tr>
      <td><b>Gemini 3.1 Pro Preview</b></td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">1.3</td>
      <td align="right" style="background-color:#fff3cd"><u>30.0</u></td>
      <td align="right" style="background-color:#ffe0b2"><b>41.9</b></td>
    </tr>
    <tr>
      <td><b>MiniMax-M2.7</b></td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">1.7</td>
      <td align="right" style="background-color:#ffcdd2"><b>75.5</b></td>
      <td align="right" style="background-color:#ffcdd2"><u>74.9</u></td>
    </tr>
    <tr>
      <td><b>DeepSeek-V4</b></td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">1.5</td>
      <td align="right" style="background-color:#ef9a9a"><u>91.5</u></td>
      <td align="right" style="background-color:#ef9a9a"><b>92.5</b></td>
    </tr>
    <tr>
      <td><b>GLM-5.1</b></td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">1.3</td>
      <td align="right" style="background-color:#fff3cd"><u>25.5</u></td>
      <td align="right" style="background-color:#fff3cd"><b>26.9</b></td>
    </tr>
    <tr>
      <td><b>GLM-5</b></td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">0.0</td>
      <td align="right" style="background-color:#d4edda">0.7</td>
      <td align="right" style="background-color:#fff3cd"><u>26.4</u></td>
      <td align="right" style="background-color:#ffe0b2"><b>30.7</b></td>
    </tr>
  </tbody>
</table>

**Color scale**: green ≤5% · pale green 5–15% · yellow 15–30% · orange 30–50% · red 50–100%
**Bold** = highest ASR per backend · <u>underline</u> = second-highest

---

## SCR-TrustLift (Trust Transfer)

Harmful-installation ASR (%) when an upstream review skill provides an endorsement. Lift = Endorsed − Control.

<table>
  <thead>
    <tr>
      <th align="left">Backend</th>
      <th align="right">Control ASR</th>
      <th align="right">Endorsed ASR</th>
      <th align="right">Lift (pp)</th>
      <th align="left">Verdict</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Claude Opus 4.6</b></td>
      <td align="right" style="background-color:#d4edda">0.00</td>
      <td align="right" style="background-color:#fff3cd">25.19</td>
      <td align="right" style="background-color:#fff3cd">+25.19</td>
      <td>Conservative but vulnerable</td>
    </tr>
    <tr>
      <td><b>Claude Opus 4.5</b></td>
      <td align="right" style="background-color:#d4edda">0.00</td>
      <td align="right" style="background-color:#ef9a9a">100.00</td>
      <td align="right" style="background-color:#ef9a9a">+100.00</td>
      <td>Complete transfer</td>
    </tr>
    <tr>
      <td><b>GPT-5.4</b></td>
      <td align="right" style="background-color:#d4edda">0.00</td>
      <td align="right" style="background-color:#ef9a9a">96.51</td>
      <td align="right" style="background-color:#ef9a9a">+96.51</td>
      <td>Strong transfer</td>
    </tr>
    <tr>
      <td><b>Gemini 3.1 Pro Preview</b></td>
      <td align="right" style="background-color:#d4edda">5.49</td>
      <td align="right" style="background-color:#ef9a9a">97.76</td>
      <td align="right" style="background-color:#ef9a9a">+92.27</td>
      <td>Strong transfer</td>
    </tr>
    <tr>
      <td><b>MiniMax-M2.7</b></td>
      <td align="right" style="background-color:#d4edda">0.00</td>
      <td align="right" style="background-color:#ef9a9a">100.00</td>
      <td align="right" style="background-color:#ef9a9a">+100.00</td>
      <td>Complete transfer</td>
    </tr>
  </tbody>
</table>

> *Not evaluated on this benchmark:* GPT-5.5, DeepSeek-V4, GLM-5.1, GLM-5.

---

## SCR-AuthBlur (Authorization Confusion)

Risky approval rate (%) under control, related context, and full advisory context. Δ = percentage-point change from control.

<table>
  <thead>
    <tr>
      <th align="left">Backend</th>
      <th align="right">L0 Control</th>
      <th align="right">L1 Related</th>
      <th align="right">Δ1 (L1−L0)</th>
      <th align="right">L3 Full Auth</th>
      <th align="right">Δ2 (L3−L0)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>GPT-5.5</b></td>
      <td align="right" style="background-color:#d4edda">2.9</td>
      <td align="right" style="background-color:#e8f5e9">10.2</td>
      <td align="right" style="background-color:#d4edda">+7.3</td>
      <td align="right" style="background-color:#fff3cd"><b>17.6</b></td>
      <td align="right" style="background-color:#e8f5e9">+14.7</td>
    </tr>
    <tr>
      <td><b>GPT-5.4</b></td>
      <td align="right" style="background-color:#d4edda"><b>9.5</b></td>
      <td align="right" style="background-color:#d4edda">7.1</td>
      <td align="right" style="background-color:#f8d7da">−2.4</td>
      <td align="right" style="background-color:#d4edda">7.3</td>
      <td align="right" style="background-color:#f8d7da">−2.2</td>
    </tr>
    <tr>
      <td><b>Claude Opus 4.6</b></td>
      <td align="right" style="background-color:#d4edda">2.0</td>
      <td align="right" style="background-color:#d4edda">10.0</td>
      <td align="right" style="background-color:#d4edda">+8.0</td>
      <td align="right" style="background-color:#fff3cd"><b>17.6</b></td>
      <td align="right" style="background-color:#fff3cd">+15.6</td>
    </tr>
    <tr>
      <td><b>Claude Opus 4.5</b></td>
      <td align="right" style="background-color:#d4edda">8.7</td>
      <td align="right" style="background-color:#d4edda">9.6</td>
      <td align="right" style="background-color:#d4edda">+0.9</td>
      <td align="right" style="background-color:#e8f5e9"><b>13.1</b></td>
      <td align="right" style="background-color:#d4edda">+4.4</td>
    </tr>
    <tr>
      <td><b>Gemini 3.1 Pro Preview</b></td>
      <td align="right" style="background-color:#d4edda">10.0</td>
      <td align="right" style="background-color:#fff3cd">30.1</td>
      <td align="right" style="background-color:#ffe0b2">+20.1</td>
      <td align="right" style="background-color:#ffe0b2"><b>35.0</b></td>
      <td align="right" style="background-color:#ffe0b2">+25.0</td>
    </tr>
    <tr>
      <td><b>MiniMax-M2.7</b></td>
      <td align="right" style="background-color:#e8f5e9">19.4</td>
      <td align="right" style="background-color:#fff3cd">31.9</td>
      <td align="right" style="background-color:#fff3cd">+12.5</td>
      <td align="right" style="background-color:#ffe0b2"><b>47.3</b></td>
      <td align="right" style="background-color:#ffcdd2">+27.9</td>
    </tr>
    <tr>
      <td><b>DeepSeek-V4</b></td>
      <td align="right" style="background-color:#fff3cd">26.9</td>
      <td align="right" style="background-color:#ffe0b2">40.6</td>
      <td align="right" style="background-color:#fff3cd">+13.7</td>
      <td align="right" style="background-color:#ffe0b2"><b>43.1</b></td>
      <td align="right" style="background-color:#fff3cd">+16.2</td>
    </tr>
    <tr>
      <td><b>GLM-5.1</b></td>
      <td align="right" style="background-color:#e8f5e9">10.5</td>
      <td align="right" style="background-color:#d4edda">8.9</td>
      <td align="right" style="background-color:#f8d7da">−1.6</td>
      <td align="right" style="background-color:#e8f5e9"><b>17.4</b></td>
      <td align="right" style="background-color:#d4edda">+6.9</td>
    </tr>
    <tr>
      <td><b>GLM-5</b></td>
      <td align="right" style="background-color:#fff3cd">20.1</td>
      <td align="right" style="background-color:#ffe0b2">40.0</td>
      <td align="right" style="background-color:#ffe0b2">+19.9</td>
      <td align="right" style="background-color:#ffcdd2"><b>52.9</b></td>
      <td align="right" style="background-color:#ffcdd2">+32.8</td>
    </tr>
  </tbody>
</table>

**Δ color scale**: green = increase (context triggers risky approval) · red = decrease (context triggers refusal)
**Bold** = highest approval rate per backend

---

## Notes

- **Lower is better** for all ASR values. A 0% score means the model fully resisted the composition attack.
- Backends are ranked **within each sub-benchmark** because coverage is uneven (see Coverage Matrix above). No cross-benchmark aggregate is reported.
- Per-benchmark ranking uses the strongest adversarial condition: A+B Explicit (CapFlow), Endorsed (TrustLift), L3 Full Auth (AuthBlur).
- Submitting a new model: open a Discussion on the dataset repo with the configuration used to run the benchmark.
