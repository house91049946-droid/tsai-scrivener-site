# 中友地政士事務所形象網站

中友地政士事務所（代書世家：蔡峻豪、蔡崇欽、丁玉梅三位地政士）形象網站。以 Astro 5 建置的靜態網站，部署於 Cloudflare Pages。

## 開發指令

| 指令 | 說明 |
| :--- | :--- |
| `npm install` | 安裝相依套件 |
| `npm run dev` | 啟動本機開發伺服器（`localhost:4321`） |
| `npm run build` | 建置正式版靜態檔到 `./dist/` |
| `npm run preview` | 在本機預覽建置結果 |
| `node scripts/check-law-links.mjs` | 檢查所有文章的 `lawRefs` 均指向 `law.moj.gov.tw`（全國法規資料庫）且連結可正常連線；CI 會自動執行，也可在本機手動跑一次再發稿 |

CI（`.github/workflows/ci.yml`）在每次 push 到 `main` 與每個 PR 上自動執行 `npm run build` 與 `check-law-links.mjs`，兩者皆需通過。

## 文章 frontmatter 規格

文章放在 `src/content/posts/`，檔名格式建議 `YYYY-MM-DD-slug.md`。frontmatter 欄位（見 `src/content.config.ts`）：

| 欄位 | 型別 / 限制 | 說明 |
| :--- | :--- | :--- |
| `title` | 字串，最長 40 字 | 文章標題 |
| `description` | 字串，最長 120 字 | 摘要（用於列表頁與 meta description） |
| `date` | 日期 | 發布日期 |
| `category` | 五選一：`買賣過戶` \| `繼承實務` \| `贈與節稅` \| `抵押設定` \| `稅務` | 分類 |
| `lawRefs` | 陣列，至少 1 筆，每筆含 `name`（字串）與 `url`（須為 `https://law.moj.gov.tw/...` 的有效網址） | 引用的法條，會被 CI 檢查連結有效性 |
| `lawRevisionCheck` | 日期 | 本文法條內容最後一次核對修法狀態的日期 |

範例：

```yaml
---
title: 房子過戶少一道手續，付了錢也不算你的
description: 民法第 758 條規定不動產物權非經登記不生效力。本文說明為何付清價金不等於取得所有權，以及移轉登記前該把關的三件事。
date: 2026-08-28
category: 買賣過戶
lawRefs:
  - name: 民法第 758 條
    url: https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=B0000001&flno=758
lawRevisionCheck: 2026-08-28
---
```

## 發稿流程

主筆 agent 開 PR → 業主 merge 即為核准上線。

## 部署設定（業主一次性）

1. 登入 Cloudflare Dashboard → Workers & Pages → Create → Pages → Connect to Git，選 `tsai-scrivener-site`。
2. Build command：`npm run build`；Build output：`dist`。
3. 完成後每次 merge 到 main 自動部署；每個 PR 會得到預覽網址。
4. 買好網域後在該 Pages 專案 → Custom domains 綁定，並回報網域名稱以更新 `astro.config.mjs` 的 `site`。
