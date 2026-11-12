"""A four-command toolbox application built with quickli."""

from quickli import Application, Argument

from operations import copy_file, echo_text, make_directory, touch_file


app = Application(name="toolbox", description="File and text utilities.")

app.register(
    copy_file,
    name="cp",
    arguments=[Argument("source"), Argument("destination")],
)
app.register(
    make_directory,
    name="mkdir",
    arguments=[Argument("path")],
)
app.register(touch_file, name="touch", arguments=[Argument("path")])
app.register(echo_text, name="echo", arguments=[Argument("text")])


if __name__ == "__main__":
    raise SystemExit(app.main())
