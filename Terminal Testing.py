from textual.app import App
from textual import events
from textual.widgets import Button


class MyApp(App):
    COLORS = [
        "white",
        "maroon",
        "red",
        "purple",
        "fuchsia",
        "olive",
        "yellow",
        "navy",
        "teal",
        "aqua",
    ]

    def on_mount(self) -> None:
        self.screen.styles.background = "darkblue"

    def on_key(self, event: events.Key) -> None:
        if event.key.isdecimal():
            self.screen.styles.background = self.COLORS[int(event.key)]
    def on_button_pressed(self) -> None:
        self.exit()


if __name__ == "__main__":
    app = MyApp()
    app.run()