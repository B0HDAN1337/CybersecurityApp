import webview
import requests
import webbrowser
import os

SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI" # test
SECRET_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe" # test

class ReCaptchaWindow:
    def __init__(self, on_solved):
        self.on_solved = on_solved
        self.api = self.ReCaptchaApi(self.on_solved)
        self.html = f"""
        <html>
          <head>
            <script src="https://www.google.com/recaptcha/api.js"></script>
          </head>
          <body>
            <form id="recaptcha-form">
              <div class="g-recaptcha" data-sitekey="{SITE_KEY}"></div>
              <br/>
              <input type="submit" value="Submit"/>
            </form>
            <script>
              document.getElementById('recaptcha-form').onsubmit = function(e) {{
                e.preventDefault();
                var response = grecaptcha.getResponse();
                if(response.length == 0) {{
                    alert("Please complete the CAPTCHA!");
                }} else {{
                    alert("CAPTCHA completed! Token: " + response);
                    window.pywebview.api.send_token(response);
                }}
              }}
            </script>
          </body>
        </html>
        """
        file = "recaptcha_test.html"
        file_path = os.path.abspath(file)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.html)

        webview.create_window("Google reCAPTCHA", url=f"http://localhost:8000/{file}", js_api=self.api)
        webview.start()    

    class ReCaptchaApi:
          def __init__(self, callback):
                self.callback = callback

          def send_token(self, token):
                  print("Token from reCAPTCHA:", token)
                  url = "https://www.google.com/recaptcha/api/siteverify"
                  data = {
                      "secret": SECRET_KEY,
                      "response": token
                  }
                  r = requests.post(url, data=data).json()
                  print("Verification result:", r)
                  if r.get("success"):
                      print("CAPTCHA verified!")
                      self.callback(True)
                  else:
                      print("CAPTCHA failed!")
                      self.callback(False)




