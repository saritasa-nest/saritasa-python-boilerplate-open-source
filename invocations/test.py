import pathlib
import copier
import invoke
import saritasa_invocations
import yaml


@invoke.task
def create_from_template(
    context: invoke.Context,
    package_name: str = "test-open-source-project",
    folder_name: str = "",
    package_description: str = "This is a short description of the package.",
    min_python_version: float = 0.0,
) -> None:
    """Test that can create project via copier."""
    saritasa_invocations.print_success(
        "Test project initialization via copier",
    )
    saritasa_invocations.print_success("Recreating tmp folder")
    context.run("rm -rf .tmp")
    context.run("mkdir -p .tmp")
    if not min_python_version:
        with pathlib.Path("copier.yaml").open() as stream:
            min_python_version = float(
                yaml.safe_load(stream)["min_python_version"]["default"],
            )
    if not folder_name:
        folder_name = package_name.replace("-", "_")
    with context.cd(".tmp"):
        context.run("git init .")
        context.run('git config --local user.email "github@saritasa.com"')
        context.run('git config --local user.name "Github"')
    copier.run_copy(
        ".",
        ".tmp",
        data={
            "package_name": package_name,
            "folder_name": folder_name,
            "package_description": package_description,
            "min_python_version": min_python_version,
        },
        vcs_ref="HEAD",
        unsafe=True,
        overwrite=True,
    )
    saritasa_invocations.print_success("Project is created at .tmp")


@invoke.task
def create_and_init_template(
    context: invoke.Context,
    package_name: str = "test-open-source-project",
    folder_name: str = "",
    package_description: str = "This is a short description of the package.",
    min_python_version: str = "",
) -> None:
    """Test that can create project via copier and start it."""
    create_from_template(
        context,
        package_name=package_name,
        folder_name=folder_name,
        package_description=package_description,
        min_python_version=min_python_version,
    )

    with context.cd(".tmp"):
        context.run(
            ". .venv/bin/activate && inv project.init",
        )


@invoke.task
def create_and_init_and_commit(
    context: invoke.Context,
    package_name: str = "test-open-source-project",
    folder_name: str = "test_open_source_project",
    package_description: str = "This is a short description of the package.",
    min_python_version: str = "",
    commit: bool = True,
) -> None:
    """Test full project init workflow."""
    create_and_init_template(
        context,
        package_name=package_name,
        folder_name=folder_name,
        package_description=package_description,
        min_python_version=min_python_version,
    )

    with context.cd(".tmp"):
        context.run("git checkout -b feature/init-project")
        context.run("git add --all")
        git_message = "Init project"
        # In cases when project is generated with minor issues which
        # pre-commit can fix.
        try:
            context.run(f'git commit -m "{git_message}"')
        except invoke.UnexpectedExit:
            if commit:
                context.run("git add --all")
                context.run(f'git commit -m "{git_message}"')
        if commit:
            context.run(
                ". .venv/bin/activate && "
                "pre-commit run --hook-stage push --all-files",
            )
