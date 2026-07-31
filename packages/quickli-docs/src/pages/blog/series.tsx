import Link from '@docusaurus/Link';
import Translate from '@docusaurus/Translate';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import type { ReactElement } from 'react';
import { blogSeries } from '../../data/blogSeries';

export default function BlogSeriesPage(): ReactElement {
  const { i18n } = useDocusaurusContext();
  const german = i18n.currentLocale === 'de';
  return (
    <Layout title="Blog series" description="Browse quiCkLI blog series and follow-up articles.">
      <main className="container margin-vert--lg">
        <header>
          <h1><Translate id="blog.series.title">Blog series</Translate></h1>
          <p><Translate id="blog.series.description">Follow a complete quiCkLI topic from the first article to the last.</Translate></p>
        </header>
        {blogSeries.map((series) => (
          <section key={series.id} className="margin-vert--lg">
            <h2>{german ? series.titleDe : series.title}</h2>
            <p>{german ? series.descriptionDe : series.description}</p>
            <p><small><Translate id="blog.series.category">Category:</Translate> {german ? series.categoryDe : series.category}</small></p>
            <ol>
              {series.articles.map((article) => (
                <li key={article.slug}>
                  <Link to={`/blog/${article.slug}`}>{german ? article.titleDe : article.title}</Link>
                </li>
              ))}
            </ol>
          </section>
        ))}
      </main>
    </Layout>
  );
}
