const API_BASE = location.origin.includes('localhost') || location.origin.startsWith('http')
  ? 'http://localhost:5000'   // ajusta si cal
  : 'http://localhost:5000';

function mountSidebar(active='main'){
  const el = document.querySelector('#sidebar');
  if(!el) return;
  el.innerHTML = `
    <div class="brand">Web Ocell</div>
    <a class="btn ${active==='main'?'':'secondary'}" href="./index.html">🟢Main</a>
    <a class="btn ${active==='info'?'':'secondary'}" href="./info.html">📄Informació</a>
    <div class="footer small">La part verda és fixa i comuna a totes les pàgines.</div>
  `;
}

function q(name){
  const url = new URL(location.href);
  return url.searchParams.get(name);
}

async function api(path){
  const r = await fetch(`${API_BASE}${path}`);
  if(!r.ok) throw new Error('API error: '+r.status);
  return r.json();
}

// HLS helper
function playHlsOrMp4(videoEl, src){
  if (src.endsWith('.m3u8')) {
    if (videoEl.canPlayType('application/vnd.apple.mpegURL')) {
      videoEl.src = src;
    } else if (window.Hls) {
      const hls = new Hls();
      hls.loadSource(src);
      hls.attachMedia(videoEl);
    } else {
      const warn = document.createElement('div');
      warn.textContent = 'Cal Hls.js per reproduir HLS en aquest navegador.';
      warn.className = 'small';
      videoEl.replaceWith(warn);
    }
  } else {
    videoEl.src = src;
  }
}