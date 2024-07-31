import atexit
import json
import os
import subprocess
from pathlib import Path
from typing import Optional

import flask
import werkzeug


class TailwindCompiler:
    """
    Start subprocess to compile TailwindCSS on-the-fly on change.
    Enables hot reloading for flask --debug mode.
    """

    proc: Optional[subprocess.Popen] = None

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(
        self,
        app: flask.Flask,
        debugmode_only: bool = True,
    ):
        """Start subprocess to compile TailwindCSS on-the-fly on change.

        Prerequisites: flask app is run in debug mode & second instance started
        by `werkzeug` is running (this second instance is needed in debug mode
        to watch for changes). This ensures that the subprocess is only started
        once.
        """
        self.app = app
        npm_script_name = "watch"
        debugmode = app.config.get("DEBUG")
        is_reloader = werkzeug.serving.is_running_from_reloader()

        if debugmode and is_reloader:
            self.run(npm_script_name)
        elif not debugmode and not debugmode_only:
            self.run(npm_script_name)
        else:
            pass

    def run(self, npm_script_name):
        """Run TailwindCSS Compiler as subprocess.

        Store the current working dir and assume that tailwind, configs,
        etc. are in the apps parent dir. Change the working directory to the
        parent dir. Get the command for running tailwind from the package.json.
        Start the subprocess. Then change back to the original working dir.
        Finally register the subprocess so that it can be shut down on exit.

        Parameters
        ----------
        npm_script_name : str
            The script that should be run must be defined in a `package.json`
            file as a child of the `scripts` key like so:
              "scripts": {
                "watch": "npx tailwindcss -i ./app/static/src/main.css -o ./app/static/dist/main.min.css --minify --watch"
                }
        """

        print("=== Starting TailwindCSS Compiler ===")

        cwd = os.getcwd()
        # Get folder where package.json is found
        app_parent_dir = str(Path(self.app.root_path).parent.parent)
        print(app_parent_dir)

        os.chdir(app_parent_dir)
        with open("package.json", encoding="utf-8") as f:
            package = json.load(f)
            try:
                cmd = package["scripts"][npm_script_name]
            except KeyError as e:
                raise ValueError(
                    f"No script with name '{npm_script_name}' "
                    "found in `package.json`."
                ) from e

        os.chdir(cwd)
        TailwindCompiler.proc = subprocess.Popen(cmd, shell=True)

        atexit.register(TailwindCompiler.terminate_on_exit)

    @classmethod
    def terminate_on_exit(cls):
        """Terminate the subprocess on exit."""
        print("=== Closing TailwindCSS Compiler ===")
        if cls.proc is not None:
            cls.proc.terminate()
            print("Closed! Bye")
