from cleo import Command


class GreetCommand(Command):
    """
    Greets someone

    startproject
        {name? : Who do you want to greet?}
        {--y|yell : If set, the task will yell in uppercase letters}
    """

    def handle(self):
        name = self.argument("name")

        if name:
            text = "Hello {}".format(name)
        else:
            text = "Hello"

        if self.option("yell"):
            text = text.upper()
        self.line("<error>foo</error>")
        self.line("<fg=green>foo</>")
        self.line("<question>foo</question>")
        self.add_style("fire", fg="red", bg="yellow", options=["bold", "blink"])
        self.line("<fire>foo</fire>")
        self.line("<fg=black;bg=cyan>foo</>")
