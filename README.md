# Open-source boilerplate

This is Saritasa's template for open source projects.

We use [copier](https://copier.readthedocs.io/en/stable/) tool for managing our boilerplate.
Read this documentation to understand how it works.

## Usage

Example:

```bash
git clone git@github.com:saritasa-nest/open-source-project && cd open-source-project
uvx copier copy git@github.com:saritasa-nest/saritasa-python-boilerplate-open-source.git . --vcs-ref main --trust --overwrite
```

## Updating .copier-answers.yml answers

```bash
uvx copier update --vcs-ref main --skip-answered --trust --skip-tasks --data {question}={answer}
```

Note: the `--data` flag is used to update the answer for a template question.
It expects template variable names (keys) in `key=value` form (for example, `--data python_version=3.14`).
When you use `--data`, Copier will update all related files.
You can use this flag multiple times in the same command to update multiple answers at once.

## Develop

Set up dev environment.

```bash
uv sync
inv pre-commit.install
```

To check if boilerplate is working

```bash
inv test.create-from-template
```

To check if boilerplate is working, and you can init project without errors

```bash
inv test.create-and-init-template
```

To check if boilerplate is working, and you can init project without errors
and also commit without doing any extra work

```bash
inv test.create-and-init-and-commit
```

Or if you're using VSCode you can use this shortcut
`SHIFT + CTRL + B` or `⇧ + ⌘ + B`
