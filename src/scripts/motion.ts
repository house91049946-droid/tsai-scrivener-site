// src/scripts/motion.ts
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';

const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

export function initMotion() {
  if (reduced) {
    // 降級：全部直接呈現
    document.querySelectorAll<HTMLElement>('.reveal, .line-inner, .goldline')
      .forEach((el) => { el.style.opacity = '1'; el.style.transform = 'none'; });
    document.querySelectorAll<HTMLElement>('[data-count]').forEach((el) => {
      el.childNodes[0]!.textContent = (+el.dataset.count!).toLocaleString();
    });
    return;
  }
  gsap.registerPlugin(ScrollTrigger);

  const lenis = new Lenis({ lerp: 0.12 });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((t) => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);

  // 首屏開場
  gsap.timeline()
    .to('.eyebrow', { opacity: 1, duration: 0.6 }, 0.2)
    .to('.l1 .line-inner', { y: 0, duration: 1, ease: 'expo.out' }, 0.35)
    .to('.l2 .line-inner', { y: 0, duration: 1, ease: 'expo.out' }, 0.5)
    .to('.hero .sub', { opacity: 1, duration: 0.7 }, 1.0)
    .to('.hero .btns', { opacity: 1, duration: 0.7 }, 1.2)
    .to('.portrait', { opacity: 1, y: 0, duration: 1.1, ease: 'expo.out' }, 0.7);

  // 捲動觸發進場
  document.querySelectorAll('[data-io]').forEach((sec) => {
    gsap.to(sec.querySelectorAll('.reveal'), {
      opacity: 1, y: 0, duration: 0.9, ease: 'expo.out', stagger: 0.1,
      scrollTrigger: { trigger: sec, start: 'top 80%' },
    });
  });

  // 數字牆
  document.querySelectorAll<HTMLElement>('[data-count]').forEach((el) => {
    const end = +el.dataset.count!;
    const obj = { v: 0 };
    gsap.to(obj, {
      v: end, duration: 1.5, ease: 'power3.out',
      scrollTrigger: { trigger: el, start: 'top 85%' },
      onUpdate: () => { el.childNodes[0]!.textContent = Math.round(obj.v).toLocaleString(); },
    });
  });

  // 視差
  gsap.to('#wm', { y: -120, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
  gsap.to('#pt', { y: 46, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });

  // 導覽列
  const nav = document.querySelector('nav')!;
  ScrollTrigger.create({ start: 40, onUpdate: (self) => nav.classList.toggle('scrolled', self.scroll() > 40) });
}
initMotion();
