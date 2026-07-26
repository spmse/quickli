import type { ReactNode } from 'react';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import CodeBlock from '@theme/CodeBlock';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

import styles from './QuickliExamples.module.css';

const minimalExample = `from quickli import Application, Argument

app = Application(name="hello")

@app.entrypoint(arguments=[Argument("name")])
def greet(name: str) -> str:
    return f"Hello, {name}!"`;

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

type TProgrammingLanguage = "bash"
    | "python"
    | "powershell"
    | "typescript"
    | "javascript"
    | "dockerfile"
    | "json"
    | "yaml"
    | "toml"
    | "ini"
    | "markdown"
    | "sql"
    | "go"
    | "rust"
    | "hcl";

type TCodePanelProps = {
    title: string;
    code: string;
    language: TProgrammingLanguage;
    showLineNumbers?: boolean;
};

interface ICodeExampleProps {
    codeExample?: string;
    language?: TProgrammingLanguage;
    title?: string;
    output?: string;
};


function CodePanel({ title, code, language, showLineNumbers }: TCodePanelProps) {
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
    { title, codeExample, language, output }: ICodeExampleProps
): ReactNode {
    return (
        <div className={styles.example}>
            <CodePanel
                title={title ?? "hello.py"}
                code={codeExample ?? minimalExample}
                language={language ?? "python"}
            />
            <p className={styles.output}>{output ?? `$ python hello.py Ada → Hello, Ada!`}</p>
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
