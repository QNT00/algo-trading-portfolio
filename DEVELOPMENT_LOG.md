# Development Log — Algorithmic Crypto Trading System
# 개발 로그 — 알고리즘 암호화폐 자동매매 시스템

> **목적 (Purpose)**
> KO: 시스템 개발 과정에서 발생한 문제, 의사결정, 해결 방법을 기록.
>
> EN: Documents problems, decisions, and solutions encountered during system development.

---

## 2026-02-22: AdaptiveTradingSystem V2 통합 — 하이브리드 인공지능 트레이딩 봇 구축
## 2026-02-22: AdaptiveTradingSystem V2 Integration — Hybrid AI Trading Bot Architecture

### 배경 (Background)

KO:
V1(Rule-based 시스템)의 잦은 휩쏘(Whipsaw)로 인한 승률 하락과 레짐 판단의 모호성을 해결하기 위해,
비정상적인 금융 시계열 데이터에 강건한 **강화학습 및 딥러닝 기반 V2 업그레이드**를 단행.

EN:
To resolve the degrading win rate caused by frequent whipsaws and ambiguous regime detection in V1 (Rule-based system),
a major **Deep Learning & Reinforcement Learning (V2) upgrade** was executed, proving robust against non-stationary financial time series.

---

### 문제 1: 정적 임계값과 비정상성 편향 (Problem 1: Static Thresholds & Non-stationarity Bias)

KO:
**현상**: V1 모델에서 보조지표(RSI, MACD)의 고정된 임계값(예: RSI > 60)은 시장의 변동성이 바뀔 때마다 오작동을 일으킴.
과거에 성공했던 임계값이 미래에도 통한다는 보장이 없는 전형적인 '비정상성(Non-stationarity)' 한계 노출.

EN:
**Symptom**: In the V1 model, static thresholds for technical indicators (e.g., RSI > 60) failed whenever market volatility regimes shifted.
This exposed the classic 'Non-stationarity' limitation—past successful thresholds do not guarantee future performance.

---

### 문제 2: 다차원 리스크 관리 부재 (Problem 2: Lack of Multi-dimensional Risk Management)

KO:
**현상**: 승률뿐만 아니라 진입 금액(Position Size), 레버리지(Leverage), 조기 청산 인내도(Exit Patience) 등을
시장 상황에 따라 유기적으로 조절해야 함에도 불구하고, V1에서는 하드코딩된 비율로 단방향 관리만 됨.

EN:
**Symptom**: Market conditions require organic adjustment not only of entry direction but also Position Sizing, Leverage, and Exit Patience.
V1 rigidly applied hardcoded ratios, creating a one-dimensional risk management bottleneck.

---

### 해결 방법: 하이브리드 V2 아키텍처 도입 (Solution: Hybrid V2 Architecture)

KO:
결정 단위를 3단계로 쪼개고 각각 최적의 AI 방법론을 적용한 통합 파이프라인(`train_all_v2.py`) 설계:

1. **환경 분석**: HMM(Hidden Markov Model) 도입.
   단순 가격 지표를 40여 개의 파생 변수(Hurst Exponent 등)로 확장하고, 비지도 학습(HMM)과 지도 학습(LightGBM)을 결합하여 현재를 넘어 **미래의 상태 전환 확률(Regime Transition Probability)**을 예측.
2. **시그널 생성**: CNN 계열의 TCN(Temporal Convolutional Network) 도입.
   과적합 방지를 위해 인과적 패딩(Causal Padding)을 적용하여 철저히 미래 데이터를 차단하고 확률 분포 기반(Softmax) 신뢰도(Confidence) 반환.
3. **자금 관리**: 강력한 PPO(Proximal Policy Optimization) 심층 강화학습 에이전트 도입.
   40차원의 시장 환경을 5차원의 행동 공간(매매 방향, 레버리지, 크기 등)으로 맵핑하여 Sortino Ratio 기반 보상 함수를 극대화하도록 자가 학습.
4. **하방 호환성 (Fallback)**:
   V2 딥러닝 컴포넌트 오류 시, 프로그램이 크래시(Crash)되지 않고 기존 안전한 V1(Rule-based) 엔진으로 우회하도록 마이크로서비스 관점의 구조적 안정성을 채택.

EN:
Divided the decision unit into 3 layers, applying optimal AI methodologies per layer, integrated via `train_all_v2.py`:

1. **Environment Analysis**: Introduced HMM.
   Expanded features to 40+ structural variables (e.g., Hurst Exponent). Combined Unsupervised (HMM) and Supervised (LightGBM) learning to predict the **Regime Transition Probability** rather than just identifying the current state.
2. **Signal Generation**: Introduced TCN (Temporal Convolutional Network).
   Applied Causal Padding strictly to prevent look-ahead bias, outputting probabilistic Confidence via Softmax.
3. **Capital Management**: Introduced PPO Deep Reinforcement Learning Agent.
   Mapped a 40-dimensional observation space to a 5-dimensional continuous action space (Direction, Leverage, Size, etc.), self-optimizing a Sortino Ratio-based reward function.
4. **Backward Compatibility (Fallback)**:
   Adopted a robust microservice-like architecture: if V2 deep learning components fail to load or error out, the system gracefully falls back to the reliable V1 (Rule-based) engine instead of crashing.

---

### 결과 및 배운 점 (Result & Learnings)

KO:
1. **과적합 통제의 중요성**: '수익이 나는 척'하는 코드를 짜는 것은 쉽지만, `rolling(raw=True)` 적용이나 교차피처 미래 참조를 원천 차단하는 구조를 세우는 과정이 V2 성패의 가장 큰 핵심이었음.
2. **소프트웨어 공학적 설계 가치**: 단일 봇을 수학적으로 고도화하는 것을 넘어, 객체지향의 상속(Inheritance)과 폴백(Fallback) 패턴을 활용함으로써 시스템 운영 중에 AI 모델을 바꿔치기(Hot-swap)할 수 있는 무중단 시스템 베이스를 확보함.

EN:
1. **Controlling Overfitting is Everything**: Writing code that "looks profitable" is easy. Enforcing `rolling(raw=True)` and architecturally blocking look-ahead bias across cross-features was the true differentiator for V2's integrity.
2. **Engineering Resiliency**: Beyond mathematical upgrades, utilizing Inheritance and Fallback patterns secured a zero-downtime foundation, natively allowing hot-swapped AI model weights during live operations.

---

## 2026-02-21: AdaptiveTradingSystem 전략 재설계 — MomentumTrend v1 → ABT v2
## 2026-02-21: AdaptiveTradingSystem Strategy Overhaul — MomentumTrend v1 → ABT v2

### 배경 (Background)

KO:
이전까지 Adaptive는 Trend+Pullback 전략(RSI>60=Long 류)을 사용했으나 평균 승률 24%로 실패 판정.
원인 분석 후 **전략 로직 자체를 교체**하는 방향으로 진행.

EN:
The Adaptive system had been running a Trend+Pullback strategy (RSI-based momentum entry)
but achieved only ~24% win rate. Root cause analysis concluded a fundamental logic flaw,
leading to a complete strategy replacement.

---

### 문제 1: MomentumTrend v1 시도 및 실패 (Problem 1: MomentumTrend v1 Attempt)

KO:
**시도한 것**: Trend+Pullback 실패 후, 순수 추세 추종(MomentumTrend)으로 전환.
- RSI/Stoch/BB 완전 제거 — 추세와 역방향 신호를 생성하던 원인
- ADX Hard Gate 추가 — ADX 기준값 미달 시 즉시 NEUTRAL (횡보 자동 차단)
- EMA 정렬 6봉(30분) 지속성 확인 — 즉각적 EMA 플립 방지

**결과** (3구간 백테스트):

| 기간 | 승률 | 손익비 | 수익률 |
|------|-----|------|------|
| 상승장 (6개월) | ~33% | ~1.6:1 | 대폭 손실 |
| 하락장 (6개월) | ~30% | ~1.7:1 | 대폭 손실 |
| 횡보 (2개월) | ~31% | ~1.6:1 | 손실 |

**진전된 부분**: 손익비 > 1 (평균 수익 > 평균 손실) — 트레일링 스탑 버그 수정 효과
**실패 원인**: 5분봉 EMA 기반 추세 추종 승률은 구조적으로 ~33% 상한 존재
→ 필요 손익분기 승률(~39%)에 미달 → 파라미터 조정으로 해결 불가

EN:
**What was tried**: After Trend+Pullback failure, pivoted to pure momentum trend-following.
- Removed RSI/Stoch/BB — these were generating signals counter to trend direction
- Added ADX Hard Gate — below threshold, return NEUTRAL immediately (ranging market filter)
- Required EMA alignment persistence across multiple bars — prevents entries on transient EMA flips

**Results** (3-period backtest):

| Period | WR | P/F | Return |
|--------|-----|-----|--------|
| Bull (6 months) | ~33% | ~1.6:1 | Large loss |
| Bear (6 months) | ~30% | ~1.7:1 | Large loss |
| Ranging (2 months) | ~31% | ~1.6:1 | Loss |

**What improved**: Profit factor > 1 (avg win > avg loss) — trailing stop bug fix took effect
**Failure reason**: 5-minute EMA-based trend following has a structural ~33% WR ceiling.
Break-even WR needed (~39%) cannot be reached; no parameter adjustment can close this gap.

---

### 문제 2: 트레일링 스탑 Dead Parameter 버그 (Problem 2: Trailing Stop Dead Parameter)

KO:
`risk_manager.py`의 `update_trailing_stop()`에서 config로 주입된 `trailing_stop_distance`가
실제 로직에 반영되지 않고 ATR 하드코딩 값만 사용되던 버그 발견.
- 결과: 0~2% 수익 구간에서 스탑이 바짝 붙어 TP 전에 청산 → R:R 역전 현상
- 수정: config 파라미터를 실제 로직에 반영, 초기 수익 구간에서 트레일링 없음으로 변경

EN:
Discovered a dead-parameter bug in `risk_manager.py`'s `update_trailing_stop()`:
the config-injected `trailing_stop_distance` was loaded but never applied.
Hardcoded ATR multipliers were used instead.
- Effect: stop loss hugged the position at 0–2% profit, triggering before TP → R:R inversion
- Fix: wired config parameter into actual logic; removed trailing in early profit phase

---

### 해결 방법: ABT v2 전략 채택 (Solution: ABT v2 Strategy)

KO:
**핵심 결정**: 5분봉 추세 추종의 구조적 한계를 인정하고 전략 자체를 교체.

**새 전략**: ABT (Adaptive Breakout-Trend)
- 타임프레임: 5분봉 → **15분봉** (노이즈 대 신호 비율 개선)
- 진입 구조: **3-Layer 필터**
  - Layer 1: 환경 필터 (ADX, 볼린저밴드 폭, 거래량 — 레짐 분류기 독립)
  - Layer 2: EMA/DI 방향 판단 (필터 역할만, 진입 타이밍 아님)
  - Layer 3: VBO 돌파 + 눌림목 혼합 트리거
- R:R 구조: 2.0:1 (이전보다 목표치 낮춤 → 손익분기 승률 33.3%로 하향)
- 트레일링: Phase 0~3 (초기 수익 구간에서 트레일 없음 → R:R 보장)

**VBO 참고 근거**: 이전 Trading Bot 프로젝트에서 VBO 전략 소규모 실거래 성공 경험 있음.
단, 당시 완성형이 아니었으므로 아이디어만 참고하고 설계는 새로 수행.

EN:
**Core decision**: Acknowledged the structural WR ceiling of 5-min trend following.
Replacing the strategy rather than tuning parameters.

**New strategy**: ABT (Adaptive Breakout-Trend)
- Timeframe: 5-minute → **15-minute** (better signal-to-noise ratio)
- Entry structure: **3-Layer filter**
  - Layer 1: Environment filter (ADX, Bollinger Band width, volume — replaces regime classifier)
  - Layer 2: EMA/DI direction determination (filter only, not timing signal)
  - Layer 3: VBO breakout + pullback combined trigger
- R:R: 2.0:1 (lower target than before → break-even WR reduced to 33.3%)
- Trailing: Phase 0–3 (no trailing in early profit phase → R:R protection)

**VBO rationale**: Prior Trading Bot project demonstrated partial success with VBO strategy in small-scale live trading.
Not production-ready at the time, but validated the core concept.

---

### 배운 것 (Learnings) / Learnings

KO:
1. **전략 교체 기준**: 파라미터 조정으로 해결할 수 없는 구조적 한계가 확인되면 전략 자체를 교체해야 함.
   "어떤 숫자를 바꾸면 나아지지 않을까"라는 생각이 드는 순간이 교체 타이밍의 신호.

2. **승률 vs 손익비의 균형**: 손익비 > 1 달성 자체는 의미 있지만 충분하지 않음.
   손익분기 승률(= 1 / (1 + 손익비)) 이상의 승률이 반드시 필요.
   예: 손익비 1.6:1 → 손익분기 승률 38.5% → 실제 승률 33%이면 손실.

3. **타임프레임 선택의 중요성**: 동일한 전략 로직이라도 5분봉과 15분봉에서 신뢰도가 다름.
   짧은 타임프레임일수록 노이즈가 많아 진입 신호가 빠르게 무효화될 수 있음.

4. **3-Layer 구조의 가치**: 진입 조건을 "환경 필터 → 방향 판단 → 타이밍"으로 분리하면
   각 계층이 독립적으로 책임을 지므로 어느 계층에서 문제가 발생하는지 분석이 쉬워짐.
   단일 점수 합산 구조에서는 불가능한 투명성.

EN:
1. **When to replace vs. tune**: When a structural ceiling is confirmed and no parameter change
   can overcome it, the strategy logic itself must be replaced. Asking "what number should I change?"
   is the signal that replacement — not tuning — is needed.

2. **Win rate vs. profit factor balance**: Achieving PF > 1 is meaningful but insufficient.
   Win rate must exceed the break-even WR (= 1 / (1 + PF)).
   Example: PF 1.6:1 → break-even WR 38.5% → actual WR 33% → still a loss.

3. **Timeframe selection matters**: The same strategy logic produces very different reliability
   on 5-minute vs. 15-minute candles. Shorter timeframes have more noise,
   causing entry signals to become invalidated rapidly.

4. **Value of layered entry structure**: Separating entry conditions into Environment → Direction → Timing
   makes each layer independently accountable, making it easy to diagnose which layer failed.
   This transparency is impossible with a single aggregated score approach.

---

## 2026-02-19: Fixed Take-Profit 도입 및 핵심 버그 수정
## 2026-02-19: Introducing Fixed Take-Profit & Critical Bug Fix

### 문제 (Problem) / Problem

KO:
1. 트레일링 스탑 업데이트 시 고정 익절(TP) 주문이 함께 취소됨
   - `update_trailing_stop()`에서 `cancel_all_orders()`를 호출하는 구조 때문
   - TP 활성화(`use_take_profit: True`)를 해도 실제로는 매번 취소되어 무효화됨
   - 결과적으로 수동으로 TP 가격을 기억해서 직접 청산하는 임시방편으로 운영 중

2. 수익 중인 포지션이 역전되어 손실로 마무리되는 패턴 반복
   - 트레일링 스탑만으로는 빠른 역전 움직임에 대응 불가
   - 특히 수익이 쌓이던 포지션이 순식간에 원래 손절선까지 내려오는 경우 발생

EN:
1. Fixed take-profit (TP) orders were being cancelled every time the trailing stop updated.
   - Root cause: `update_trailing_stop()` called `cancel_all_orders()` internally.
   - Even with `use_take_profit: True` in config, TP orders were silently wiped on every trailing stop adjustment.
   - Workaround in place: manually remembering TP prices and closing positions by hand.

2. Profitable positions repeatedly reversed into losses.
   - Trailing stop alone was too slow to react to sharp reversals.
   - Positions that had built up unrealized profit would collapse back to the original stop-loss level.

---

### 가설 (Hypothesis) / Hypothesis

KO:
- 공격적 단타 시스템(5분봉, 7종목)에서는 큰 추세 수익보다
  일관된 R:R로 승률을 확보하는 것이 기대수익(EV) 측면에서 유리
- 트레일링 스탑은 손실 제한 역할에 집중, TP는 익절 확정 역할로 분리

EN:
- For an aggressive scalping system (5-min candles, 7 symbols), securing consistent R:R wins
  produces better expected value (EV) than chasing large trend moves.
- Design philosophy: trailing stop handles downside protection; fixed TP handles profit capture. Separate concerns.

---

### 해결 방법 (Solution) / Solution

KO:

**버그 수정** (`execution_engine.py`):
```python
# 변경 전: 모든 주문 취소 (TP까지 사라짐)
self._retry(self.exchange.cancel_all_orders, lsym)

# 변경 후: 스탑로스 주문 ID만 취소 (TP 보존)
stop_order_id = position.get('stop_order_id')
if stop_order_id:
    self._retry(self.exchange.cancel_order, stop_order_id, lsym)
```

**포지션 청산 시나리오별 동작 정리**:
| 상황 | SL 주문 | TP 주문 |
|---|---|---|
| 트레일링 스탑 업데이트 | 취소 후 재배치 | 유지 |
| SL 발동 (손절) | 체결 | 거래소가 자동 취소 |
| TP 발동 (익절) | 거래소가 자동 취소 | 체결 |
| 수동 종료 | `cancel_all_orders`로 취소 | `cancel_all_orders`로 취소 |

EN:

**Bug fix** (`execution_engine.py`):
```python
# Before: cancel ALL orders (TP disappears as side effect)
self._retry(self.exchange.cancel_all_orders, lsym)

# After: cancel only the stop-loss order by ID (TP is preserved)
stop_order_id = position.get('stop_order_id')
if stop_order_id:
    self._retry(self.exchange.cancel_order, stop_order_id, lsym)
```

**Exit scenario matrix**:
| Scenario | SL Order | TP Order |
|---|---|---|
| Trailing stop update | Cancelled & replaced | Preserved |
| SL triggered (stop-out) | Filled | Auto-cancelled by exchange |
| TP triggered (take profit) | Auto-cancelled by exchange | Filled |
| Manual close | Cancelled via `cancel_all_orders` | Cancelled via `cancel_all_orders` |

---

### 추가 변경사항 / Additional Changes

**SIDEWAYS 레짐 진입 임계값 강화** (`signal_generator.py`):

KO:
- 문제: SIDEWAYS 레짐에서 손실 비중이 높음 (2/17~18 로그 분석)
- 해결: 완전 차단이 아닌 임계값 상향 (고품질 신호만 통과, 강한 신호는 여전히 진입 가능)
- SIDEWAYS_QUIET, SIDEWAYS_CHOPPY 각각 임계값 상향 조정

EN:
- Problem: SIDEWAYS regime showed a disproportionate share of losses (log analysis 2/17–18).
- Solution: Raised entry threshold per regime — not a full block, but only high-confidence signals pass.
- SIDEWAYS_QUIET and SIDEWAYS_CHOPPY thresholds raised independently.

**최대 동시 포지션 축소 / Max concurrent positions reduced** (`config.py`):

KO: 문제: 소규모 계좌에서 다수 포지션 × 리스크 비율 = 과도한 동시 노출 → "잔고 부족" 에러 반복 발생
    해결: 최대 동시 포지션 수 축소 (계좌 규모 증가 시 확대 예정)

EN: Problem: On a small account, multiple simultaneous positions × risk per trade = excessive exposure → repeated "insufficient balance" errors.
    Solution: Reduced max concurrent positions. Will scale up as account grows.

---

### 결과 (Result) / Result

KO:
- 2026-02-19 이후부터 클린 데이터 수집 시작 (버그 수정 + 전체 설정 반영)
- 이전 로그(2/17~18) 기준 승률: 51~62% 범위 (설정 전환 시점 혼재)
- 2주 후(3월 초) 레짐별 승률, TP 체결률 분석 예정

EN:
- Clean data collection begins from 2026-02-19 (all bug fixes + config changes applied)
- Prior log win rates (2/17–18): 51–62% range (mixed — config transitions overlap)
- Planned analysis in ~2 weeks (early March): win rate by regime, TP fill rate

---

### 배운 것 (Learnings) / Learnings

KO:
1. **거래소 API 특성**: Bybit는 주문 수정(modify) API 미지원 → cancel + 재주문 방식 강제.
   이 구조에서 `cancel_all_orders`는 의도치 않은 부수효과를 만들 수 있음.
   → 항상 주문 ID 기반 개별 취소를 기본으로 사용해야 함.

2. **Dead Parameter 발견**: `config.py`의 `trailing_stop_distance` 값은 로드 후 미사용.
   실제 트레일링 스탑은 `risk_manager.py`에 하드코딩된 단계별 로직으로 동작.
   → config 값을 바꿔도 동작에 영향 없음. 추후 코드 정리 필요.

3. **데이터 기반 의사결정의 한계**: 3일 로그에서 SIDEWAYS 레짐 성과가 날마다 달랐음
   (2/17: SIDEWAYS 손실 우세 vs 2/18 오전: SIDEWAYS 수익 우세).
   하드코딩 임계값은 단기 데이터 과적합 위험. 2~3주 후 재검토 필요.

EN:
1. **Exchange API constraint**: Bybit does not support order modify — forced into cancel + re-submit pattern.
   In this architecture, `cancel_all_orders` creates unintended side effects.
   → Default to individual order cancellation by ID; use `cancel_all_orders` only for full position closes.

2. **Dead parameter discovered**: `trailing_stop_distance` in `config.py` is loaded but never read.
   Actual trailing stop logic is hardcoded in `risk_manager.py` as a staged tightening process.
   → Changing the config value has zero effect. Cleanup needed.

3. **Limits of small-sample decisions**: SIDEWAYS regime performance varied day by day across only 3 days of logs.
   Hardcoded thresholds risk overfitting to short-term data. Revisit in 2–3 weeks.

---

## 2026-02-18: 시스템 파라미터 조정
## 2026-02-18: System Parameter Tuning

### 변경 내용 / Changes

KO:
- 확신도 임계값 상향 (저품질 신호 필터링 강화)
- 트레일링 스탑 거리 조정 (포지션 여유 확보 — 실제 dead parameter였음, 추후 정리 필요)
- 스캔 주기 연장: 30초 → 60초 (중복 진입 시도 감소)

EN:
- Confidence threshold raised (stronger filtering of low-quality signals)
- Trailing stop distance adjusted (give positions more room — later confirmed dead parameter, cleanup needed)
- Scan interval extended: 30s → 60s (reduce duplicate entry attempts during open positions)

### 이유 / Rationale

KO:
- 기존 임계값에서 기준치를 겨우 넘긴 신호들이 손실 기여 비중 높음
- 30초 스캔은 포지션 보유 중 중복 시도로 "잔고 부족" 에러 빈발

EN:
- Signals just above the previous threshold were disproportionately contributing to losses.
- 30-second scan interval caused duplicate entry attempts while positions were open, generating frequent "insufficient balance" errors.

---

## 2026-02-05 ~ 2026-02-09: AdaptiveTradingSystem 개발 완료 및 멀티봇 충돌 해결
## 2026-02-05 ~ 2026-02-09: AdaptiveTradingSystem Completion & Multi-Bot Conflict Resolution

### 배경 / Background

KO:
AggressiveTradingSystem을 개발하는 동시에, **AdaptiveTradingSystem(단타)**과
**TrendFollowingSystem(중장기)**을 별도로 개발하는 멀티봇 아키텍처를 구성한 기간.

EN:
This period covered building a multi-bot architecture in parallel:
**AdaptiveTradingSystem** (short-term scalping) and **TrendFollowingSystem** (swing/trend).

---

### 문제 1: 백테스터 버그 (Problem 1: Backtester Bugs)

KO:
AdaptiveTradingSystem의 백테스터(`backtester.py`)에서 두 가지 핵심 버그 발견:

1. **레버리지 1x 고정 버그**: `risk_manager.py`에서 ATR 기반 변동성 계산이 잘못 처리되어
   레버리지가 항상 1배로 고정됨. 포지션 사이징 전체가 의도와 달리 작동하고 있었음.

2. **P&L 이중 적용 버그**: equity curve 계산에서 레버리지가 두 번 적용되던 문제.
   실제 수익률이 과대 계상되어 백테스트 결과가 왜곡됨.
   Dead code 제거 후 수정.

EN:
Two critical bugs found in `backtester.py`:

1. **Leverage stuck at 1x**: ATR-based volatility in `risk_manager.py` was not being processed correctly,
   causing leverage to default to 1x regardless of market conditions.
   The entire position sizing logic was silently broken.

2. **P&L double-application**: The equity curve calculation was applying leverage twice,
   inflating simulated returns. Removed dead code and corrected.

---

### 문제 2: 고정 임계값의 한계 (Problem 2: Fixed Entry Threshold Limitations)

KO:
초기 설계는 롱/숏 진입 확신도를 고정 임계값으로 적용했음.
그러나 실전에서는 시장 레짐(추세/횡보/고변동성)에 따라 신호의 신뢰도가 달라지는 문제.
- 추세장에서의 신호와 횡보장에서의 같은 수치 신호는 신뢰도가 다름
- 하나의 임계값으로 모든 시장 상황을 처리하는 것은 근본적 한계

**해결**: 레짐별 동적 임계값 구현
- `STRONG_UPTREND`: 롱 진입에 유리하게 조정
- `STRONG_DOWNTREND`: 숏 진입에 유리하게 조정
- `HIGH_VOLATILITY`: 진입 조건 강화 (모든 방향)
- 기본 임계값 위에 additive adjustment를 적용하는 구조

EN:
Initial design used fixed confidence thresholds for long/short entry.
In live trading, the reliability of signals varies significantly by market regime.
- The same numerical confidence score means different things in a trending vs. ranging market
- A single threshold cannot meaningfully filter across all conditions

**Solution**: Regime-conditional dynamic thresholds
- `STRONG_UPTREND`: Long-entry threshold adjusted favorably
- `STRONG_DOWNTREND`: Short-entry threshold adjusted favorably
- `HIGH_VOLATILITY`: Entry conditions tightened for all directions
- Structure: additive adjustments on top of a base threshold (not absolute overrides)

---

### 문제 3: 두 봇 포지션 충돌 (Problem 3: Multi-Bot Position Conflicts)

KO:
AdaptiveTradingSystem(단타)과 TrendFollowingSystem(중장기)을 동시에 운영할 때
같은 거래소 계정에서 충돌 발생:

1. **추매 문제**: 동일 코인에서 두 봇이 같은 방향 진입 → 의도치 않은 포지션 확대
2. **스탑 간섭**: 단타봇의 좁은 스탑로스가 중장기 포지션까지 청산
3. **반대 진입**: 두 봇이 같은 코인에서 반대 방향 진입 → 헤지 발생 (양쪽 수수료 낭비)

**해결**:
1. 두 시스템의 포지션 추적 로직 완전 분리 (shared state 제거)
2. 각 봇이 독립적으로 API에 연결, nohup으로 별도 프로세스 운영
3. 계좌 규모가 커지면 거래소 서브계정으로 완전 분리 예정
4. 소수점 처리 버그 추가 수정 (저가 코인 주문 수량 정밀도)

EN:
Running AdaptiveTradingSystem (short-term) and TrendFollowingSystem (swing) simultaneously
on the same exchange account caused three classes of conflict:

1. **Unintended pyramiding**: Both bots entering the same direction on the same coin → position size grows beyond intent
2. **Stop interference**: Short-term bot's tight stop-loss inadvertently closing long-term positions
3. **Hedging**: Bots entering opposite directions on the same coin → fee-burning hedge with no intent

**Resolution**:
1. Fully decoupled position tracking logic between the two systems (removed shared state)
2. Each bot runs as an independent process with its own API connection via nohup
3. Sub-account separation planned when capital grows sufficiently
4. Fixed decimal precision bug for low-price coins (order quantity precision)

---

### TrendFollowingSystem 설계 결정 / TrendFollowingSystem Design Decisions

KO:
단타 시스템과 상관관계를 낮추기 위한 설계 선택:
- **타임프레임**: 4시간봉 + 일봉 (멀티 타임프레임, 단타와 완전히 다름)
- **진입 로직**: 일봉 추세 확인 → 4시간봉에서 타이밍 포착
- **보유 기간**: 수일 ~ 수주
- **청산**: 일봉 ATR 기반 트레일링 (단타보다 훨씬 넓은 스탑)
- **레버리지**: 낮게 설정 (장기 보유 중 변동성 흡수 필요)

백테스트 결과 (6개 코인, 12개월 하락장):
- Buy & Hold 대비 유의미한 Alpha 확인 → 절대 수익보다 리스크 대비 수익이 목표
- MDD: 개별 코인 대비 낮게 유지 (방어적 구조 확인)
- 거래 빈도: 월 1~2회 수준 (단타와 상관관계 낮음)

EN:
Design choices to minimize correlation with the scalping system:
- **Timeframe**: 4-hour + Daily (multi-timeframe — completely separate from 5-min scalping)
- **Entry logic**: Confirm trend on daily chart → time entry on 4H chart
- **Hold duration**: Days to weeks
- **Exit**: Daily ATR-based trailing stop (much wider than scalping system)
- **Leverage**: Conservative (must absorb volatility during extended holds)

Backtest results (6 coins, 12-month bear market):
- Meaningful alpha confirmed vs. Buy & Hold → goal is risk-adjusted return, not absolute return
- MDD: substantially lower than individual coins (defensive structure validated)
- Trade frequency: ~1–2 per month (low correlation with scalping system)

---

### 배운 것 (Learnings) / Learnings

KO:
1. **백테스터는 별도로 검증해야 함**: 전략 코드보다 백테스터 자체의 버그(레버리지 1x 고정, P&L 이중 적용)가
   결과를 더 크게 왜곡할 수 있음. "백테스트가 안 좋다 = 전략이 나쁘다"가 아닐 수 있음.

2. **단일 임계값 vs 레짐별 임계값**: 시장은 상태가 바뀐다. 추세장 신호와 횡보장 신호는
   같은 수치여도 다른 의미를 가짐. 임계값은 레짐에 따라 조정되어야 함.

3. **멀티봇 간섭은 설계 단계에서 고려해야 함**: 단일 봇 테스트에서 잘 작동하던 것이
   두 봇을 동시에 운영하면 예상치 못한 상호작용을 만들 수 있음. 포지션 상태 관리를
   처음부터 독립적으로 설계하는 것이 중요.

4. **실거래 = 가장 정직한 모의거래**: 소액 실거래를 페이퍼 트레이딩 대신 선택.
   슬리피지, 체결 지연, 심리적 압박 등 시뮬레이션에서 잡히지 않는 요소를 직접 경험.

EN:
1. **Validate the backtester, not just the strategy**: Bugs in the backtester itself (leverage stuck at 1x,
   P&L double-counted) distorted results more than strategy flaws would. "Poor backtest" ≠ "poor strategy"
   without first verifying the testing infrastructure.

2. **Single threshold vs. regime-conditional thresholds**: Markets shift between states.
   The same confidence score means different things in trending vs. ranging conditions.
   Thresholds must adapt to regime, not just to a fixed signal strength.

3. **Multi-bot interference must be designed for upfront**: What works cleanly in single-bot testing
   can produce unexpected interactions in multi-bot operation (shared positions, stop interference, hedging).
   Position state management must be fully isolated from the start.

4. **Live trading is the most honest paper trading**: Chose small-capital live trading over simulation.
   Slippage, fill delays, and psychological pressure are not captured in backtests — they must be experienced directly.

---

## 2025: ML 기반 가격 예측 시스템 구축 → 한계 발견 → 레짐 기반 시스템으로 전환
## 2025: Building an ML Price Prediction System → Discovering Its Limits → Pivoting to Regime-Based Design

### 구축한 것 (What Was Built)

KO:
단순한 모델 실험이 아닌, **프로덕션 수준의 ML 트레이딩 파이프라인 전체**를 직접 설계하고 구현.

**1. 데이터 파이프라인**
- `Master_Data_Pump.py`: 6개 코인 × 7개 타임프레임 × 1.5년치 OHLCV 수집 (총 ~300MB Parquet)
- `Live_Data_Pump.py`: 60초 주기 증분 동기화 (마지막 타임스탬프 기준 delta fetch)
- ThreadPoolExecutor 병렬 다운로드, API 속도 제한 자동 처리

**2. 피처 엔진 (72개 지표)**
- `indicators.py`: 추세(MA/EMA 7종), 모멘텀(RSI/MACD/Stochastic), 변동성(ATR/BB), 거래량(OBV/VWAP)
- **독자 설계 피처**: 가격 속도(Velocity), 가속도(Acceleration), 드래그(Drag), 엔트로피(Entropy)
- 시장 미시구조: 호가창 불균형(Order Book Imbalance), 펀딩비, 미결제약정
- 확률 피처: Monte Carlo 1000회 시뮬레이션 기반 `Prob_Up_1h`

**3. ML 학습 파이프라인**
- `Feature_Factory.py`: Triple Barrier 라벨링 적용
  - Profit Target: 진입 + ATR × 배수
  - Stop Loss: 진입 − ATR × 배수
  - Time Limit: N봉 타임아웃
  - 라벨: 0(손절), 1(타임아웃), 2(익절)
- `Model_Training.py`: PyTorch LSTM + Attention 아키텍처
  - LSTM 2레이어, Attention 가중합, FC 레이어
  - **메모리맵(Memmap) 학습**: 7GB+ 데이터를 RAM 없이 학습하는 엔지니어링
- `AutoML_Master.py`: 코인별 XGBoost 앙상블 (6개 모델 독립 학습)
- `Live_Inference_Bridge.py`: 실시간 추론 (최근 N봉 → z-score 정규화 → LSTM → 확률 출력)

**4. Streamlit 대시보드**
- 봇 실행/정지, 누적 P&L 곡선, 실시간 로그
- 멀티타임프레임 차트 (Plotly), 펀딩비/공포탐욕지수, 호가창 시각화
- 전략 시뮬레이션 샌드박스, Kelly Criterion 계산기

EN:
This was not a simple model experiment — a **full production-grade ML trading pipeline** was designed and implemented end-to-end.

**1. Data Pipeline**
- `Master_Data_Pump.py`: 1.5 years of OHLCV for 6 coins × 7 timeframes (~300MB Parquet)
- `Live_Data_Pump.py`: 60-second incremental sync (delta fetch from last timestamp)
- Parallel downloads via ThreadPoolExecutor with automatic API rate-limit handling

**2. Feature Engine (72 indicators)**
- `indicators.py`: Trend (7 MA/EMA variants), Momentum (RSI/MACD/Stochastic), Volatility (ATR/BB), Volume (OBV/VWAP)
- **Custom-designed features**: Price Velocity, Acceleration, Drag, Entropy — physics-inspired metrics
- Market microstructure: Order Book Imbalance, Funding Rate, Open Interest
- Probability feature: `Prob_Up_1h` via Monte Carlo simulation (1,000 paths)

**3. ML Training Pipeline**
- `Feature_Factory.py`: Triple Barrier Labeling (methodology from Lopez de Prado's *Advances in Financial Machine Learning*)
  - Profit Target / Stop Loss: ATR-based multipliers
  - Time Limit: N-bar timeout
  - Labels: 0 (stop-out), 1 (timeout), 2 (take-profit)
- `Model_Training.py`: PyTorch LSTM + Attention
  - Multi-layer LSTM, attention-weighted pooling, FC layers
  - **Memory-mapped training**: trained on 7GB+ datasets without loading into RAM
- `AutoML_Master.py`: Coin-specific XGBoost ensemble (6 independent models)
- `Live_Inference_Bridge.py`: Real-time inference — last N bars → z-score normalization → LSTM → softmax probabilities

**4. Streamlit Dashboard**
- Bot start/stop, cumulative P&L curve, real-time log tail
- Multi-timeframe interactive charts (Plotly), funding rates, Fear & Greed Index, order book visualization
- Strategy simulation sandbox, Kelly Criterion calculator

---

### 한계 발견 (Problem Discovered)

KO:
기술 스택은 완성됐지만 **실전 수익성 검증에서 한계**에 도달.
- 학습 데이터(in-sample)에서는 모델이 수렴하고 정확도도 나옴
- 실전 추론(out-of-sample)에서 예측 정확도가 무작위 수준으로 하락
- 원인 분석:
  1. **비정상성(Non-stationarity)**: 금융 시계열의 통계적 특성이 시간에 따라 변함. 과거 패턴이 미래에 반복된다는 보장 없음.
  2. **과적합(Overfitting)**: 72개 피처, 7GB 데이터에도 불구하고 모델이 과거 노이즈를 패턴으로 학습. 학습 데이터에서만 작동.
  3. **시장 효율성**: 단순히 반복 가능한 가격 패턴은 이미 다른 참여자들이 차익거래로 소멸시킴.

EN:
The technical stack was complete, but **real-world profitability validation revealed fundamental limits**.
- In-sample: model converged, accuracy metrics looked promising
- Out-of-sample: prediction accuracy dropped to near-random levels
- Root cause analysis:
  1. **Non-stationarity**: Financial time series change statistical properties over time; past patterns don't repeat reliably.
  2. **Overfitting**: Despite 72 features and 7GB of data, the model memorized historical noise as signal.
  3. **Market efficiency**: Simple exploitable price patterns are already arbitraged away by other participants.

---

### 전환 (Pivot)

KO:
"미래 가격의 방향을 예측"하는 것 자체가 근본적으로 불안정한 목표라는 결론.
방향을 바꿔 **"현재 시장이 어떤 상태(regime)인가"를 분류**하는 접근으로 전환:

| 이전 접근 | 현재 접근 |
|---|---|
| 미래 가격 예측 (Price Prediction) | 현재 레짐 분류 (Regime Classification) |
| 절대적 방향 예측 | 확률적 상태 식별 |
| LSTM 시퀀스 예측 | KMeans 클러스터링 + 규칙 기반 앙상블 |
| 단일 모델 (BTC 중심) | 레짐별 차별화된 신호 + 리스크 파라미터 |

이 전환이 현재 세 개 시스템(Aggressive/Adaptive/TrendFollowing)의 설계 철학이 됨.

EN:
Concluded that predicting future price direction is a fundamentally unstable objective.
Pivoted to **classifying the current market regime** instead:

| Previous Approach | Current Approach |
|---|---|
| Price Prediction | Regime Classification |
| Absolute direction forecast | Probabilistic state identification |
| LSTM sequence prediction | KMeans clustering + rule-based ensemble |
| Single model (BTC-focused) | Regime-specific signals + risk parameters |

This pivot became the core design philosophy of the current three-system architecture
(Aggressive / Adaptive / TrendFollowing).

---

### 배운 것 (Learnings) / Learnings

KO:
1. **파이프라인 완성 ≠ 전략 타당성**: 데이터 수집, 피처 엔지니어링, 모델 학습, 실시간 추론까지 모두 구현했지만, 기술적 완성도와 전략적 수익성은 독립적인 문제.
2. **Triple Barrier 라벨링의 한계**: Lopez de Prado 방법론을 적용했음에도 out-of-sample 성능이 in-sample을 따라가지 못함. 라벨링 방식이 정교해도 기저 신호(underlying signal)가 약하면 무의미.
3. **금융 ML의 핵심 질문**: "무엇을 예측할 것인가"가 "어떻게 예측할 것인가"보다 중요. 가격 방향 대신 레짐을 예측 대상으로 바꾼 것이 아키텍처 전체를 바꿈.
4. **엔지니어링 역량의 축적**: 데이터 파이프라인, 피처 엔진, 메모리맵 학습, 실시간 추론 브릿지 등 현재 시스템의 인프라 설계에 직접 활용됨.

EN:
1. **Pipeline completeness ≠ strategy validity**: Built the full stack (data → features → training → live inference) but found that engineering quality and strategic profitability are independent problems.
2. **Limits of Triple Barrier labeling**: Even applying Lopez de Prado's methodology, out-of-sample performance failed to match in-sample. Sophisticated labeling doesn't compensate for a weak underlying signal.
3. **The core question in financial ML**: *What* to predict matters more than *how* to predict. Changing the prediction target from price direction to market regime restructured the entire architecture.
4. **Engineering foundation carried forward**: The data pipeline, feature engine, memory-mapped training, and live inference bridge designs directly informed the infrastructure of the current system.

---

*이 로그는 GitHub 업로드 시 레포 루트에 배치 예정.*
*민감 정보(API 키, 실제 전략 파라미터 수치)는 포함하지 않음.*

*This log will be placed at the repository root upon GitHub upload.*
*No sensitive information (API keys, actual strategy parameter values) is included.*
