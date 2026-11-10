/* RRS Site Assistant – floating chat widget (no dependencies). */
(function () {
	'use strict';
	if (window.self !== window.top || !window.RRS_AI) return; // not inside the Cornerstone preview iframe

	var cfg = window.RRS_AI;
	var busy = false;
	var loaded = false;

	/* ---------- DOM ---------- */
	var root = el('div', 'rrs-ai');
	root.innerHTML =
		'<button type="button" class="rrs-ai__fab" aria-label="Open Site Assistant">' +
		'<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><path fill="currentColor" d="M4 4h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H8l-4 4V6a2 2 0 0 1 2-2z"/></svg>' +
		'</button>' +
		'<section class="rrs-ai__panel" hidden aria-label="Site Assistant">' +
		'<header class="rrs-ai__head"><strong>Site Assistant</strong>' +
		'<span><button type="button" class="rrs-ai__new" title="Start a new chat">New chat</button>' +
		'<button type="button" class="rrs-ai__close" aria-label="Close">×</button></span></header>' +
		'<div class="rrs-ai__log" role="log" aria-live="polite"></div>' +
		'<form class="rrs-ai__form">' +
		'<textarea rows="2" placeholder="e.g. Change the Sunday service time on the home page to 10:30am"></textarea>' +
		'<button type="submit">Send</button>' +
		'</form>' +
		'</section>';
	document.body.appendChild(root);

	var fab = root.querySelector('.rrs-ai__fab');
	var panel = root.querySelector('.rrs-ai__panel');
	var log = root.querySelector('.rrs-ai__log');
	var form = root.querySelector('.rrs-ai__form');
	var input = form.querySelector('textarea');
	var sendBtn = form.querySelector('button');

	fab.addEventListener('click', function () { toggle(true); });
	root.querySelector('.rrs-ai__close').addEventListener('click', function () { toggle(false); });
	root.querySelector('.rrs-ai__new').addEventListener('click', function () {
		if (busy) return;
		api('reset', {}).then(function () { log.innerHTML = ''; greet(); });
	});
	input.addEventListener('keydown', function (e) {
		if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); }
	});
	form.addEventListener('submit', function (e) {
		e.preventDefault();
		var text = input.value.trim();
		if (!text || busy) return;
		input.value = '';
		add({ type: 'user', text: text });
		run('message', { text: text, context: { url: location.href, post_id: cfg.postId || 0 } });
	});

	function toggle(open) {
		panel.hidden = !open;
		fab.hidden = open;
		if (open && !loaded) {
			loaded = true;
			if (!cfg.ready) {
				greet(); // setup message only
			} else {
				api('history', null, 'GET').then(function (r) {
					(r.items || []).forEach(add);
					if (!r.items || !r.items.length) greet();
				}).catch(function () { greet(); });
			}
		}
		if (open) input.focus();
	}

	function greet() {
		if (!cfg.ready) {
			var n = add({ type: 'notice', text: 'The Site Assistant isn’t set up yet: it needs an API key. ' });
			if (cfg.setup) {
				var a = document.createElement('a');
				a.href = cfg.setup; a.textContent = 'Finish setup →';
				n.appendChild(a);
			}
			input.disabled = sendBtn.disabled = true;
			return;
		}
		add({ type: 'assistant', text: 'Hi! I can update pages on ' + cfg.site + ' for you — change text, images and buttons, add sections, or create new pages. What would you like to do?' });
	}

	/* ---------- the step loop ---------- */
	function run(endpoint, body) {
		setBusy(true);
		var typing = add({ type: 'typing', text: 'Working…' });
		api(endpoint, body).then(function (r) {
			typing.remove();
			(r.items || []).forEach(add);
			if (r.done) {
				setBusy(false);
				if (r.retry) retryButton();
			} else {
				run('continue', {});
			}
		}).catch(function (err) {
			typing.remove();
			add({ type: 'error', text: err.message || 'Something went wrong.' });
			setBusy(false);
			retryButton();
		});
	}

	function retryButton() {
		var b = el('button', 'rrs-ai__retry');
		b.type = 'button';
		b.textContent = 'Retry';
		b.addEventListener('click', function () { b.remove(); run('continue', {}); });
		log.appendChild(b);
		scroll();
	}

	function setBusy(on) {
		busy = on;
		sendBtn.disabled = on;
		input.disabled = on;
		if (!on) input.focus();
	}

	/* ---------- rendering ---------- */
	function add(item) {
		var node = el('div', 'rrs-ai__msg rrs-ai__msg--' + item.type);
		if (item.type === 'assistant') node.innerHTML = md(item.text);
		else if (item.type === 'tool') node.textContent = '⚙ ' + item.text;
		else if (item.type === 'tool_error') node.textContent = '⚠ ' + item.text + ' failed';
		else node.textContent = item.text;
		log.appendChild(node);
		scroll();
		return node;
	}

	function scroll() { log.scrollTop = log.scrollHeight; }

	// Tiny, safe markdown: escape first, then bold / code / links / lists / line breaks.
	function md(s) {
		s = String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
		s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
		s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
		s = s.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
		s = s.replace(/(^|[\s(])(https?:\/\/[^\s<)]+)/g, '$1<a href="$2" target="_blank" rel="noopener">$2</a>');
		s = s.replace(/^\s*[-*] (.+)$/gm, '<li>$1</li>').replace(/(<li>[\s\S]*?<\/li>)(?!\s*<li>)/g, '<ul>$1</ul>');
		s = s.replace(/^#{1,6} (.+)$/gm, '<strong>$1</strong>');
		return s.replace(/\n{2,}/g, '<br><br>').replace(/\n/g, '<br>').replace(/<\/li><br>/g, '</li>').replace(/<br><ul>/g, '<ul>');
	}

	/* ---------- helpers ---------- */
	function api(path, body, method) {
		return fetch(cfg.root + path, {
			method: method || 'POST',
			credentials: 'same-origin',
			headers: { 'Content-Type': 'application/json', 'X-WP-Nonce': cfg.nonce },
			body: method === 'GET' ? undefined : JSON.stringify(body || {})
		}).then(function (res) {
			return res.json().catch(function () { return {}; }).then(function (data) {
				if (!res.ok) throw new Error(data.message || ('Request failed (' + res.status + ')'));
				return data;
			});
		});
	}

	function el(tag, cls) { var n = document.createElement(tag); n.className = cls; return n; }
})();
