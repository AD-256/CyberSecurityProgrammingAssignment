from textual.app import App
from textual import events
from textual.screen import Screen, ModalScreen
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Label, Footer, Header, Input


InfoScreenOption = 1

class InfoScreen(Screen):
    def compose(self):
        yield Header()
        yield Footer()
        
        if InfoScreenOption == 1:
            yield Container(
                Vertical(
                    Label("safecomms"),
                    id="dialog"),

                Horizontal(
                    Button("Back",id="Back",variant="error")),
                id="maincontain")
        else:
            yield Container(
                Vertical(
                    Label("incident"),
                    id="dialog"),

                Horizontal(
                    Button("Back",id="Back",variant="error")),
                id="maincontain")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "Back":
            self.app.pop_screen()

class LoginScreen(Screen):
    def compose(self):
        yield Header()
        yield Footer()

        yield Container(
            Vertical(
                Label("Test"),
                Input(placeholder="Username", type="text"),
                Input(placeholder="Password", type="text"),
                id="dialog"
            ),

            Horizontal(
                Button("Submit",id="SubmitLogin"),
                Button("Back",id="Back",variant="error")
            ),
            id="maincontain"
        )
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "SubmitLogin":
            print("hh")
        elif event.button.id == "Back":
            self.app.pop_screen()

SignupText = """\
Welcome to the Sign up page! Here you can create an account.

Your Password must have at least:
A total length of 8
1 Uppercase letter
1 Lowercase letter
1 Numer
1 Symbol
"""
class SignupScreen(Screen):
    def compose(self):
        yield Header()
        yield Footer()

        yield Container(
            Vertical(
                Label(SignupText),
                Input(placeholder="Username", type="text"),
                Input(placeholder="Password", type="text"),
                id="dialog"
            ),

            Horizontal(
                Button("Submit",id="SubmitSignup"),
                Button("Back",id="Back",variant="error")
            ),
            id="maincontain"
        )
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "SubmitSignup":
            print("hh")
        elif event.button.id == "Back":
            self.app.pop_screen()
        
    


IntroText = """\
Welcome to the Esports Cyber App, Designed to keep you safe.
"""
class EsportsApp(App):

    CSS_PATH = "Styles.tcss"

    def compose(self):
        self.title = "Esports Cyber App"
        self.ENABLE_COMMAND_PALETTE = False

        yield Header()
        yield Footer()

        yield Container(
            Vertical(
                Label(IntroText),
                id="dialog"
            ),
            
            Horizontal(
                Button("Log In",id="login"),
                Button("Sign Up",id="signup"),
                Button("Safe Communication",id="safecomms"),
                Button("Incident Response",id="incident"),
                Button("Exit",id="exit",variant="error")
            ),
            id="maincontain"
        )
        

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "exit":
            EsportsApp.exit(self)
        elif event.button.id == "login":
            self.push_screen(LoginScreen())
        elif event.button.id == "signup":
            self.push_screen(SignupScreen())
        elif event.button.id == "safecomms":
            global InfoScreenOption
            InfoScreenOption = 1
            self.push_screen(InfoScreen())
        elif  event.button.id == "incident":
            global InfoScreenOption
            InfoScreenOption = 2
            self.push_screen(InfoScreen())

if __name__ == "__main__":
    app = EsportsApp()
    app.run()