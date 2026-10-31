'use client';
import { useState, type ComponentType, type AnchorHTMLAttributes } from 'react';
import './aimeet-ui.css';

export type Exhibitor = {
  id: string;
  companyName: string;
  boothNumber?: string;
  categories?: string[];
  category?: string;
  exhibitionContent?: string;
  companyDescription?: string;
  logoUrl?: string;
};
export type CardLabels = {
  details: (name: string) => string;
  save: (name: string) => string;
  unsave: (name: string) => string;
  booth: string;
  noBooth: string;
  emptyDescription: string;
  moreCategories: (count: number) => string;
};
export const japaneseLabels: CardLabels = {
  details: name => `${name}の詳細を見る`,
  save: name => `${name}をお気に入りに追加`,
  unsave: name => `${name}をお気に入りから削除`,
  booth: '小間番号', noBooth: '未登録',
  emptyDescription: '出展者の詳細情報をご覧いただけます。',
  moreCategories: count => `ほか${count}カテゴリ`,
};
function httpUrl(value?: string) {
  try { const u = new URL(value || ''); return ['https:', 'http:'].includes(u.protocol) ? u.href : undefined; }
  catch { return undefined; }
}
function Logo({ name, src }: { name: string; src?: string }) {
  const [failed, setFailed] = useState(false);
  const initials = name.replace(/株式会社|有限会社|合同会社/g, '').trim().slice(0, 2) || 'A';
  return <div className="aimeet-card__visual">
    {src && !failed ? <img src={src} alt="" loading="lazy" onError={() => setFailed(true)} />
      : <span className="aimeet-card__initials" aria-hidden="true">{initials}</span>}
  </div>;
}
type Props = {
  exhibitor: Exhibitor;
  /** Supply a trusted route built by the application's existing router. */
  href: string;
  saved: boolean;
  pending?: boolean;
  onFavorite: (id: string) => void;
  labels?: CardLabels;
  /** Wrap the existing router Link to satisfy anchor props when needed. */
  LinkComponent?: ComponentType<AnchorHTMLAttributes<HTMLAnchorElement>>;
};
export function ExhibitorCard({ exhibitor: e, href, saved, pending, onFavorite,
  labels: t = japaneseLabels, LinkComponent }: Props) {
  const Link = LinkComponent || 'a';
  const categories = [...new Set(e.categories?.length ? e.categories : e.category ? [e.category] : [])];
  const logo = httpUrl(e.logoUrl);
  return <article className="aimeet-card">
    <Logo key={logo || 'no-logo'} src={logo} name={e.companyName} />
    <button type="button" className="aimeet-card__favorite" aria-pressed={saved}
      aria-label={saved ? t.unsave(e.companyName) : t.save(e.companyName)} disabled={pending}
      onClick={() => onFavorite(e.id)}>{saved ? '♥' : '♡'}</button>
    <div className="aimeet-card__body">
      <div className="aimeet-card__tags">{categories.slice(0, 2).map(c => <span key={c}>{c}</span>)}
        {categories.length > 2 && <span aria-label={t.moreCategories(categories.length - 2)}>＋{categories.length - 2}</span>}
      </div>
      <h3><Link className="aimeet-card__link" href={href} aria-label={t.details(e.companyName)}>{e.companyName}</Link></h3>
      <p>{e.exhibitionContent || e.companyDescription || t.emptyDescription}</p>
    </div>
    <div className="aimeet-card__bottom"><span>{t.booth} <b>{e.boothNumber || t.noBooth}</b></span><span aria-hidden="true">↗</span></div>
  </article>;
}
