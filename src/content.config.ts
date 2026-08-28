// src/content.config.ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string().max(40),
    description: z.string().max(120),
    date: z.coerce.date(),
    category: z.enum(['買賣過戶', '繼承實務', '贈與節稅', '抵押設定', '稅務']),
    lawRefs: z.array(z.object({ name: z.string(), url: z.string().url() })).min(1),
    lawRevisionCheck: z.coerce.date(),
  }),
});
export const collections = { posts };
