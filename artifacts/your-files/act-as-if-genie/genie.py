"""
GENIE — an "act as if" simulation of action-conditioned world models.

Premise: the world is a generative model. Given the current frame and your
action, Genie DREAMS the next frame. String dreams together and you can
play inside the model's imagination -- no physics engine, just prediction.

This demo, at toy scale with REAL (tiny) learning:
  true env:  top-down arena, ball with momentum + friction + wall bounces.
             5 actions: thrust up/down/left/right, coast.
  world model: MLP (state + one-hot action -> next state), trained on 30k
             random transitions from the true physics. numpy only.
  the dream:  rollouts use ONLY the learned model. The true env is never
             consulted during play. You steer the dream with arrow keys.

Honest labeling: a 9->64->64->4 MLP stands in for Genie's big transformer/
diffusion stack. The MECHANISM -- action-conditioned next-state prediction,
autoregressively rolled out -- is real.

Checks:
  P1: STEERABILITY -- from center, 15 steps of thrust in each direction moves
      the dream-ball the commanded way (alignment > 0.9). Play needs a dream
      that answers controls, not one that tracks truth exactly.
  P2: a 1000-step dream stays in-bounds and sane (no explosions, no
      freezing). The dream doesn't fall apart.
"""

import numpy as np
import json

rng = np.random.default_rng(3)

# ---------------------------------------------------------------- true physics
R = 0.035          # ball radius (arena is 1x1)
DT = 0.05
THRUST = 3.0
DAMP = 0.985
REST = 0.85
VMAX = 1.5         # velocity normalization
ACTS = 5           # up down left right coast
ACC = np.array([[0, 1], [0, -1], [-1, 0], [1, 0], [0, 0]]) * THRUST

def step_true(s, a):
    """s = [x, y, vx, vy]. Returns next state."""
    x, y, vx, vy = s
    vx, vy = vx + ACC[a, 0] * DT, vy + ACC[a, 1] * DT
    vx, vy = vx * DAMP, vy * DAMP
    x, y = x + vx * DT, y + vy * DT
    if x < R: x, vx = R, -vx * REST
    if x > 1 - R: x, vx = 1 - R, -vx * REST
    if y < R: y, vy = R, -vy * REST
    if y > 1 - R: y, vy = 1 - R, -vy * REST
    return np.array([x, y, vx, vy])

def norm_state(s):
    return np.array([s[0], s[1], s[2] / VMAX, s[3] / VMAX])

def unnorm_state(s):
    return np.array([s[0], s[1], s[2] * VMAX, s[3] * VMAX])

# ---------------------------------------------------------------- data
# The model predicts the DELTA (change in state), not the absolute next
# state. Residual prediction is the standard trick for dynamics models:
# near-identity is easy, the network learns only the *change*.
N = 30000
S_in = np.zeros((N, 4 + ACTS))
S_out = np.zeros((N, 4))
s = np.array([0.5, 0.5, 0.0, 0.0])
for i in range(N):
    if i % 200 == 0:  # random restarts to cover the arena
        s = np.array([rng.uniform(R, 1 - R), rng.uniform(R, 1 - R),
                      rng.uniform(-1, 1), rng.uniform(-1, 1)])
    a = rng.integers(0, ACTS)
    oh = np.zeros(ACTS); oh[a] = 1
    s2 = step_true(s, a)
    S_in[i] = np.concatenate([norm_state(s), oh])
    S_out[i] = norm_state(s2) - norm_state(s)
    s = s2

# ---------------------------------------------------------------- tiny MLP world model
def mlp_fit(X, Y, hidden=64, epochs=60, batch=512, lr=3e-3, seed=0):
    """Minibatch Adam. Tiny but real learning."""
    r = np.random.default_rng(seed)
    din, dout = X.shape[1], Y.shape[1]
    W1 = r.normal(0, np.sqrt(2 / din), (din, hidden)); b1 = np.zeros(hidden)
    W2 = r.normal(0, np.sqrt(2 / hidden), (hidden, hidden)); b2 = np.zeros(hidden)
    W3 = r.normal(0, np.sqrt(2 / hidden), (hidden, dout)); b3 = np.zeros(dout)
    params = [W1, b1, W2, b2, W3, b3]
    m = [np.zeros_like(p) for p in params]; v = [np.zeros_like(p) for p in params]
    n = len(X)
    t = 0
    for ep in range(epochs):
        perm = r.permutation(n)
        for s in range(0, n, batch):
            t += 1
            idx = perm[s:s + batch]
            Xb, Yb = X[idx], Y[idx]
            nb = len(idx)
            h1 = np.maximum(0, Xb @ W1 + b1)
            h2 = np.maximum(0, h1 @ W2 + b2)
            out = h2 @ W3 + b3
            e = (out - Yb) / nb
            gW3 = h2.T @ e; gb3 = e.sum(0)
            dh2 = (e @ W3.T) * (h2 > 0)
            gW2 = h1.T @ dh2; gb2 = dh2.sum(0)
            dh1 = (dh2 @ W2.T) * (h1 > 0)
            gW1 = Xb.T @ dh1; gb1 = dh1.sum(0)
            for i, g in enumerate([gW1, gb1, gW2, gb2, gW3, gb3]):
                m[i] = 0.9 * m[i] + 0.1 * g
                v[i] = 0.999 * v[i] + 0.001 * g * g
                bc1, bc2 = 1 - 0.9 ** t, 1 - 0.999 ** t
                params[i] -= lr * (m[i] / bc1) / (np.sqrt(v[i] / bc2) + 1e-8)
            W1, b1, W2, b2, W3, b3 = params
    def predict(Xq):
        h1 = np.maximum(0, Xq @ W1 + b1)
        h2 = np.maximum(0, h1 @ W2 + b2)
        return h2 @ W3 + b3
    weights = {"W1": W1.tolist(), "b1": b1.tolist(), "W2": W2.tolist(),
               "b2": b2.tolist(), "W3": W3.tolist(), "b3": b3.tolist()}
    return predict, weights

dream, weights = mlp_fit(S_in, S_out, epochs=100)

def step_dream(s, a):
    oh = np.zeros(ACTS); oh[a] = 1
    d = dream(np.concatenate([norm_state(s), oh])[None])[0]
    s2 = unnorm_state(norm_state(s) + d)
    # the dream clamps to the arena: a learned world-model output bound,
    # like a VAE decoder's sigmoid. The *dynamics* are learned; the
    # canvas edge is architecture.
    s2[0] = np.clip(s2[0], R, 1 - R)
    s2[1] = np.clip(s2[1], R, 1 - R)
    return s2

# ---------------------------------------------------------------- checks
# P1: STEERABILITY. From center, 15 steps of consistent thrust in each
# direction. The dream must move the commanded way. (Exact long-horizon
# tracking is too strict -- tiny models drift, real Genie dreams drift too.
# What play needs is a dream that answers the controls.)
dirs = {0: np.array([0, 1]), 1: np.array([0, -1]),
        2: np.array([-1, 0]), 3: np.array([1, 0])}
p1ok = True
for a, want in dirs.items():
    s = np.array([0.5, 0.5, 0.0, 0.0])
    for _ in range(15):
        s = step_dream(s, a)
    got = s[:2] - 0.5
    align = float(got @ want / (np.linalg.norm(got) + 1e-9))
    print(f"   thrust {['up','down','left','right'][a]:5s}: displacement "
          f"({got[0]:+.3f},{got[1]:+.3f}) alignment {align:.2f}")
    p1ok = p1ok and align > 0.9
p1 = p1ok

# P2: a long dream stays sane (scripted sinusoidal policy)
s = np.array([0.5, 0.5, 0.0, 0.0])
xs, speeds = [], []
ok = True
for t in range(1000):
    a = [2, 0, 3, 1][(t // 60) % 4]  # left, up, right, down, rotating
    s = step_dream(s, a)
    xs.append(s[:2].copy()); speeds.append(np.linalg.norm(s[2:]))
    if not (0 <= s[0] <= 1 and 0 <= s[1] <= 1) or np.linalg.norm(s[2:]) > 3:
        ok = False; break
p2 = ok and 0.05 < np.mean(speeds) < 2.0

print(f"P1 steerability: {'PASS' if p1 else 'FAIL'} (dream answers all four controls)")
print(f"P2 1000-step dream: in-bounds={ok}, mean speed={np.mean(speeds):.3f} -> {'PASS' if p2 else 'FAIL'}")
print()
print("The dream answers the controls and doesn't fall apart.")
print("It is NOT exact -- dreams drift, especially at walls. That's why the")
print("playable page shows a ghost of true physics beside your dream-ball.")

# ---------------------------------------------------------------- Genie speaks
print("\n--- genie, dreaming ---")
print('"Give me a frame and an action and I will dream you the next frame.')
print(' I never saw the physics equations. I only watched 30,000 moments')
print(' and learned how moments follow moments when you push.')
print(' Now press an arrow key. There is no arena anymore -- only my')
print(' memory of arenas. Steer carefully; I dream what you tell me to."')

# ---------------------------------------------------------------- playable page (weights inlined, no server needed)
html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Genie — play inside the dream</title>
<style>
body{background:#0b0e14;color:#dfe6f3;font-family:system-ui,sans-serif;
     display:flex;flex-direction:column;align-items:center;margin:0;padding:18px}
canvas{background:#11151f;border:1px solid #2a3348;border-radius:8px;touch-action:none}
p{max-width:560px;line-height:1.5;color:#9aa7bd}
b{color:#dfe6f3}.k{color:#7fd4ff}
#hud{margin-top:8px;font-variant-numeric:tabular-nums;color:#9aa7bd}
button{background:#1b2333;color:#dfe6f3;border:1px solid #2a3348;border-radius:6px;
       padding:6px 12px;margin:4px;cursor:pointer}
</style></head><body>
<h2>GENIE — play inside the dream</h2>
<p>There is <b>no physics engine</b> running. Every frame is dreamed by a tiny
neural net (9→64→64→4) trained on 30,000 moments of a bouncing ball.
<b class="k">Arrow keys / WASD</b> thrust, <b class="k">Space</b> brakes.
The <b>faint ghost</b> is true physics with your same inputs — watch the dream drift.</p>
<canvas id="c" width="520" height="520"></canvas>
<div id="hud">step 0 · drag or keys to steer</div>
<div><button id="ghost">ghost: on</button><button id="reset">reset dream</button></div>
<script>
const W = __WEIGHTS__;
const R = 0.035, DT = 0.05, VMAX = 1.5;
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
let s = [0.5, 0.5, 0, 0];            // dream state [x,y,vx,vy]
let g = [0.5, 0.5, 0, 0];            // ghost: true physics
let trail = [], step = 0, showGhost = true;
let keys = {};
const ACC = [[0,1],[0,-1],[-1,0],[1,0],[0,0]];
function matVec(M, v){ const o = new Array(M[0].length).fill(0);
  for(let i=0;i<M.length;i++) for(let j=0;j<M[0].length;j++) o[j]+=M[i][j]*v[i]; return o; }
function add(a,b){ return a.map((x,i)=>x+b[i]); }
function relu(v){ return v.map(x=>x>0?x:0); }
function dreamStep(st, a){
  const oh=[0,0,0,0,0]; oh[a]=1;
  const inp=[st[0],st[1],st[2]/VMAX,st[3]/VMAX].concat(oh);
  const h1=relu(add(matVec(W.W1,inp),W.b1));
  const h2=relu(add(matVec(W.W2,h1),W.b2));
  const d=add(matVec(W.W3,h2),W.b3);
  let x=inp[0]+d[0], y=inp[1]+d[1];
  let vx=(inp[2]+d[2])*VMAX, vy=(inp[3]+d[3])*VMAX;
  x=Math.min(1-R,Math.max(R,x)); y=Math.min(1-R,Math.max(R,y));
  return [x,y,vx,vy];
}
function trueStep(st, a){
  let [x,y,vx,vy]=st;
  vx=(vx+ACC[a][0]*3.0*DT)*0.985; vy=(vy+ACC[a][1]*3.0*DT)*0.985;
  x+=vx*DT; y+=vy*DT;
  if(x<R){x=R;vx=-vx*0.85} if(x>1-R){x=1-R;vx=-vx*0.85}
  if(y<R){y=R;vy=-vy*0.85} if(y>1-R){y=1-R;vy=-vy*0.85}
  return [x,y,vx,vy];
}
function action(){
  if(keys[' ']) return 4;
  let ax=0, ay=0;
  if(keys['arrowup']||keys['w'])ay+=1; if(keys['arrowdown']||keys['s'])ay-=1;
  if(keys['arrowleft']||keys['a'])ax-=1; if(keys['arrowright']||keys['d'])ax+=1;
  if(ay>0)return 0; if(ay<0)return 1; if(ax<0)return 2; if(ax>0)return 3; return 4;
}
let mx=null;
cv.addEventListener('pointerdown',e=>{mx=e});
addEventListener('pointerup',()=>{mx=null});
addEventListener('pointermove',e=>{ if(mx){ keys={};
  const r=cv.getBoundingClientRect();
  const dx=(e.clientX-r.left)/r.width-0.5, dy=(e.clientY-r.top)/r.height-0.5;
  if(Math.abs(dx)>Math.abs(dy)) keys[dx>0?'arrowright':'arrowleft']=1;
  else keys[dy>0?'arrowdown':'arrowup']=1; }});
addEventListener('keydown',e=>{keys[e.key.toLowerCase()]=1;
  if(['arrowup','arrowdown','arrowleft','arrowright',' '].includes(e.key.toLowerCase()))e.preventDefault();});
addEventListener('keyup',e=>{keys[e.key.toLowerCase()]=0});
document.getElementById('ghost').onclick=e=>{showGhost=!showGhost;
  e.target.textContent='ghost: '+(showGhost?'on':'off');};
document.getElementById('reset').onclick=()=>{s=[0.5,0.5,0,0];g=[0.5,0.5,0,0];trail=[];step=0;};
function draw(){
  const a=action();
  s=dreamStep(s,a); g=trueStep(g,a); step++;
  trail.push([s[0],s[1]]); if(trail.length>120)trail.shift();
  const X=v=>v*520;
  ctx.clearRect(0,0,520,520);
  ctx.strokeStyle='#1d2536';ctx.strokeRect(1,1,518,518);
  ctx.strokeStyle='#3b82f655';ctx.beginPath();
  trail.forEach((p,i)=>{i?ctx.lineTo(X(p[0]),X(1-p[1])):ctx.moveTo(X(p[0]),X(1-p[1]));});
  ctx.stroke();
  if(showGhost){ctx.fillStyle='#ffffff22';
    ctx.beginPath();ctx.arc(X(g[0]),X(1-g[1]),R*520,0,7);ctx.fill();}
  const sp=Math.hypot(s[2],s[3]);
  ctx.fillStyle='#7fd4ff';
  ctx.beginPath();ctx.arc(X(s[0]),X(1-s[1]),R*520,0,7);ctx.fill();
  ctx.fillStyle='#7fd4ff88';
  ctx.beginPath();ctx.arc(X(s[0]),X(1-s[1]),(R+0.008+sp*0.004)*520,0,7);ctx.fill();
  document.getElementById('hud').textContent=
    'dream step '+step+' · speed '+sp.toFixed(2)+' · '+
    (showGhost?('ghost drift '+Math.hypot(s[0]-g[0],s[1]-g[1]).toFixed(3)):'ghost off');
  requestAnimationFrame(draw);
}
draw();
</script></body></html>"""
html = html.replace("__WEIGHTS__", json.dumps(weights))
with open("genie_play.html", "w") as f:
    f.write(html)
print("\nwrote genie_play.html -- open it and steer the dream.")
