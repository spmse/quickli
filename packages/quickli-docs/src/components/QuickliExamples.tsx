import type { ReactNode } from 'react';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import CodeBlock from '@theme/CodeBlock';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import styles from './QuickliExamples.module.css';

const minimalExample = `from quickli import Application, Argument
from quickli import core_json_or_yaml_loading, core_json_or_yaml_rendering

app = Application(name="profile")

@app.entrypoint(arguments=[Argument("payload")])
def normalize(payload: str) -> str:
    data = core_json_or_yaml_loading(payload)
    return core_json_or_yaml_rendering(data, format_name="json")`;

const existingProjectCommands = {
    pip: `pip install quickli`,
    uv: `uv add quickli`,
};

const newProjectCommands = {
    pip: `mkdir my-cli && cd my-cli
git init
python -m venv .venv
source .venv/bin/activate
python -m pip install quickli`,
    uv: `mkdir my-cli && cd my-cli
git init
uv init
uv add quickli`,
};

type ProgrammingLanguage = "bash" | "python";

type CodePanelProps = {
    title: string;
    code: string;
    language: ProgrammingLanguage;
    showLineNumbers?: boolean;
};

interface CodeExampleProps {
    codeExample?: string;
    language?: ProgrammingLanguage;
    title?: string;
    output?: string;
}


function CodePanel({ title, code, language, showLineNumbers }: CodePanelProps) {
    return (
        <div className={styles.codePanel}>
            <div className={styles.codeHeader}>{title}</div>
            <CodeBlock
                language={language}
                className={styles.highlightedCode}
                showLineNumbers={showLineNumbers}
            >
                {code}
            </CodeBlock>
        </div>
    );
}

export function MinimalExample(
    { title, codeExample, language, output }: CodeExampleProps
): ReactNode {
    return (
        <div className={styles.example}>
            <CodePanel
                title={title ?? "hello.py"}
                code={codeExample ?? minimalExample}
                language={language ?? "python"}
            />
            <p className={styles.output}>
                {output ?? `$ python profile.py "name: Ada" → {"name": "Ada"}`}
            </p>
        </div>
    );
}

export function AddToProject(): ReactNode {
    return (
        <section className={styles.projectSection}>
            <div className={styles.sectionIntro}>
                <p className={styles.eyebrow}>Add to your project</p>
                <Heading as="h2">Start where you are.</Heading>
                <p>
                    Add quickli to an existing Git project, or create a clean project to experiment with
                    the framework.
                </p>
            </div>
            <div className={styles.projectPaths}>
                <article className={styles.projectPath}>
                    <span className={styles.pathLabel}>Existing project</span>
                    <Heading as="h3">Add quickli to Git</Heading>
                    <p>
                        Keep your current project and install quickli into its virtual environment.
                    </p>
                    <Tabs groupId="add-to-project" defaultValue="pip" className={styles.projectTabs}>
                        <TabItem value="pip" label="pip" default>
                            <CodePanel title="Terminal" code={existingProjectCommands["pip"]} language="bash" />
                        </TabItem>
                        <TabItem value="uv" label="uv">
                            <CodePanel title="Terminal" code={existingProjectCommands["uv"]} language="bash" />
                        </TabItem>
                    </Tabs>
                </article>
                <article className={styles.projectPath}>
                    <span className={styles.pathLabel}>New project</span>
                    <Heading as="h3">Initialize a workspace</Heading>
                    <p>Create a small Git project, then add quickli as its first dependency.</p>
                    <Tabs groupId="add-to-project" defaultValue="pip" className={styles.projectTabs}>
                        <TabItem value="pip" label="pip" default>
                            <CodePanel title="Terminal" code={newProjectCommands["pip"]} language="bash" />
                        </TabItem>
                        <TabItem value="uv" label="uv">
                            <CodePanel title="Terminal" code={newProjectCommands["uv"]} language="bash" />
                        </TabItem>

                    </Tabs>
                </article>
            </div>
            <p className={styles.projectNote}>
                Prefer a guided walkthrough? Continue to{' '}
                <Link to="/docs/getting-started">the Getting Started guide</Link>.
            </p>
        </section>
    );
}
