import logi
from textual.app import App
from textual import events
from textual.screen import Screen, ModalScreen
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Label, Footer, Header, Input

InfoScreenOption = 1

logi.DBCheck()


class FunctionScreen(Screen):
    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        username: str = None,
    ) -> None:
        super().__init__(name, id, classes)

        self.user = username

    def update_buttons(self):
        
        if logi.CheckForMFA(self.user) == None:
            self.query_one("#Toggle", Button).label = "Enable MFA"
            self.query_one("#KeyLabel", Label).update("")
        else:
            self.query_one("#Toggle", Button).label = "Disable MFA"
            self.query_one("#KeyLabel", Label).update(f"MFA Key:\n{logi.CheckForMFA(self.user)}\nKEEP THIS SAFE INSIDE YOUR AUTHENTICATOR")

    def compose(self):

        FunctionText = f"""
        Hello {self.user} Welcome to the Esports Cyber App!
        Here you can enable 2FA using your mobile.
        """
        
        yield Header(icon="")

        yield Container(
                Vertical(
                    Label(FunctionText),
                id="dialog"),

                Horizontal(
                        Button("Enable MFA", id="Toggle"),
                        Label(f"MFA Key:\n{logi.CheckForMFA(self.user)}\nKEEP THIS SAFE INSIDE YOUR AUTHENTICATOR",id="KeyLabel")
                ),
                
                Horizontal(
                    Button("Logout",id="Back",classes="Exit"),
                classes="Buttons"),
                id="maincontain")
        
    def on_mount(self, event):
            self.update_buttons()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "Back":
            self.app.pop_screen()
        elif event.button.id == "Toggle":
            if logi.CheckForMFA(self.user) is None:
                logi.EnableMFA(self.user)
                
            else:
                logi.DisableMFA(self.user)
            self.update_buttons()

class InfoScreen(Screen):

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        option: str = 1,
    ) -> None:
        super().__init__(name, id, classes)

        self.option = option

    def compose(self):

        SafeCommsText = """
        Safe Communication Online.

        1, Never share your password.
        2, Never share any personal data like home address or phone number
        3, Definitely never share any banking details or data such as your National Insurance Number
        """

        IncidentText = """
        Incident Response and Recovery Plans
        addressing security breaches
        recovery procedures to minimize downtime and user impact
        Lorem
        Ipsum
        Dolor
        """

        yield Header(icon="")

        if self.option == 1:
            self.option = SafeCommsText
        else:
            self.option = IncidentText

        yield Container(
            Vertical(
                Label(self.option),
            id="dialog"),

            Horizontal(
                Button("Back",id="Back",classes="Exit"),
            classes="Buttons"),
            id="maincontain")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "Back":
            self.app.pop_screen()

class LoginScreen(Screen):

    def update_inputs(self):
        if logi.CheckForMFA(self.query_one("#LoginUN", Input).value) == None:self.query_one("#LoginMFA", Input).display = False
        else:self.query_one("#LoginMFA", Input).display = True

    def compose(self):

        LoginText = """\
        Welcome to the Log in page! Here you can enter your account.
        """

        yield Header(icon="")

        yield Container(
            Vertical(
                Vertical(
                    Label(LoginText),
                    Label("",id="errmsg"),
                ),
                Vertical(
                    Input(placeholder="Username",id="LoginUN", type="text"),
                    Input(placeholder="Password",id="LoginPW", type="text",password=True),
                    Input(placeholder="MFA Token",id="LoginMFA", type="text")
                ),
                id="dialog"
            ),

            Horizontal(
                Button("Submit",id="LoginSubmit"),
                Button("Back",id="Back",classes="Exit"),
            classes="Buttons"),
            id="maincontain"
        )

    def on_mount(self, event):
            self.update_inputs()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "LoginSubmit":
            username = self.query_one("#LoginUN", Input).value
            password = self.query_one("#LoginPW", Input).value
            x = logi.Login(username,password)
            if x == 0:
                self.update_inputs()
                if logi.CheckForMFA(username) == None:
                    self.app.push_screen(FunctionScreen(username=username))
                else:
                    if logi.MFALogin(username,password,self.query_one("#LoginMFA", Input).value):
                        self.app.push_screen(FunctionScreen(username=username))
            elif x == 411:
                self.query_one("#errmsg", Label).update(f"[bold red]ERROR: Incorrect Credentials")
            elif x == 404:
                self.query_one("#errmsg", Label).update(f"[bold red]ERROR: No Account Found")
        elif event.button.id == "Back":
            self.app.pop_screen()

class SignupScreen(Screen):

    def compose(self):

        SignupText = """
        Welcome to the Sign up page! Here you can create an account.

        Your Password must have at least:
        A total length of 8
        1 Uppercase letter
        1 Lowercase letter
        1 Number
        1 Symbol
        """

        yield Header(icon="")

        yield Container(
            Vertical(
                Vertical(
                    Label(SignupText),
                    Label("",id="errmsg"),
                ),
                Vertical(
                    Input(placeholder="Username", type="text",id="SignupUN"),
                    Input(placeholder="Password", type="text",id="SignupPW",password=True),
                ),
                id="dialog"
            ),

            Horizontal(
                Button("Submit",id="SignupSubmit"),
                Button("Back",id="Back",classes="Exit"),
            classes="Buttons"),
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
    
        

class EsportsApp(App):

    CSS_PATH = "Styles.tcss"

    def compose(self):

        IntroText = """\
        Welcome to the Esports Cyber App, Designed to keep you safe.
        """

        self.title = "Esports Cyber App"
        self.ENABLE_COMMAND_PALETTE = False

        yield Header(icon="")

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
                Button("Exit",id="exit",classes="Exit"),
            classes="Buttons"),
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
            self.push_screen(InfoScreen(option=1))
        elif  event.button.id == "incident":
            self.push_screen(InfoScreen(option=2))

if __name__ == "__main__":
    app = EsportsApp()
    app.run()