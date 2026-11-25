// captions.js — one word (or a short pair) at a time, synced to the voice (STIL_KITABI §6).
// White, heavy, dark stroke + soft shadow, centred at 70 % of the height.
export function groupWords(words) {
  const out = [];
  for (let i = 0; i < words.length; i++) {
    const w = words[i], n = words[i + 1];
    const bare = w.word.replace(/[^\p{L}\p{N}]/gu, '');
    if (n && bare.length <= 3 && !/[.,:;!?"]$/.test(w.word) && (w.word + ' ' + n.word).length <= 14 && w.spk === n.spk && n.start - w.end < .25) {
      out.push({ text: w.word + ' ' + n.word, start: w.start, end: n.end, spk: w.spk, hl: w.hl || n.hl }); i++;
    } else out.push({ text: w.word, start: w.start, end: w.end, spk: w.spk, hl: w.hl });
  }
  for (let i = 0; i < out.length; i++) out[i].until = out[i + 1] ? Math.min(out[i + 1].start, out[i].end + .6) : out[i].end + .4;   // no caption over a long pause
  return out;
}

// colors + names: { speaker: '#hex' } and { speaker: 'Luna' } put the speaker's name on a pill of their colour above the
// words (dialogue episodes); hl words (the script's emphasis list) sit on a yellow patch.
export function drawCaption(g, groups, t, W, H, { font = '"Segoe UI Black", "Arial Black", sans-serif', size = 74, y = .70, colors = null, names = null, hlColor = '#ffd23f' } = {}) {
  const c = groups.find(c => t >= c.start - .02 && t < c.until);
  if (!c) return;
  const text = c.text.replace(/^"|"$/g, '').replace(/"/g, '');
  const age = t - c.start, pop = age < .07 ? 1.06 - age / .07 * .06 : 1;
  const s = size * Math.min(W, H) / 1080 * pop;
  g.save();
  g.font = `900 ${s}px ${font}`; g.textAlign = 'center'; g.textBaseline = 'middle';
  g.lineJoin = 'round'; g.miterLimit = 2;
  g.shadowColor = 'rgba(10,6,20,.55)'; g.shadowBlur = s * .18; g.shadowOffsetY = s * .06;
  g.strokeStyle = '#140c1c'; g.lineWidth = s * .2; g.strokeText(text, W / 2, H * y);
  g.shadowColor = 'transparent';
  const tw = g.measureText(text).width;
  if (c.hl) {                                   // emphasis word: dark text on a yellow felt patch (dizivanastudio style)
    g.fillStyle = hlColor; g.beginPath(); g.roundRect(W / 2 - tw / 2 - s * .18, H * y - s * .62, tw + s * .36, s * 1.16, s * .22); g.fill();
    g.fillStyle = '#1e1a28'; g.fillText(text, W / 2, H * y);
  } else { g.fillStyle = '#ffffff'; g.fillText(text, W / 2, H * y); }
  const col = colors && c.spk && colors[c.spk], who = names && c.spk && names[c.spk];
  if (col && who) {                             // the speaker's name on a pill of their colour, above the words
    const fs = s * .42; g.font = `700 ${fs}px ${font}`; const pw = g.measureText(who).width, py = H * y - s * 1.08;
    g.fillStyle = col; g.beginPath(); g.roundRect(W / 2 - pw / 2 - fs * .7, py - fs * .78, pw + fs * 1.4, fs * 1.5, fs * .75); g.fill();
    g.fillStyle = '#1e1a3c'; g.fillText(who, W / 2, py);
  }
  g.restore();
}
