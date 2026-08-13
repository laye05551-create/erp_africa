from locust import HttpUser, task, between

class ERPAfricaUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # 1. Charger la vraie page de connexion pour récupérer le cookie CSRF
        res_get = self.client.get("/login/")
        csrf_token = res_get.cookies.get("csrftoken", "")

        # 2. Soumettre le formulaire sur /login/ en autorisant la redirection
        self.client.post(
            "/login/",
            data={
                "username": "abdoulaye",
                "password": "Dieynaba_20",
                "csrfmiddlewaretoken": csrf_token,
            },
            headers={
                "X-CSRFToken": csrf_token,
                "Referer": self.host + "/login/",
            },
            allow_redirects=True
        )

    @task(3)
    def dashboard(self):
        self.client.get("/dashboard/")

    @task(2)
    def liste_factures(self):
        self.client.get("/factures/")

    @task(2)
    def liste_stocks(self):
        self.client.get("/stocks/")

    @task(1)
    def liste_clients(self):
        self.client.get("/clients/")

    @task(1)
    def comptabilite(self):
        self.client.get("/comptabilite/")