// src/lib/cover.ts — 文章封面：依分類挑一組照片，同分類內按文章順序輪替，避免相鄰重複
const pools: Record<string, string[]> = {
  稅務: ['cover-tax', 'flow-calc', 'svc-plan', 'cover-mortgage', 'svc-ptax', 'flow-sign'],
  繼承實務: ['cover-inherit', 'svc-gift', 'flow-folder', 'svc-plan'],
  贈與節稅: ['cover-gift', 'svc-inherit', 'flow-done', 'svc-ptax'],
  買賣過戶: ['cover-transfer', 'flow-sign', 'hero-street'],
  抵押設定: ['cover-mortgage', 'flow-folder'],
};
/** posts 需已依日期排序；回傳 /photo/xxx.webp */
export function coverFor(id: string, category: string, posts: { id: string; data: { category: string } }[]) {
  const pool = pools[category] ?? pools['稅務'];
  const same = posts.filter((p) => p.data.category === category).map((p) => p.id);
  const i = Math.max(0, same.indexOf(id));
  return `/photo/${pool[i % pool.length]}.webp`;
}
