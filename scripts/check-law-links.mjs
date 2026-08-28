// scripts/check-law-links.mjs — 檢查文章 lawRefs 均指向全國法規資料庫、連結真的有效（非 302→ErrorPage）、
// 且頁面內容與 frontmatter 的條號互相一致
import { readFileSync, readdirSync } from 'node:fs';
const dir = 'src/content/posts';
let fail = 0;
const refs = []; // { file, name, url }

for (const f of readdirSync(dir).filter((f) => f.endsWith('.md'))) {
  const src = readFileSync(`${dir}/${f}`, 'utf8');
  for (const m of src.matchAll(/-\s*name:\s*(.+)\r?\n\s*url:\s*(\S+)/g)) {
    const name = m[1].trim();
    const url = m[2].trim();
    if (!url.startsWith('https://law.moj.gov.tw/')) {
      console.error(`${f}: lawRefs 必須指向 law.moj.gov.tw → ${url}`);
      fail = 1;
      continue;
    }
    refs.push({ file: f, name, url });
  }
}

const bodyCache = new Map(); // url -> { res, body }
for (const ref of refs) {
  // 3. frontmatter name（如「民法第 758 條」）抽出的條號，須與 URL 的 flno 一致
  const flno = new URL(ref.url).searchParams.get('flno');
  const nameNo = ref.name.match(/第\s*(\d+)\s*條/)?.[1];
  if (!flno || !nameNo || flno !== nameNo) {
    console.error(`${ref.file}: lawRefs name「${ref.name}」條號與 URL flno=${flno ?? '(無)'} 不一致`);
    fail = 1;
    continue;
  }

  let cached = bodyCache.get(ref.url);
  if (!cached) {
    const res = await fetch(ref.url, { method: 'GET' }).catch(() => null);
    if (!res || !res.ok) {
      console.error(`連結失效（${res?.status ?? '網路錯誤'}）: ${ref.url}`);
      fail = 1;
      continue;
    }
    const body = await res.text();
    cached = { res, body };
    bodyCache.set(ref.url, cached);
  }
  const { res, body } = cached;

  // 1. fetch 後的最終網址不能落在 ErrorPage（law.moj.gov.tw 對錯誤條號常回 302→ErrorPage.aspx 再 200）
  if (res.url.includes('ErrorPage')) {
    console.error(`${ref.file}: 連結導向錯誤頁 → ${ref.url} → ${res.url}`);
    fail = 1;
    continue;
  }

  // 2. body 需真的含有「第 <flno> 條」
  if (!body.includes(`第 ${flno} 條`)) {
    console.error(`${ref.file}: 頁面內容找不到「第 ${flno} 條」→ ${ref.url}`);
    fail = 1;
  }
}
process.exit(fail);
