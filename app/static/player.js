(function () {
  const P = window.PAYLOAD;
  const root = document.getElementById('player');
  const answers = {};
  const answeredFns = {};

  function h(tag, attrs, ...kids) {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (k === 'class') el.className = v;
      else if (k.startsWith('on')) el.addEventListener(k.slice(2), v);
      else if (v === true) el.setAttribute(k, '');
      else if (v !== false && v != null) el.setAttribute(k, v);
    }
    for (const kid of kids.flat()) if (kid != null) el.append(kid.nodeType ? kid : document.createTextNode(kid));
    return el;
  }
  const changed = () => updateProgress();

  // ---------- renderers ----------
  const R = {};

  R.fill = R.dropdown = (it, body) => {
    const vals = [];
    const passage = h('div', { class: 'passage' });
    it.parts.forEach(p => {
      if (p.t != null) { passage.append(p.t); return; }
      vals[p.b] = '';
      let input;
      if (it.type === 'fill') {
        input = h('input', { class: 'blank', type: 'text', size: p.size, autocomplete: 'off', autocapitalize: 'none', spellcheck: 'false',
          'aria-label': 'Lacuna ' + (p.b + 1), oninput: e => { vals[p.b] = e.target.value; changed(); } });
      } else {
        input = h('select', { class: 'blank', 'aria-label': 'Opção ' + (p.b + 1), onchange: e => { vals[p.b] = e.target.value; changed(); } },
          h('option', { value: '' }, '▾'), p.options.map(o => h('option', { value: o }, o)));
      }
      passage.append(input);
    });
    answers[it.id] = vals;
    answeredFns[it.id] = () => vals.length > 0 && vals.every(v => String(v).trim() !== '');
    body.append(passage);
  };

  R.choice = (it, body) => {
    answers[it.id] = null;
    const box = h('div', { class: 'options' });
    it.options.forEach((o, i) => {
      const lab = h('label', { class: 'option' },
        h('input', { type: 'radio', name: 'q_' + it.id, onchange: () => {
          answers[it.id] = i;
          box.querySelectorAll('.option').forEach(x => x.classList.remove('sel'));
          lab.classList.add('sel');
          changed();
        } }), o);
      box.append(lab);
    });
    answeredFns[it.id] = () => answers[it.id] !== null;
    body.append(box);
  };

  R.truefalse = (it, body) => {
    const vals = it.statements.map(() => null);
    answers[it.id] = vals;
    it.statements.forEach((s, i) => {
      const t = h('button', { type: 'button', class: 't' }, 'True');
      const f = h('button', { type: 'button', class: 'f' }, 'False');
      const set = v => { vals[i] = v; t.classList.toggle('on', v === true); f.classList.toggle('on', v === false); changed(); };
      t.onclick = () => set(true);
      f.onclick = () => set(false);
      const tr = (it.statement_translations || [])[i];
      body.append(h('div', { class: 'tf-row' },
        h('span', {}, `${String.fromCharCode(97 + i)}) ${s}`, tr ? h('small', { class: 'tf-tr' }, tr) : null),
        h('span', { class: 'seg' }, t, f)));
    });
    answeredFns[it.id] = () => vals.every(v => v !== null);
  };

  R.order = (it, body) => {
    const seq = [];  // indices into it.tokens
    const bank = h('div', { class: 'chips bank' });
    const line = h('div', { class: 'chips answer' });
    let dragFrom = null;
    const sync = () => { answers[it.id] = seq.map(i => it.tokens[i]); changed(); };
    const draw = () => {
      bank.replaceChildren();
      line.replaceChildren();
      it.tokens.forEach((tok, i) => {
        if (seq.includes(i)) return;
        bank.append(h('span', { class: 'chip', draggable: 'true', ondragstart: () => { dragFrom = { bank: i }; },
          onclick: () => { seq.push(i); draw(); sync(); } }, tok));
      });
      if (!seq.length) line.append(h('span', { class: 'placeholder' }, 'Clique ou arraste as palavras para montar a frase aqui'));
      seq.forEach((ti, pos) => {
        const chip = h('span', { class: 'chip', draggable: 'true', title: 'Clique para devolver · arraste para reordenar',
          ondragstart: e => { dragFrom = { pos }; chip.classList.add('dragging'); },
          ondragend: () => chip.classList.remove('dragging'),
          ondragover: e => e.preventDefault(),
          ondrop: e => { e.preventDefault(); e.stopPropagation(); dropAt(pos); },
          onclick: () => { seq.splice(pos, 1); draw(); sync(); } }, it.tokens[ti]);
        line.append(chip);
      });
    };
    const dropAt = pos => {
      if (!dragFrom) return;
      if (dragFrom.bank != null) seq.splice(pos, 0, dragFrom.bank);
      else { const [v] = seq.splice(dragFrom.pos, 1); seq.splice(pos > dragFrom.pos ? pos - 1 : pos, 0, v); }
      dragFrom = null; draw(); sync();
    };
    line.addEventListener('dragover', e => e.preventDefault());
    line.addEventListener('drop', e => { e.preventDefault(); dropAt(seq.length); });
    answers[it.id] = [];
    answeredFns[it.id] = () => seq.length === it.tokens.length;
    draw();
    body.append(line, h('div', { style: 'height:.5rem' }), bank);
  };

  const COLORS = ['#3b5bdb', '#e8590c', '#2b8a3e', '#ae3ec9', '#1098ad', '#d6336c', '#5c940d', '#f59f00'];
  // match with pictures: the words on top, a grid of pictures below; each picture shows the word linked to it
  function matchPics(it, body) {
    const links = it.left.map(() => null); // word index -> picture index
    let active = null;
    const words = it.left.map((t, i) => h('button', { type: 'button', class: 'm-item m-word', onclick: () => clickWord(i) }, t));
    const slots = it.right.map(() => h('span', { class: 'm-slot' }, '?'));
    const pics = it.right.map((t, j) => h('button', { type: 'button', class: 'm-item m-pic', onclick: () => clickPic(j) },
      h('img', { src: it.right_images[j], alt: t, loading: 'lazy' }), slots[j]));
    const sync = () => { answers[it.id] = links.map(j => j === null ? null : it.right[j]); draw(); changed(); };
    function clickWord(i) {
      if (links[i] !== null && active === null) { links[i] = null; sync(); return; }
      active = active === i ? null : i; draw();
    }
    function clickPic(j) {
      const owner = links.indexOf(j);
      if (active === null) { if (owner >= 0) { links[owner] = null; sync(); } return; }
      if (owner >= 0) links[owner] = null;
      links[active] = j; active = null; sync();
    }
    function draw() {
      words.forEach((el, i) => {
        el.classList.toggle('active', active === i);
        el.classList.toggle('linked', links[i] !== null);
        el.style.borderColor = links[i] !== null ? COLORS[i % COLORS.length] : '';
      });
      pics.forEach((el, j) => {
        const i = links.indexOf(j);
        el.classList.toggle('linked', i >= 0);
        el.style.borderColor = i >= 0 ? COLORS[i % COLORS.length] : '';
        slots[j].textContent = i >= 0 ? it.left[i] : '?';
        slots[j].style.color = i >= 0 ? COLORS[i % COLORS.length] : '';
      });
    }
    answers[it.id] = links.map(() => null);
    answeredFns[it.id] = () => links.every(j => j !== null);
    body.append(h('p', { class: 'hint', style: 'margin-top:0' }, 'Clique numa expressão e depois na figura que combina com ela. Clique de novo para desfazer.'),
      h('div', { class: 'm-words' }, words), h('div', { class: 'm-pics' }, pics));
    draw();
  }

  R.match = (it, body) => {
    if (it.right_images) return matchPics(it, body);
    const links = it.left.map(() => null); // left index -> right display index
    let active = null;
    const wrap = h('div', { class: 'match' });
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    const lcol = h('div', { class: 'm-col left' });
    const rcol = h('div', { class: 'm-col right' });
    const lEls = it.left.map((t, i) => h('div', { class: 'm-item', onclick: () => clickLeft(i) }, t, h('span', { class: 'dot' })));
    const rEls = it.right.map((t, j) => h('div', { class: 'm-item', onclick: () => clickRight(j) }, h('span', { class: 'dot' }), t));
    lcol.append(...lEls); rcol.append(...rEls);
    wrap.append(svg, lcol, rcol);
    const sync = () => { answers[it.id] = links.map(j => j === null ? null : it.right[j]); draw(); changed(); };
    function clickLeft(i) {
      if (links[i] !== null && active === null) { links[i] = null; sync(); return; }
      active = active === i ? null : i; draw();
    }
    function clickRight(j) {
      const owner = links.indexOf(j);
      if (active === null) { if (owner >= 0) { links[owner] = null; sync(); } return; }
      if (owner >= 0) links[owner] = null;
      links[active] = j; active = null; sync();
    }
    function draw() {
      lEls.forEach((el, i) => { el.classList.toggle('active', active === i); el.classList.toggle('linked', links[i] !== null); });
      rEls.forEach((el, j) => el.classList.toggle('linked', links.includes(j)));
      const box = wrap.getBoundingClientRect();
      svg.replaceChildren();
      links.forEach((j, i) => {
        if (j === null) return;
        const a = lEls[i].getBoundingClientRect(), b = rEls[j].getBoundingClientRect();
        const x1 = a.right - box.left, y1 = a.top + a.height / 2 - box.top, x2 = b.left - box.left, y2 = b.top + b.height / 2 - box.top;
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const mx = (x1 + x2) / 2;
        path.setAttribute('d', `M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}`);
        path.setAttribute('stroke', COLORS[i % COLORS.length]);
        path.setAttribute('stroke-width', '3');
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke-linecap', 'round');
        svg.append(path);
        lEls[i].querySelector('.dot').style.borderColor = COLORS[i % COLORS.length];
        rEls[j].querySelector('.dot').style.borderColor = COLORS[i % COLORS.length];
      });
      lEls.forEach((el, i) => { if (links[i] === null) el.querySelector('.dot').style.borderColor = ''; });
      rEls.forEach((el, j) => { if (!links.includes(j)) el.querySelector('.dot').style.borderColor = ''; });
    }
    window.addEventListener('resize', draw);
    answers[it.id] = links.map(() => null);
    answeredFns[it.id] = () => links.every(j => j !== null);
    body.append(h('p', { class: 'hint', style: 'margin-top:0' }, 'Clique num item da esquerda e depois no par da direita. Clique de novo para desfazer.'), wrap);
    requestAnimationFrame(draw);
  };

  R.group = (it, body) => {
    const place = it.words.map(() => null);
    let picked = null, dragging = null;
    const bank = h('div', { class: 'chips bank' });
    const zones = it.categories.map(c => h('div', { class: 'chips' }));
    const groups = h('div', { class: 'groups' }, it.categories.map((c, ci) => {
      const g = h('div', { class: 'group', onclick: () => { if (picked !== null) { place[picked] = c; picked = null; sync(); } },
        ondragover: e => { e.preventDefault(); g.classList.add('over'); }, ondragleave: () => g.classList.remove('over'),
        ondrop: e => { e.preventDefault(); g.classList.remove('over'); if (dragging !== null) { place[dragging] = c; dragging = null; sync(); } } },
        h('h4', {}, c), zones[ci]);
      return g;
    }));
    bank.addEventListener('dragover', e => e.preventDefault());
    bank.addEventListener('drop', e => { e.preventDefault(); if (dragging !== null) { place[dragging] = null; dragging = null; sync(); } });
    const sync = () => { answers[it.id] = it.words.map((w, i) => [w, place[i]]).filter(p => p[1] !== null); draw(); changed(); };
    function chip(i) {
      return h('span', { class: 'chip' + (picked === i ? ' picked' : ''), draggable: 'true',
        ondragstart: () => { dragging = i; },
        onclick: e => { e.stopPropagation();
          if (picked !== null && picked !== i && place[i] !== null) { place[picked] = place[i]; picked = null; sync(); return; }
          if (place[i] !== null) { place[i] = null; picked = null; sync(); } else { picked = picked === i ? null : i; draw(); } } }, it.words[i]);
    }
    function draw() {
      bank.replaceChildren();
      zones.forEach(z => z.replaceChildren());
      it.words.forEach((w, i) => {
        if (place[i] === null) bank.append(chip(i));
        else zones[it.categories.indexOf(place[i])].append(chip(i));
      });
      if (!bank.children.length) bank.append(h('span', { class: 'placeholder' }, 'Todas as palavras foram classificadas ✓'));
    }
    answers[it.id] = [];
    answeredFns[it.id] = () => place.every(p => p !== null);
    body.append(h('p', { class: 'hint', style: 'margin-top:0' }, 'Clique numa palavra e depois no grupo (ou arraste). Clique numa palavra já colocada para devolvê-la.'), bank, groups);
    draw();
  };

  R.free = (it, body) => {
    const count = h('div', { class: 'wordcount' });
    const upd = v => {
      const n = (v.match(/[A-Za-zÀ-ÿ']+/g) || []).length;
      count.textContent = `${n} palavra(s)` + (it.min_words ? ` · mínimo ${it.min_words}` : '');
    };
    const ta = h('textarea', { rows: 6, placeholder: 'Write your answer here…', spellcheck: 'false',
      oninput: e => { answers[it.id] = e.target.value; upd(e.target.value); changed(); } });
    answers[it.id] = '';
    answeredFns[it.id] = () => String(answers[it.id]).trim().length > 0;
    upd('');
    body.append(ta, count);
  };

  R.info = (it, body) => {
    if (it.text) body.append(h('div', { class: 'reading' }, it.text));
    answers[it.id] = null;
  };

  // speaking: listen to the model, record your voice, play it back; optional check with the browser's speech recognition
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  const canRecord = !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia && window.MediaRecorder);
  let micStream = null, stopCurrent = null;
  const simplify = s => String(s).toLowerCase().replace(/[’‘`´]/g, "'").replace(/[^a-z0-9' ]+/g, ' ').replace(/\s+/g, ' ').trim();

  R.speak = (it, body) => {
    const vals = it.phrases.map(() => ({ recorded: false, heard: '' }));
    answers[it.id] = vals;
    answeredFns[it.id] = () => vals.every(v => v.recorded);
    if (!canRecord) body.append(h('p', { class: 'hint warnbox' }, '⚠ Seu navegador não permite gravar a voz. Pratique falando em voz alta e marque cada frase como feita.'));
    it.phrases.forEach((p, i) => {
      const status = h('span', { class: 'speak-status' });
      const mine = h('audio', { controls: true, hidden: true });
      const model = p.audio ? h('audio', { src: p.audio, preload: 'none' }) : null;
      const listenBtn = model ? h('button', { type: 'button', class: 'btn small', onclick: () => { model.currentTime = 0; model.play(); } }, '🔊 Ouvir') : null;
      const recBtn = h('button', { type: 'button', class: 'btn small primary' }, canRecord ? '🎙 Gravar' : '✓ Já falei');
      const heard = h('div', { class: 'speak-heard', hidden: true });
      const done = () => { vals[i].recorded = true; row.classList.add('done'); changed(); };

      recBtn.onclick = async () => {
        if (!canRecord) { done(); status.textContent = '✓ feito'; return; }
        if (stopCurrent) { stopCurrent(); return; }
        try {
          micStream = micStream || await navigator.mediaDevices.getUserMedia({ audio: true });
        } catch (e) {
          status.textContent = '⚠ Microfone bloqueado. Libere o microfone no navegador e tente de novo.';
          return;
        }
        const chunks = [];
        const rec = new MediaRecorder(micStream);
        rec.ondataavailable = e => { if (e.data.size) chunks.push(e.data); };
        rec.onstop = () => {
          stopCurrent = null;
          recBtn.textContent = '🎙 Gravar de novo';
          recBtn.classList.remove('rec');
          mine.src = URL.createObjectURL(new Blob(chunks, { type: rec.mimeType || 'audio/webm' }));
          mine.hidden = false;
          status.textContent = '✓ gravado — ouça e compare com o modelo';
          done();
        };
        const timer = setTimeout(() => rec.state === 'recording' && rec.stop(), 20000);
        stopCurrent = () => { clearTimeout(timer); if (rec.state === 'recording') rec.stop(); };
        rec.start();
        recBtn.textContent = '⏹ Parar';
        recBtn.classList.add('rec');
        status.textContent = '● gravando… fale agora';
      };

      let checkBtn = null;
      if (SR) {
        checkBtn = h('button', { type: 'button', class: 'btn small', title: 'O navegador tenta reconhecer o que você falou' }, '🗣 Verificar pronúncia');
        checkBtn.onclick = () => {
          const r = new SR();
          r.lang = 'en-US'; r.interimResults = false; r.maxAlternatives = 5;
          checkBtn.disabled = true; checkBtn.textContent = '👂 Ouvindo… fale agora';
          r.onresult = e => {
            const alts = [...e.results[0]].map(a => a.transcript);
            const ok = alts.some(a => simplify(a) === simplify(p.text));
            vals[i].heard = ok ? p.text : alts[0];
            heard.hidden = false;
            heard.className = 'speak-heard ' + (ok ? 'ok' : 'bad');
            heard.textContent = ok ? `✓ Perfeito! Entendemos: “${p.text}”` : `Entendemos: “${alts[0]}”. Tente de novo, falando com calma.`;
            changed();
          };
          r.onerror = () => { heard.hidden = false; heard.className = 'speak-heard'; heard.textContent = 'Não consegui ouvir. Verifique o microfone e tente de novo.'; };
          r.onend = () => { checkBtn.disabled = false; checkBtn.textContent = '🗣 Verificar pronúncia'; };
          r.start();
        };
      }
      const row = h('div', { class: 'speak-row' },
        h('div', { class: 'speak-text' }, `${it.phrases.length > 1 ? (i + 1) + '. ' : ''}${p.text}`),
        h('div', { class: 'row' }, listenBtn, recBtn, checkBtn, status), model, mine, heard);
      body.append(row);
    });
  };

  // interactive video: the video pauses at each stop and shows a multiple-choice question
  const fmtTime = t => `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, '0')}`;
  R.video = (it, body) => {
    const vals = it.stops.map(() => null);
    answers[it.id] = vals;
    answeredFns[it.id] = () => vals.every(v => v !== null);
    const shown = it.stops.map(() => false);
    const video = h('video', { class: 'q-video', src: it.video, playsinline: true, 'webkit-playsinline': true, preload: 'metadata',
      controls: true, controlsList: 'nofullscreen nodownload', disablePictureInPicture: true, poster: it.poster || null });
    let track = null;
    if (it.subtitles) {
      track = h('track', { kind: 'subtitles', srclang: 'en', label: 'English', src: it.subtitles });
      video.append(track);
    }
    const overlay = h('div', { class: 'v-overlay', hidden: true });
    const stage = h('div', { class: 'v-stage' }, video, overlay);
    const list = h('ol', { class: 'v-list' });
    let current = null;

    const exitFs = () => {
      if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
      if (video.webkitDisplayingFullscreen) video.webkitExitFullscreen();
    };
    function ask(i) {
      current = i; shown[i] = true;
      video.pause(); exitFs();
      const s = it.stops[i];
      const go = h('button', { type: 'button', class: 'btn primary', disabled: vals[i] === null,
        onclick: () => { overlay.hidden = true; current = null; drawList(); video.play().catch(() => {}); } }, 'Continuar o vídeo ▶');
      const opts = s.options.map((o, oi) => h('button', { type: 'button', class: 'v-opt' + (vals[i] === oi ? ' sel' : ''),
        onclick: () => { vals[i] = oi; opts.forEach((b, bi) => b.classList.toggle('sel', bi === oi)); go.disabled = false; changed(); drawList(); } }, o));
      overlay.replaceChildren(h('div', { class: 'v-card' },
        h('div', { class: 'v-q' }, `⏸ ${i + 1}/${it.stops.length} · ${s.question}`),
        s.translation ? h('div', { class: 'q-translation' }, s.translation) : null,
        h('div', { class: 'v-opts' }, opts), h('div', { class: 'row', style: 'justify-content:flex-end' }, go)));
      overlay.hidden = false;
      drawList();
    }
    video.addEventListener('timeupdate', () => {
      if (current !== null) { if (!video.paused) video.pause(); return; }
      const t = video.currentTime;
      // also catches a student who drags the bar past a pause
      const i = it.stops.findIndex((s, si) => !shown[si] && t >= s.at);
      if (i >= 0) ask(i);
    });
    video.addEventListener('play', () => { if (current !== null) video.pause(); });
    function drawList() {
      list.replaceChildren(...it.stops.map((s, i) => h('li', { class: vals[i] !== null ? 'done' : '' },
        h('button', { type: 'button', class: 'linklike', disabled: !shown[i],
          title: shown[i] ? 'Rever esta pergunta' : 'Assista ao vídeo até esta pausa',
          onclick: () => { video.currentTime = Math.max(0, s.at - 0.05); ask(i); } },
          `${fmtTime(s.at)} — ${shown[i] ? s.question : 'pergunta ' + (i + 1) + ' (aparece durante o vídeo)'}`),
        vals[i] !== null ? h('span', { class: 'mark ok' }, ' ✓ respondida') : null)));
    }
    const ccBtn = track ? h('button', { type: 'button', class: 'btn small', onclick: () => {
      const tt = video.textTracks[0]; if (!tt) return;
      tt.mode = tt.mode === 'showing' ? 'hidden' : 'showing';
      ccBtn.textContent = tt.mode === 'showing' ? '💬 Legenda: ligada' : '💬 Legenda: desligada';
    } }, '💬 Legenda: desligada') : null;
    const again = h('button', { type: 'button', class: 'btn small', onclick: () => { video.currentTime = 0; video.play().catch(() => {}); } }, '↺ Assistir do início');
    body.append(h('p', { class: 'hint', style: 'margin-top:0' },
      'Aperte ▶ e assista. O vídeo vai pausar sozinho para você responder; depois clique em "Continuar o vídeo". ' +
      'Dica: assista primeiro sem legenda e, se precisar, ligue a legenda.'),
      stage, h('div', { class: 'row', style: 'margin:.5rem 0' }, ccBtn, again), list);
    drawList();
  };

  // ---------- build ----------
  let qn = 0;
  const graded = P.items.filter(it => it.type !== 'info');
  P.items.forEach(it => {
    const body = h('div');
    const info = it.type === 'info';
    const card = h('section', { class: 'card q' + (info ? ' info' : ''), id: 'q_' + it.id },
      h('div', { class: 'q-head' },
        info ? h('div', { class: 'q-num info' }, '📖') : h('div', { class: 'q-num' }, String(++qn)),
        h('div', { style: 'flex:1' }, it.prompt ? h('div', { class: 'q-prompt' }, it.prompt) : null,
          it.translation ? h('div', { class: 'q-translation' }, it.translation) : null,
          info ? null : h('div', { class: 'q-type' }, `${it.points} ponto(s)`))),
      it.example ? h('div', { class: 'q-example' }, h('b', {}, 'Example · Exemplo: '), it.example) : null,
      it.image ? h('img', { class: 'q-img', src: it.image, alt: '', loading: 'lazy', referrerpolicy: 'no-referrer' }) : null,
      it.audio ? h('audio', { class: 'q-audio', src: it.audio, controls: true, preload: 'none' }) : null,
      body);
    root.append(card);
    R[it.type](it, body);
  });

  function updateProgress() {
    const done = graded.filter(it => answeredFns[it.id]()).length;
    document.getElementById('progress').textContent = `${done} de ${graded.length} questões respondidas`;
    document.getElementById('submitMsg').textContent = '';
    confirmArmed = false;
    return done;
  }

  let confirmArmed = false, sending = false;
  const btn = document.getElementById('submitBtn');
  btn.addEventListener('click', async () => {
    if (sending) return;
    if (stopCurrent) stopCurrent();
    const done = graded.filter(it => answeredFns[it.id]()).length;
    const msg = document.getElementById('submitMsg');
    if (done < graded.length && !confirmArmed) {
      msg.textContent = `⚠ ${graded.length - done} questão(ões) incompleta(s). Clique de novo para enviar mesmo assim.`;
      msg.style.color = '#9a6200';
      confirmArmed = true;
      const first = graded.find(it => !answeredFns[it.id]());
      if (first) document.getElementById('q_' + first.id).scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }
    sending = true;
    btn.disabled = true;
    btn.textContent = 'Enviando…';
    try {
      const r = await fetch(P.submitUrl, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ answers }) });
      const data = await r.json().catch(() => ({}));
      if (!r.ok || !data.redirect) throw new Error(data.error || 'Não foi possível enviar. Verifique sua conexão e tente de novo.');
      window.location = data.redirect;
    } catch (e) {
      msg.textContent = e.message;
      msg.style.color = 'var(--bad)';
      sending = false;
      btn.disabled = false;
      btn.textContent = 'Enviar respostas ✓';
    }
  });
  updateProgress();
})();
