# Art Project — Technical Stack Spec
*Vesper side chat, 2026-10-10. Living document; prices verified Oct 2026 and volatile (AI memory boom).*

## 0. The loop (what we're building)

Per robot, two timescales:

- **Fast (10–50 Hz):** sense → carve (self-built latent representation) → act (policy + logistic-map exploration with learnable r).
- **Slow (minutes):** measure audience attention → bandit update over behavior-modes → update the chaos dial r and the attention model.
- **Offline (nightly):** replay consolidation ("dreaming") — the carve digests the day.

No foundation model in the loop. No cloud. The learning *is* the performance.

## 1. Compute — one brain per robot

Conceptual call: each robot gets its own computer. Separate bodies, separate brains, no shared server. (A central server would be cheaper and would quietly falsify the "three minds" premise.)

| Option | What | Price (Oct 2026) | Verdict |
|---|---|---|---|
| Jetson Orin Nano Super dev kit | 8 GB, 67 INT8 TOPS, 15 W | **$399 list** (NVIDIA raised it from $249 in ~July 2026; street $280–550) | Default. Runs perception + learning on one board. |
| Raspberry Pi 5 8 GB + Hailo AI kit | CPU + 13–26 TOPS TPU | Pi 5 8 GB ~$95 list but rising fast (memory crisis); Hailo kit ~$70 | Budget fallback. Fine for perception + small-MLP RL. Tighter headroom. |
| Jetson Orin NX 16 GB module | 100 TOPS | $999/1KU (module only, needs carrier) | Only if we later add a VLM commentator. Overkill today. |

3 robots × Orin Nano Super ≈ **$1,200** at list. Prices are moving monthly — re-check before buying.

## 2. Perception pipeline — the attention measurement

This is the load-bearing wall. Prototype it *first*, on a laptop webcam, before any robot exists.

**Sensors per room:**
- 1× overhead camera (USB3, 1080p, wide angle; ~$40–80, e.g. ELP modules) → person detection + tracking → position, dwell, trajectories.
- 1× frontal camera (same class) → head pose → facing-toward-robot or not.
- Optional: mic array (~$30–60) for social audio (laughter, exclamations); floor IR beams for ground-truth counts.

**Software (all edge, no cloud):**
- Detection + tracking: Ultralytics YOLOv8/YOLO11 pose **(license flag: AGPL-3.0** — fine for a gallery piece you don't distribute as software, but know it; Apache-2.0 alternatives: RTMPose/RTMDet via OpenMMLab).
- Head orientation: MediaPipe (Apache-2.0), lightweight, CPU-friendly. (6DRepNet if MediaPipe's pose is too coarse.)
- Motion energy: OpenCV optical flow (no model needed) → per-person stillness.
- Proximity: floor-plane homography from the overhead camera (calibrate once with a checkerboard) — no depth camera needed. (Intel RealSense D435 ~$200–350 if we want real depth later.)

**The composite (per 10 s window):**
`A = w1·dwell + w2·oriented + w3·stillness + w4·proximity + w5·social − w6·phone_up`,
normalized by occupancy baseline. **Don't fix the weights** — let each robot learn which kind of attention to value (the score itself is learned).

**Calibration experiment (do this before building robots):** record test footage, get human "how interesting was this" ratings, check the composite tracks them. Ungrounded metric = the robot optimizes a number nobody validated.

**Privacy (non-negotiable for a public piece):** edge processing only, pose skeletons never faces, no raw video stored, clear signage, visible attention meter (legibility = consent; the Hawthorne effect becomes part of the piece).

## 3. Learning & control stack

| Piece | Choice | License | Notes |
|---|---|---|---|
| Deep learning | PyTorch | BSD | Small nets only; nothing big. |
| RL scaffolding | **CleanRL** (single-file, MIT) | MIT | Pick over Stable-Baselines3: our two-timescale custom loop fights SB3's abstractions; CleanRL is hackable. |
| Self-built carve | Tiny MLP autoencoder → latent dynamics (world-model-lite) over the robot's own sensor vector | — | The floor constructs itself. Start MLP; graduate only if needed. |
| Chaos dial | NumPy logistic map `x←r·x(1−x)`, **r learnable** by the slow loop | — | r < ~3.57 order → r ≈ 3.5699 edge → r → 4 chaos. Kelly's measured δ = 4.669198… is the dial's calibration. |
| Slow loop | Contextual bandit over behavior-modes, reward = attention composite | — | Minutes timescale; this is where "learning to hold a gaze" lives. |
| Fast loop | TD / small actor-critic on intrinsic curiosity (prediction error) | — | Seconds timescale; the starter motor before attention takes over. |
| Middleware | Python + ZeroMQ pub/sub | — | Honest call: ROS 2 (Apache-2.0) is the robotics standard but heavyweight; for 3 robots on an art timeline, ZeroMQ is enough. Graduate to ROS 2 only if integration pain demands it. |
| Logging | SQLite / Parquet, everything | — | The logs are part of the piece (receipts; also the "dream" replay source). |

## 4. Robot bodies

Tiers, prototype → gallery:

- **Prototype:** off-the-shelf edu base (iRobot Create 3 / TurtleBot-class, ~$300–600 street — verify, product lines are churning) + servo squeegee arm (~$50 parts) + the fluid (colored water + cellulose ether, as the original — cheap, safe, nontoxic).
- **Gallery:** custom mecanum-wheel base (strafe + spin = it can *dance*; ~$200–400 parts) + 3D-printed arm + Dynamixel XL330 servos (~$25 each) or MG996R (~$10).
- **Honest note:** the original used a KUKA industrial arm ($$$$). We don't want one — a mobile base is *better* for this concept (roaming, approaching the audience, holding a gaze by moving closer).
- **Safety (public = liability):** e-stop buttons, hard speed caps, soft bumpers, supervised or bounded floor area. Design this in from day one, not as an afterthought.

## 5. Power & five-day ops

Five days continuous is an *operations* problem, not an AI problem:

- Batteries won't last — plan tethered power or a charging dock + scheduled sleep cycles from the start.
- Precedent: the original *Can't Help Myself* was powered off nightly by museum staff. We can do better: make the offline hours part of the piece — the robot "sleeps" and runs replay consolidation ("dreaming"). The carve digests the day without witnesses.
- Thermal: a Jetson in an enclosed plinth needs airflow. Boring, load-bearing.

## 6. Budget sketch (3 robots)

| Item | Prototype (1 robot) | Gallery (3 robots) |
|---|---|---|
| Compute (Orin Nano Super × n) | $400 | $1,200 |
| Bases + arms + servos | $400–600 | $1,200–1,800 |
| Cameras (2/room) + mics | $150 | $400–500 |
| Power, networking, cabling, mounts | $100 | $300 |
| Fluid, printing, misc parts | $50 | $200 |
| **Total** | **~$800–1,200** | **~$3,500–5,000** |

Bases/servos/cameras marked approximate — verify at buy time. Everything is drifting with the memory shortage.

## 7. Build order (the honest sequence)

1. **Attention pipeline on a laptop webcam.** Validate the metric against human ratings. (Weekend; the one result everything stands on.)
2. **One robot, scripted behaviors, in a room.** Does the attention score actually respond to behavior differences?
3. **Slow learning loop** (bandit over behavior-modes). Does it learn to hold a gaze over days?
4. **Self-built carve** (autoencoder) + **learnable r dial**. Does the floor construct itself? Does neglect drive r toward chaos?
5. **Three robots, three rooms.** Do the floors diverge with the audiences?
6. **Gallery hardening:** safety, power/dream cycles, signage + consent, logging as artifact.

## 8. Open risks

- Attention metric validity (step 1 either grounds the piece or kills it — good).
- Goodhart: the robot discovers startle > beauty. Mitigation: reward *held* (sustained, still, oriented) over *grabbed* (spike then leave). Or don't mitigate — it's the piece. Decide deliberately.
- Audience gaming the meter (adversarial visitors). That's data, not failure.
- Hardware price volatility (2026 memory crisis). Buy compute early.
- The bootstrap problem: random carve + noisy attention early on. The curiosity starter-motor is load-bearing; don't skip it.
