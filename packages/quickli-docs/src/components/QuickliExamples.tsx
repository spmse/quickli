import type { ReactNode } from 'react';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import CodeBlock from '@theme/CodeBlock';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import Translate, { translate } from '@docusaurus/Translate';

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

interface AddToProjectProps {
    eyebrowLabel?: string;
    headingLabel?: string;
    descriptionLabel?: string;
    existingProjectLabel?: string;
    existingProjectHeadingLabel?: string;
    existingProjectDescriptionLabel?: string;
    newProjectLabel?: string;
    newProjectHeadingLabel?: string;
    newProjectDescriptionLabel?: string;
    noteLabel?: string;
    noteLinkLabel?: string;
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

export function AddToProject({
    eyebrowLabel,
    headingLabel,
    descriptionLabel,
    existingProjectLabel,
    existingProjectHeadingLabel,
    existingProjectDescriptionLabel,
    newProjectLabel,
    newProjectHeadingLabel,
    newProjectDescriptionLabel,
    noteLabel,
    noteLinkLabel,
}: AddToProjectProps): ReactNode {
    const defaultEyebrow = translate({
        id: 'component.AddToProject.eyebrow',
        message: 'Add to your project',
        description: 'Eyebrow label for the AddToProject section',
    });
    const defaultHeading = translate({
        id: 'component.AddToProject.heading',
        message: 'Start where you are.',
        description: 'Heading for the AddToProject section',
    });
    const defaultDescription = translate({
        id: 'component.AddToProject.description',
        message: 'Add quickli to an existing Git project, or create a clean project to experiment with the framework.',
        description: 'Description for the AddToProject section',
    });
    const defaultExistingLabel = translate({
        id: 'component.AddToProject.existingProject.label',
        message: 'Existing project',
        description: 'Label for the existing project path',
    });
    const defaultExistingHeading = translate({
        id: 'component.AddToProject.existingProject.heading',
        message: 'Add quickli to Git',
        description: 'Heading for the existing project path',
    });
    const defaultExistingDescription = translate({
        id: 'component.AddToProject.existingProject.description',
        message: 'Keep your current project and install quickli into its virtual environment.',
        description: 'Description for the existing project path',
    });
    const defaultNewLabel = translate({
        id: 'component.AddToProject.newProject.label',
        message: 'New project',
        description: 'Label for the new project path',
    });
    const defaultNewHeading = translate({
        id: 'component.AddToProject.newProject.heading',
        message: 'Initialize a workspace',
        description: 'Heading for the new project path',
    });
    const defaultNewDescription = translate({
        id: 'component.AddToProject.newProject.description',
        message: 'Create a small Git project, then add quickli as its first dependency.',
        description: 'Description for the new project path',
    });
    const defaultNote = translate({
        id: 'component.AddToProject.note',
        message: 'Prefer a guided walkthrough? Continue to',
        description: 'Note before the getting-started link',
    });
    const defaultNoteLink = translate({
        id: 'component.AddToProject.note.link',
        message: 'the Getting Started guide',
        description: 'Link label for the getting-started guide',
    });

    return (
        <section className={styles.projectSection}>
            <div className={styles.sectionIntro}>
                <p className={styles.eyebrow}>{eyebrowLabel ?? defaultEyebrow}</p>
                <Heading as="h2">{headingLabel ?? defaultHeading}</Heading>
                <p>{descriptionLabel ?? defaultDescription}</p>
            </div>
            <div className={styles.projectPaths}>
                <article className={styles.projectPath}>
                    <span className={styles.pathLabel}>{existingProjectLabel ?? defaultExistingLabel}</span>
                    <Heading as="h3">{existingProjectHeadingLabel ?? defaultExistingHeading}</Heading>
                    <p>{existingProjectDescriptionLabel ?? defaultExistingDescription}</p>
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
                    <span className={styles.pathLabel}>{newProjectLabel ?? defaultNewLabel}</span>
                    <Heading as="h3">{newProjectHeadingLabel ?? defaultNewHeading}</Heading>
                    <p>{newProjectDescriptionLabel ?? defaultNewDescription}</p>
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
                {noteLabel ?? defaultNote}{' '}
                <Link to="/docs/getting-started">{noteLinkLabel ?? defaultNoteLink}</Link>.
            </p>
        </section>
    );
}
