"""Flask web application for warehouse management"""
from flask import Flask, render_template, request, redirect, url_for
from varasto import Varasto


app = Flask(__name__)


class StorageManager:
    """Manages in-memory storage for multiple warehouses"""
    def __init__(self):
        self.storages = {}
        self.next_id = 1

    def add_storage(self, name, varasto):
        """Add a new storage and return its ID"""
        storage_id = self.next_id
        self.storages[storage_id] = {"name": name, "varasto": varasto}
        self.next_id += 1
        return storage_id

    def get_storage(self, storage_id):
        """Get a storage by ID"""
        return self.storages.get(storage_id)

    def delete_storage(self, storage_id):
        """Delete a storage by ID"""
        if storage_id in self.storages:
            del self.storages[storage_id]

    def get_all_storages(self):
        """Get all storages"""
        return self.storages


storage_manager = StorageManager()


@app.route("/")
def index():
    """Display all storages"""
    return render_template("index.html", storages=storage_manager.get_all_storages())


@app.route("/create", methods=["GET", "POST"])
def create_storage():
    """Create a new storage"""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        try:
            tilavuus = float(request.form.get("tilavuus", 0))
            alku_saldo = float(request.form.get("alku_saldo", 0))
        except ValueError:
            tilavuus = 0
            alku_saldo = 0

        if tilavuus > 0 and name:
            varasto = Varasto(tilavuus, alku_saldo)
            storage_manager.add_storage(name, varasto)
            return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/edit/<int:storage_id>", methods=["GET", "POST"])
def edit_storage(storage_id):
    """Edit an existing storage"""
    storage_data = storage_manager.get_storage(storage_id)
    if storage_data is None:
        return redirect(url_for("index"))

    if request.method == "POST":
        action = request.form.get("action")

        if action == "update":
            name = request.form.get("name", "").strip()
            if name:
                storage_data["name"] = name

        elif action == "add":
            try:
                amount = float(request.form.get("amount", 0))
                if amount > 0:
                    storage_data["varasto"].lisaa_varastoon(amount)
            except ValueError:
                pass

        elif action == "remove":
            try:
                amount = float(request.form.get("amount", 0))
                if amount > 0:
                    storage_data["varasto"].ota_varastosta(amount)
            except ValueError:
                pass

        return redirect(url_for("edit_storage", storage_id=storage_id))

    return render_template("edit.html", storage_id=storage_id, storage=storage_data)


@app.route("/delete/<int:storage_id>", methods=["POST"])
def delete_storage(storage_id):
    """Delete a storage"""
    storage_manager.delete_storage(storage_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=False)
