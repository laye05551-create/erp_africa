from locust import HttpUser, task, between

class ERPAfricaUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Connexion automatique
        self.client.post("/", {
            "username": "abdoulaye",
            "password": "Dieynaba_20",
        })
    
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