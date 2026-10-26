(function () {
  const ex = window.EX;
  const TYPES = window.TYPES;
  const list = document.getElementById('items');

  function h(tag, attrs, ...kids) {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (k === 'class') el.className = v;
      else if (k.startsWith('on')) el.addEventListener(k.slice(2), v);
      else if (k === 'value') el.value = v;
      else if (v === true) el.setAttribute(k, '');
      else if (v !== false && v != null) el.setAttribute(k, v);
    }
    for (const kid of kids.flat()) if (kid != null) el.append(kid.nodeType ? kid : document.createTextNode(kid));
    return el;
  }
  const uid = () => 'i' + Math.random().toString(16).slice(2, 10);

  // ---------- meta ----------
  document.querySelectorAll('#meta [data-k]').forEach(el => {
    const k = el.dataset.k;
    if (el.type === 'checkbox') el.checked = !!ex[k];
    else el.value = ex[k] == null ? '' : (k === 'due_date' ? String(ex[k]).slice(0, 16) : ex[k]);
    el.addEventListener('input', () => { ex[k] = el.type === 'checkbox' ? el.checked : el.value; });
    el.addEventListener('change', () => { ex[k] = el.type === 'checkbox' ? el.checked : el.value; });
  });
  document.querySelectorAll('#meta .cls').forEach(cb => { cb.checked = ex.class_ids.includes(Number(cb.value)); });

  // ---------- item templates ----------
  const DEFAULTS = {
    fill: () => ({ prompt: 'Complete the sentences.', text: 'I [am] a student.\nShe [is|\'s] from Brazil.' }),
    dropdown: () => ({ prompt: 'Choose the correct option.', text: 'They [am|is|*are] my friends.' }),
    choice: () => ({ prompt: '', options: ['', '', ''], correct: 0 }),
    truefalse: () => ({ prompt: 'True or false?', statements: [{ text: '', answer: true }] }),
    order: () => ({ prompt: 'Put the words in order.', tokens: [], alternatives: [] }),
    match: () => ({ prompt: 'Match the columns.', pairs: [{ left: '', right: '' }, { left: '', right: '' }] }),
    group: () => ({ prompt: 'Put the words in the correct group.', categories: ['', ''], words: [{ text: '', category: '' }] }),
    free: () => ({ prompt: '', model_answer: '', keywords: [], min_words: 0, points: 5 }),
    speak: () => ({ prompt: 'Listen and repeat. Record your voice.', translation: 'Ouça e repita. Grave a sua voz.', phrases: [{ text: '', audio: '' }] }),
    info: () => ({ prompt: 'Read the text.', translation: 'Leia o texto.', text: '' }),
  };

  function field(label, input, hint) {
    return h('div', { class: 'field' }, h('label', {}, label), input, hint ? h('div', { class: 'hint' }, hint) : null);
  }
  function text(it, key, attrs) {
    return h('input', Object.assign({ type: 'text', value: it[key] || '', oninput: e => { it[key] = e.target.value; } }, attrs || {}));
  }
  function area(it, key, rows, attrs) {
    return h('textarea', Object.assign({ rows: rows || 3, oninput: e => { it[key] = e.target.value; } }, attrs || {}), it[key] || '');
  }

  function rowsEditor(arr, makeRow, blank, addLabel) {
    const box = h('div', { class: 'rows-editor' });
    const draw = () => {
      box.replaceChildren();
      arr.forEach((row, i) => {
        box.append(h('div', { class: 'r' }, makeRow(row, i),
          h('button', { class: 'btn small ghost', type: 'button', title: 'Remover', onclick: () => { arr.splice(i, 1); draw(); } }, '✕')));
      });
      box.append(h('button', { class: 'btn small', type: 'button', onclick: () => { arr.push(blank()); draw(); const rows = box.querySelectorAll('.r input[type=text]'); if (rows.length) rows[rows.length - 1].focus(); } }, addLabel));
    };
    draw();
    return box;
  }

  const EDITORS = {
    fill: it => [
      field('Texto', area(it, 'text', 6, { style: 'font-family:monospace' }),
        'Coloque a resposta entre [colchetes]. Respostas alternativas com |, ex.: She [is|\'s] happy. Maiúsculas e ponto final são ignorados.'),
    ],
    dropdown: it => [
      field('Texto', area(it, 'text', 6, { style: 'font-family:monospace' }),
        'Opções entre [colchetes] separadas por |. Marque a correta com *, ex.: I [*am|is|are] happy.'),
    ],
    choice: it => {
      const box = h('div');
      const draw = () => {
        box.replaceChildren(h('label', {}, 'Alternativas (marque a correta)'));
        it.options.forEach((o, i) => {
          box.append(h('div', { class: 'rows-editor' }, h('div', { class: 'r' },
            h('input', { type: 'radio', name: 'c_' + it.id, checked: it.correct === i, onchange: () => { it.correct = i; } }),
            h('input', { type: 'text', value: o, placeholder: 'Alternativa ' + (i + 1), oninput: e => { it.options[i] = e.target.value; } }),
            h('button', { class: 'btn small ghost', type: 'button', onclick: () => { it.options.splice(i, 1); if (it.correct >= it.options.length) it.correct = 0; draw(); } }, '✕'))));
        });
        box.append(h('button', { class: 'btn small', type: 'button', onclick: () => { it.options.push(''); draw(); } }, '+ alternativa'));
      };
      draw();
      return [box];
    },
    truefalse: it => [h('label', {}, 'Afirmações'), rowsEditor(it.statements, s => [
      h('input', { type: 'text', value: s.text, placeholder: 'Afirmação', oninput: e => { s.text = e.target.value; } }),
      h('input', { type: 'text', value: s.translation || '', placeholder: 'Tradução (opcional)', oninput: e => { s.translation = e.target.value; } }),
      h('select', { style: 'max-width:130px', onchange: e => { s.answer = e.target.value === 'T'; } },
        h('option', { value: 'T', selected: s.answer }, 'True'), h('option', { value: 'F', selected: !s.answer }, 'False')),
    ], () => ({ text: '', answer: true }), '+ afirmação')],
    order: it => [
      field('Frase correta, em partes', h('input', {
        type: 'text', value: it.tokens.join(' / '), placeholder: 'Are / you / a student / ?',
        oninput: e => { it.tokens = e.target.value.split('/').map(s => s.trim()).filter(Boolean); }
      }), 'Separe as partes com / (cada parte vira um bloco para arrastar).'),
      field('Outras ordens aceitas (opcional)', h('textarea', {
        rows: 2, oninput: e => { it.alternatives = e.target.value.split('\n').map(s => s.trim()).filter(Boolean); }
      }, it.alternatives.join('\n')), 'Uma frase completa por linha.'),
    ],
    match: it => [h('label', {}, 'Pares (a coluna da direita é embaralhada para o aluno)'), rowsEditor(it.pairs, p => [
      h('input', { type: 'text', value: p.left, placeholder: 'Esquerda', oninput: e => { p.left = e.target.value; } }),
      h('span', {}, '↔'),
      h('input', { type: 'text', value: p.right, placeholder: 'Direita', oninput: e => { p.right = e.target.value; } }),
    ], () => ({ left: '', right: '' }), '+ par')],
    group: it => {
      const wordsBox = h('div');
      const drawWords = () => wordsBox.replaceChildren(h('label', {}, 'Palavras'), rowsEditor(it.words, w => [
        h('input', { type: 'text', value: w.text, placeholder: 'Palavra', oninput: e => { w.text = e.target.value; } }),
        h('select', { onchange: e => { w.category = e.target.value; } },
          h('option', { value: '' }, '— grupo —'),
          it.categories.filter(Boolean).map(c => h('option', { value: c, selected: w.category === c }, c))),
      ], () => ({ text: '', category: '' }), '+ palavra'));
      drawWords();
      return [
        field('Grupos', h('input', {
          type: 'text', value: it.categories.join(', '), placeholder: 'am, is, are',
          onchange: e => { it.categories = e.target.value.split(',').map(s => s.trim()).filter(Boolean); drawWords(); }
        }), 'Separados por vírgula.'),
        wordsBox,
      ];
    },
    free: it => [
      field('Resposta modelo (mostrada ao aluno na correção)', area(it, 'model_answer', 3)),
      field('Palavras-chave (opcional)', h('input', {
        type: 'text', value: (it.keywords || []).join(', '), placeholder: 'am, is, my name is',
        oninput: e => { it.keywords = e.target.value.split(',').map(s => s.trim()).filter(Boolean); }
      }), 'Dão uma nota provisória automática. Texto livre sempre vai para sua revisão.'),
      field('Mínimo de palavras', h('input', { type: 'number', min: 0, value: it.min_words || 0, oninput: e => { it.min_words = Number(e.target.value); } })),
    ],
    speak: it => [h('label', {}, 'Palavras ou frases para o aluno falar (cada uma com seu áudio modelo, opcional)'), rowsEditor(it.phrases, p => [
      h('input', { type: 'text', value: p.text, placeholder: 'Ex.: How do you spell your name?', oninput: e => { p.text = e.target.value; } }),
      h('input', { type: 'text', value: p.audio || '', placeholder: 'Áudio modelo (link)', style: 'max-width:260px', oninput: e => { p.audio = e.target.value; } }),
    ], () => ({ text: '', audio: '' }), '+ frase'),
      h('div', { class: 'hint' }, 'O aluno ouve o modelo, grava a própria voz e compara. Cada frase gravada vale ponto; o navegador também tenta reconhecer a pronúncia (só como retorno ao aluno).')],
    info: it => [field('Texto', area(it, 'text', 8), 'Aparece uma vez, sem pontos. Use para textos de leitura seguidos de perguntas.')],
  };

  function unitCount(it) {
    if (it.type === 'fill' || it.type === 'dropdown') return ((it.text || '').match(/\[[^\[\]]+\]/g) || []).length;
    if (it.type === 'truefalse') return it.statements.length;
    if (it.type === 'match') return it.pairs.length;
    if (it.type === 'group') return it.words.length;
    if (it.type === 'speak') return it.phrases.length;
    if (it.type === 'info') return 0;
    return 1;
  }
  function pts(it) { if (it.type === 'info') return 0; return Number(it.points) > 0 ? Number(it.points) : (it.type === 'free' ? 5 : Math.max(1, unitCount(it))); }

  function render() {
    list.replaceChildren();
    ex.items.forEach((it, idx) => {
      const move = d => { const j = idx + d; if (j < 0 || j >= ex.items.length) return; [ex.items[idx], ex.items[j]] = [ex.items[j], ex.items[idx]]; render(); };
      const card = h('div', { class: 'card item-card' },
        h('div', { class: 'item-toolbar' },
          h('span', { class: 'title' }, `${idx + 1}. ${TYPES[it.type]}`),
          h('label', { class: 'row', style: 'margin:0;font-weight:600' }, 'Pontos',
            h('input', { type: 'number', min: 0, step: 0.5, style: 'width:80px', value: it.points || '', placeholder: 'auto', oninput: e => { it.points = e.target.value; updateTotal(); } })),
          h('button', { class: 'btn small', type: 'button', title: 'Subir', onclick: () => move(-1) }, '↑'),
          h('button', { class: 'btn small', type: 'button', title: 'Descer', onclick: () => move(1) }, '↓'),
          h('button', { class: 'btn small', type: 'button', title: 'Duplicar', onclick: () => { ex.items.splice(idx + 1, 0, Object.assign(JSON.parse(JSON.stringify(it)), { id: uid() })); render(); } }, '⧉'),
          h('button', { class: 'btn small danger', type: 'button', onclick: () => { if (confirm('Remover esta questão?')) { ex.items.splice(idx, 1); render(); } } }, 'Remover')),
        field('Enunciado (em inglês)', area(it, 'prompt', 2)),
        field('Tradução do enunciado (aparece logo abaixo)', text(it, 'translation', { placeholder: 'Ex.: Complete as frases.' })),
        field('Exemplo para o aluno seguir (opcional)', text(it, 'example', { placeholder: 'Ex.: I ___ a student. → I am a student.' })),
        field('Imagem (link, opcional)', text(it, 'image', { type: 'url', placeholder: 'https://…' })),
        field('Áudio (link, opcional)', text(it, 'audio', { type: 'text', placeholder: 'https://… (mp3/m4a) — para listening' })),
        EDITORS[it.type](it));
      card.addEventListener('input', updateTotal);
      list.append(card);
    });
    if (!ex.items.length) list.append(h('div', { class: 'card muted' }, 'Nenhuma questão ainda. Use os botões abaixo para adicionar.'));
    updateTotal();
  }
  function updateTotal() {
    const total = ex.items.reduce((s, it) => s + pts(it), 0);
    document.getElementById('totalPts').textContent = `${ex.items.length} questões · ${total} pontos (nota convertida para 0–10)`;
  }

  document.getElementById('addBar').addEventListener('click', e => {
    const t = e.target.dataset.type;
    if (!t) return;
    ex.items.push(Object.assign({ id: uid(), type: t, image: '' }, DEFAULTS[t]()));
    render();
    list.lastElementChild.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });

  document.getElementById('saveBtn').addEventListener('click', async () => {
    const btn = document.getElementById('saveBtn');
    const err = document.getElementById('saveErr');
    err.hidden = true;
    btn.disabled = true;
    const body = Object.assign({}, ex, {
      class_ids: [...document.querySelectorAll('#meta .cls:checked')].map(c => Number(c.value)),
      max_attempts: Number(ex.max_attempts) || 0,
    });
    try {
      const r = await fetch('/teacher/exercises/save', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
      const data = await r.json().catch(() => ({ error: 'Erro ao salvar (sessão expirada?)' }));
      if (!r.ok) throw new Error(data.error || 'Erro ao salvar');
      window.location = data.redirect;
    } catch (e) {
      err.textContent = e.message;
      err.hidden = false;
      btn.disabled = false;
    }
  });

  render();
})();
