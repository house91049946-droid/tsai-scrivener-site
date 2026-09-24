// src/scripts/ui.ts — 全站互動：選單、logo 深淺、首屏輪播、進場、大字視差、回頂
import Lenis from 'lenis';

const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const body = document.body;

// 平滑捲動
let lenis: Lenis | null = null;
if (!reduced) {
  lenis = new Lenis({ lerp: 0.1 });
  const raf = (t: number) => { lenis!.raf(t); requestAnimationFrame(raf); };
  requestAnimationFrame(raf);
}

// 選單
const menu = document.getElementById('menu');
const openBtn = document.getElementById('menu-open');
const closeBtn = document.getElementById('menu-close');
const burgerBtn = document.getElementById('menu-btn');
const setMenu = (open: boolean) => {
  menu?.classList.toggle('open', open);
  menu?.setAttribute('aria-hidden', String(!open));
  body.classList.toggle('menu-open', open);
  [openBtn, burgerBtn].forEach((b) => b?.setAttribute('aria-expanded', String(open)));
  burgerBtn?.setAttribute('aria-label', open ? '關閉選單' : '開啟選單');
  const lbl = burgerBtn?.querySelector('.lbl'); if (lbl) lbl.textContent = open ? '關閉' : '選單';
  if (open) lenis?.stop(); else lenis?.start();
};
burgerBtn?.addEventListener('click', () => setMenu(!menu?.classList.contains('open')));
menu?.querySelectorAll<HTMLElement>('.o-nav a').forEach((a, i) => a.style.setProperty('--i', String(i)));
openBtn?.addEventListener('click', () => setMenu(true));
closeBtn?.addEventListener('click', () => setMenu(false));
menu?.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => setMenu(false)));
addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });

// logo 深淺：首頁首屏上是白字
const hero = document.getElementById('hero');
if (hero) body.classList.add('on-dark');
const onScroll = () => {
  const past = hero ? window.scrollY > hero.offsetHeight - 80 : window.scrollY > 10;
  body.classList.toggle('scrolled', past);
};
onScroll();
addEventListener('scroll', onScroll, { passive: true });

// 首屏輪播
if (hero) {
  const slides = [...hero.querySelectorAll<HTMLElement>('.slide')];
  const dots = [...hero.querySelectorAll<HTMLButtonElement>('.pager button')];
  let cur = 0;
  let timer = 0;
  const go = (n: number) => {
    cur = (n + slides.length) % slides.length;
    slides.forEach((s, i) => s.classList.toggle('on', i === cur));
    dots.forEach((d, i) => d.classList.toggle('on', i === cur));
    // 預先載入下一張
    const next = slides[(cur + 1) % slides.length]?.querySelector('img');
    if (next && next.loading === 'lazy') next.loading = 'eager';
  };
  const start = () => { clearInterval(timer); if (!reduced) timer = window.setInterval(() => go(cur + 1), 6500); };
  dots.forEach((d) => d.addEventListener('click', () => { go(Number(d.dataset.go)); start(); }));
  start();
}

// 進場
const els = document.querySelectorAll<HTMLElement>('.reveal');
const show = (el: HTMLElement) => { el.classList.add('in'); el.style.opacity = '1'; el.style.transform = 'none'; };
if (reduced || !('IntersectionObserver' in window)) {
  els.forEach(show);
} else {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { show(e.target as HTMLElement); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -10% 0px' });
  els.forEach((el) => io.observe(el));
  // 保險：背景分頁或觀察器沒觸發時，2 秒後一律顯示已在畫面上方的元素
  setTimeout(() => els.forEach((el) => { if (el.getBoundingClientRect().top < innerHeight) show(el); }), 2000);
}

// 大字視差
const word = document.getElementById('word');
if (word && !reduced) {
  const upd = () => {
    const r = word.parentElement!.getBoundingClientRect();
    const p = (innerHeight - r.top) / (innerHeight + r.height);
    word.style.transform = `translateX(${(0.5 - p) * 120}px)`;
  };
  upd();
  addEventListener('scroll', upd, { passive: true });
}

// 回頂
const top = document.getElementById('to-top');
const onTop = () => top?.classList.toggle('show', window.scrollY > 700);
onTop();
addEventListener('scroll', onTop, { passive: true });
top?.addEventListener('click', () => (lenis ? lenis.scrollTo(0) : window.scrollTo({ top: 0, behavior: 'smooth' })));
