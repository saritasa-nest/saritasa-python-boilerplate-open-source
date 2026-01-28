import invoke
import saritasa_invocations

import invocations

ns = invoke.Collection(
    invocations.test,
    saritasa_invocations.git,
    saritasa_invocations.poetry,
    saritasa_invocations.pre_commit,
    saritasa_invocations.github_actions,
)

# Configurations for run command
ns.configure(
    {
        "run": {
            "pty": True,
            "echo": True,
        },
    },
)
