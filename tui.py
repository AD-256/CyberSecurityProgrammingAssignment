import logi
from textual.app import App
from textual import events
from textual.screen import Screen, ModalScreen
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Label, Footer, Header, Input

InfoScreenOption = 1

logi.DBCheck()

class InfoScreen(Screen):
    def compose(self):
        yield Header()
        yield Footer()
        global InfoScreenOption
        
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

LoginText = """\
Welcome to the Log in page! Here you can enter your account.
"""
class LoginScreen(Screen):
    def compose(self):
        yield Header()
        yield Footer()

        yield Container(
            Vertical(
                Label(LoginText),
                Input(placeholder="Username", type="text"),
                Input(placeholder="Password", type="text"),
                id="dialog"
            ),

            Horizontal(
                Button("Submit",id="LoginSubmit"),
                Button("Back",id="Back",variant="error")
            ),
            id="maincontain"
        )
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "LoginSubmit":
            print("hh")
        elif event.button.id == "Back":
            self.app.pop_screen()

SignupText = """\
Welcome to the Sign up page! Here you can create an account.

Your Password must have at least:
A total length of 8
1 Uppercase letter
1 Lowercase letter
1 Number
1 Symbol
"""
class SignupScreen(Screen):
    def compose(self):
        yield Header()
        yield Footer()

        yield Container(
            Vertical(
                Label(SignupText),
                Label("",id="errmsg"),
                Input(placeholder="Username", type="text",id="SignupUN"),
                Input(placeholder="Password", type="text",id="SignupPW",password=True),
                id="dialog"
            ),

            Horizontal(
                Button("Submit",id="SignupSubmit"),
                Button("Back",id="Back",variant="error")
            ),
            id="maincontain"
        )
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "SignupSubmit":
            x = logi.Signup(self.query_one("#SignupUN", Input).value,self.query_one("#SignupPW", Input).value)
            if x == 409:
                self.query_one("#errmsg", Label).update(f"[bold red]ERROR: An Accout Called {self.query_one("#SignupUN", Input).value} Already Exists")
            elif x == 0:
                self.query_one("#errmsg", Label).update(f"[bold green]Account Created!")
            elif x == 1:
                self.query_one("#errmsg", Label).update(f"[bold green]Account Created! [yellow]However, Your Password Is Weak")
            elif x == 411:
                self.query_one("#errmsg", Label).update(f"[bold red]ERROR: Your Password Does Not Meet The Listed Requirements")
            
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
        global InfoScreenOption
        if event.button.id == "exit":
            EsportsApp.exit(self)
        elif event.button.id == "login":
            self.push_screen(LoginScreen())
        elif event.button.id == "signup":
            self.push_screen(SignupScreen())
        elif event.button.id == "safecomms":
            InfoScreenOption = 1
            self.push_screen(InfoScreen())
        elif  event.button.id == "incident":
            InfoScreenOption = 2
            self.push_screen(InfoScreen())

if __name__ == "__main__":
    app = EsportsApp()
    app.run()