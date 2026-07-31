import type { ReactElement } from 'react';
import Footer from '@theme-original/Footer';
import useBaseUrl from '@docusaurus/useBaseUrl';

export default function FooterWrapper(): ReactElement {
  return (
    <div className="footer-shell">
      <Footer />
      <div className="footer-brand" aria-label="quiCkLI">
        <img
          src={`${useBaseUrl('img/quickli-dark-transparent.png')}`}
          alt="quiCkLI"
        />
      </div>
    </div>
  );
}
