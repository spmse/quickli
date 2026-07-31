import type { ReactNode } from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Translate, { translate } from '@docusaurus/Translate';

import { AddToProject, MinimalExample } from '../components/QuickliExamples';
import styles from './index.module.css';

function HomepageHeader() {
    const { siteConfig } = useDocusaurusContext();
    const lightLogo = useBaseUrl('img/quickli-light-transparent.png');
    const darkLogo = useBaseUrl('img/quickli-dark-transparent.png');

    return (
        <header className={styles.heroBanner}>
            <div className="container">
                <div className={styles.brandMark} aria-label="quiCkLI">
                    <img className={styles.brandMarkLight} src={lightLogo} alt="quiCkLI" />
                    <img className={styles.brandMarkDark} src={darkLogo} alt="" />
                </div>
                <div className={styles.heroGrid}>
                    <div>
                        <p className={styles.eyebrow}>
                            <Translate id="homepage.hero.eyebrow">
                                A small place to learn CLI design
                            </Translate>
                        </p>
                        <Heading as="h1" className={styles.heroTitle}>
                            <Translate id="homepage.hero.title">
                                Build command-line tools you can understand.
                            </Translate>
                        </Heading>
                        <p className={styles.heroSubtitle}>
                            <Translate
                                id="homepage.hero.subtitle"
                                values={{ title: siteConfig.title }}
                            >
                                {'{title} is an educational minimal framework for learning how Python command-line applications are put together.'}
                            </Translate>
                        </p>
                        <div className={styles.buttons}>
                            <Link className="button button--primary button--lg" to="/docs/getting-started">
                                <Translate id="homepage.hero.button.docs">
                                    Read the docs
                                </Translate>
                            </Link>
                            <Link
                                className="button button--secondary button--lg"
                                href="https://pypi.org/project/quickli/"
                            >
                                <Translate id="homepage.hero.button.pypi">
                                    Install from PyPI
                                </Translate>
                            </Link>
                            <Link
                                className="button button--secondary button--lg"
                                href="https://github.com/spmse/quickli"
                            >
                                <Translate id="homepage.hero.button.source">
                                    View source
                                </Translate>
                            </Link>
                        </div>
                    </div>
                    <MinimalExample />
                </div>
            </div>
        </header>
    );
}

function Overview() {
    return (
        <section className={styles.overview}>
            <div className="container">
                <div className={styles.sectionIntro}>
                    <p className={styles.eyebrow}>
                        <Translate id="homepage.overview.eyebrow">Learn by building</Translate>
                    </p>
                    <Heading as="h2">
                        <Translate id="homepage.overview.heading">The essentials, without the noise.</Translate>
                    </Heading>
                    <p>
                        <Translate id="homepage.overview.description">
                            quickli keeps the core ideas visible: register a handler, describe its inputs, and
                            dispatch explicit command-line tokens.
                        </Translate>
                    </p>
                </div>
                <div className={styles.cards}>
                    <article className={styles.card}>
                        <span className={styles.cardNumber}>01</span>
                        <Heading as="h3">
                            <Translate id="homepage.overview.card1.heading">Small primitives</Translate>
                        </Heading>
                        <p>
                            <Translate id="homepage.overview.card1.description">
                                {'Learn Application, Command, Argument, and Option one concept at a time.'}
                            </Translate>
                        </p>
                    </article>
                    <article className={styles.card}>
                        <span className={styles.cardNumber}>02</span>
                        <Heading as="h3">
                            <Translate id="homepage.overview.card2.heading">Readable Python</Translate>
                        </Heading>
                        <p>
                            <Translate id="homepage.overview.card2.description">
                                Use decorators and ordinary functions to create tools that are easy to inspect.
                            </Translate>
                        </p>
                    </article>
                    <article className={styles.card}>
                        <span className={styles.cardNumber}>03</span>
                        <Heading as="h3">
                            <Translate id="homepage.overview.card3.heading">Room to explore</Translate>
                        </Heading>
                        <p>
                            <Translate id="homepage.overview.card3.description">
                                Start with a tiny example, then add conversion, validation, and subcommands.
                            </Translate>
                        </p>
                    </article>
                </div>
                <div className={styles.nextStep}>
                    <div>
                        <p className={styles.eyebrow}>
                            <Translate id="homepage.nextStep.eyebrow">New to quickli?</Translate>
                        </p>
                        <Heading as="h2">
                            <Translate id="homepage.nextStep.heading">Begin with the documentation.</Translate>
                        </Heading>
                        <p>
                            <Translate id="homepage.nextStep.description">
                                Follow the short guide, run the example, and use the source as your reference.
                            </Translate>
                        </p>
                    </div>
                    <Link className="button button--primary" to="docs/introduction">
                        <Translate id="homepage.nextStep.button">
                            Read the introduction
                        </Translate>
                    </Link>
                </div>
            </div>
        </section>
    );
}

export default function Home(): ReactNode {
    const { siteConfig } = useDocusaurusContext();

    return (
        <Layout
            title={siteConfig.title}
            description={translate({
                id: 'homepage.meta.description',
                message: 'A minimal Python framework for building command-line interfaces. Learn CLI design with small, readable examples.',
                description: 'Homepage meta description for SEO',
            })}
        >
            <HomepageHeader />
            <Overview />
            <div className={styles.addToProject}>
                <div className="container">
                    <AddToProject />
                </div>
            </div>
        </Layout>
    );
}
