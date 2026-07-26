import type { ReactNode } from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import { AddToProject, MinimalExample } from '../components/QuickliExamples';
import styles from './index.module.css';

function HomepageHeader() {
    const { siteConfig } = useDocusaurusContext();

    return (
        <header className={styles.heroBanner}>
            <div className="container">
                <div className={styles.heroGrid}>
                    <div>
                        <p className={styles.eyebrow}>A small place to learn CLI design</p>
                        <Heading as="h1" className={styles.heroTitle}>
                            Build command-line tools you can understand.
                        </Heading>
                        <p className={styles.heroSubtitle}>
                            {siteConfig.title} is an educational minimal framework lite for learning how
                            Python command-line applications are put together.
                        </p>
                        <div className={styles.buttons}>
                            <Link className="button button--primary button--lg" to="/docs/getting-started">
                                Read the docs
                            </Link>
                            <Link
                                className="button button--secondary button--lg"
                                href="https://pypi.org/project/quickli/"
                            >
                                Install from PyPI
                            </Link>
                            <Link
                                className="button button--secondary button--lg"
                                href="https://github.com/spmse/quickli"
                            >
                                View source
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
                    <p className={styles.eyebrow}>Learn by building</p>
                    <Heading as="h2">The essentials, without the noise.</Heading>
                    <p>
                        quickli keeps the core ideas visible: register a handler, describe its inputs, and
                        dispatch explicit command-line tokens.
                    </p>
                </div>
                <div className={styles.cards}>
                    <article className={styles.card}>
                        <span className={styles.cardNumber}>01</span>
                        <Heading as="h3">Small primitives</Heading>
                        <p>
                            Learn <code>Application</code>, <code>Command</code>, <code>Argument</code>, and{' '}
                            <code>Option</code> one concept at a time.
                        </p>
                    </article>
                    <article className={styles.card}>
                        <span className={styles.cardNumber}>02</span>
                        <Heading as="h3">Readable Python</Heading>
                        <p>Use decorators and ordinary functions to create tools that are easy to inspect.</p>
                    </article>
                    <article className={styles.card}>
                        <span className={styles.cardNumber}>03</span>
                        <Heading as="h3">Room to explore</Heading>
                        <p>Start with a tiny example, then add conversion, validation, and subcommands.</p>
                    </article>
                </div>
                <div className={styles.nextStep}>
                    <div>
                        <p className={styles.eyebrow}>New to quickli?</p>
                        <Heading as="h2">Begin with the documentation.</Heading>
                        <p>Follow the short guide, run the example, and use the source as your reference.</p>
                    </div>
                    <Link className="button button--primary" to="/docs/introduction">
                        Read the introduction
                    </Link>
                </div>
            </div>
        </section>
    );
}

export default function Home(): ReactNode {
    const { siteConfig } = useDocusaurusContext();

    return (
        <Layout title={siteConfig.title} description={siteConfig.tagline}>
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
