import Link from '@docusaurus/Link';
import Translate from '@docusaurus/Translate';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import type { ReactElement } from 'react';
import type { BlogSeries } from '../data/blogSeries';

type Props = {
  series: BlogSeries;
  currentSlug: string;
};

export default function BlogSeriesNavigation({ series, currentSlug }: Props): ReactElement {
  const { i18n } = useDocusaurusContext();
  const german = i18n.currentLocale === 'de';
  const currentIndex = series.articles.findIndex((article) => article.slug === currentSlug);
  const previous = currentIndex > 0 ? series.articles[currentIndex - 1] : undefined;
  const next = currentIndex >= 0 ? series.articles[currentIndex + 1] : undefined;

  return (
    <aside className="blog-series-navigation" aria-label={german ? 'Serie' : 'Series'}>
      <p><strong>{german ? series.titleDe : series.title}</strong></p>
      <p>
        {currentIndex >= 0 && (
          <Translate
            id="blog.series.part"
            values={{ current: currentIndex + 1, total: series.articles.length }}
          >{`Part {current} of {total}`}</Translate>
        )}
      </p>
      <ol>
        {series.articles.map((article) => (
          <li key={article.slug} aria-current={article.slug === currentSlug ? 'page' : undefined}>
            <Link to={`/blog/${article.slug}`}>
              {article.position}. {german ? article.titleDe : article.title}
            </Link>
          </li>
        ))}
      </ol>
      <p>
        {previous && <Link to={`/blog/${previous.slug}`}>← <Translate id="blog.series.previous">Previous</Translate></Link>}
        {previous && next && ' · '}
        {next && <Link to={`/blog/${next.slug}`}><Translate id="blog.series.next">Next</Translate> →</Link>}
      </p>
      <p><Link to="/blog/series"><Translate id="blog.series.overviewLink">View all series</Translate></Link></p>
    </aside>
  );
}
