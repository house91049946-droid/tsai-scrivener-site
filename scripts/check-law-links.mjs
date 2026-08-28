// scripts/check-law-links.mjs — 檢查文章 lawRefs 均指向全國法規資料庫且可連線
import { readFileSync, readdirSync } from 'node:fs';
const dir = 'src/content/posts';
let fail = 0;
const urls = new Set();
for (const f of readdirSync(dir).filter((f) => f.endsWith('.md'))) {
  const src = readFileSync(`${dir}/${f}`, 'utf8');
  for (const m of src.matchAll(/url:\s*(\S+)/g)) {
    const url = m[1];
    if (!url.startsWith('https://law.moj.gov.tw/')) {
      console.error(`${f}: lawRefs 必須指向 law.moj.gov.tw → ${url}`);
      fail = 1;
    } else urls.add(url);
  }
}
for (const url of urls) {
  const res = await fetch(url, { method: 'GET' }).catch(() => null);
  if (!res || !res.ok) { console.error(`連結失效（${res?.status ?? '網路錯誤'}）: ${url}`); fail = 1; }
}
process.exit(fail);
