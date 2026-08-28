// astro.config.mjs
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://tsai-scrivener-site.pages.dev', // 業主綁自訂網域後改
  integrations: [sitemap()],
});
