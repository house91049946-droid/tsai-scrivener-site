// src/scripts/ui.ts — 全站互動：置頂導覽、手機選單、進場、回頂
const nav = document.getElementById('nav');
const burger = document.getElementById('burger');
const menu = document.getElementById('mobile-menu');

const onScroll = () => nav?.classList.toggle('scrolled', window.scrollY > 10);
onScroll();
addEventListener('scroll', onScroll, { passive: true });

burger?.addEventListener('click', () => {
  const open = menu?.classList.toggle('open');
  burger.setAttribute('aria-expanded', String(!!open));
  document.body.style.overflow = open ? 'hidden' : '';
});
menu?.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => {
  menu.classList.remove('open');
  burger?.setAttribute('aria-expanded', 'false');
  document.body.style.overflow = '';
}));

// 下拉選單（桌機 hover、手機點擊）
document.querySelectorAll<HTMLElement>('.has-sub > button').forEach((b) => {
  b.addEventListener('click', () => b.parentElement?.classList.toggle('open'));
});

// 進場：舊頁面的 .reveal 也一併處理
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const els = document.querySelectorAll<HTMLElement>('.reveal');
if (reduced || !('IntersectionObserver' in window)) {
  els.forEach((el) => { el.classList.add('in'); el.style.opacity = '1'; el.style.transform = 'none'; });
} else {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      const el = e.target as HTMLElement;
      el.classList.add('in'); el.style.opacity = '1'; el.style.transform = 'none';
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  els.forEach((el) => io.observe(el));
}

// 回頂
const top = document.getElementById('to-top');
const onTop = () => top?.classList.toggle('show', window.scrollY > 600);
onTop();
addEventListener('scroll', onTop, { passive: true });
top?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

// 保險：分頁在背景或觀察器沒觸發時，1.5 秒後一律顯示
setTimeout(() => els.forEach((el) => { el.classList.add('in'); el.style.opacity = '1'; el.style.transform = 'none'; }), 1500);
