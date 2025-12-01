"""Tests for Flask web application"""
import unittest
from app import app, storage_manager


class TestApp(unittest.TestCase):
    """Test cases for Flask app routes"""

    def setUp(self):
        """Set up test client and clear storages"""
        self.client = app.test_client()
        app.config["TESTING"] = True
        storage_manager.storages.clear()
        storage_manager.next_id = 1

    def test_index_empty(self):
        """Test index page with no storages"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Warehouse Management", response.data)
        self.assertIn(b"Create Storage", response.data)

    def test_create_storage_page(self):
        """Test create storage page loads"""
        response = self.client.get("/create")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create New Storage", response.data)

    def test_create_storage_post(self):
        """Test creating a new storage"""
        response = self.client.post("/create", data={
            "name": "Test Storage",
            "tilavuus": "100",
            "alku_saldo": "50"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Storage", response.data)
        self.assertEqual(len(storage_manager.storages), 1)

    def test_create_storage_invalid_capacity(self):
        """Test creating storage with invalid capacity"""
        response = self.client.post("/create", data={
            "name": "Test Storage",
            "tilavuus": "0",
            "alku_saldo": "0"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(storage_manager.storages), 0)

    def test_edit_storage_page(self):
        """Test edit storage page loads"""
        # First create a storage
        self.client.post("/create", data={
            "name": "Test Storage",
            "tilavuus": "100",
            "alku_saldo": "50"
        })
        response = self.client.get("/edit/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit Storage", response.data)

    def test_edit_storage_not_found(self):
        """Test editing non-existent storage redirects"""
        response = self.client.get("/edit/999", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Warehouse Management", response.data)

    def test_edit_storage_update_name(self):
        """Test updating storage name"""
        self.client.post("/create", data={
            "name": "Original Name",
            "tilavuus": "100",
            "alku_saldo": "0"
        })
        response = self.client.post("/edit/1", data={
            "action": "update",
            "name": "New Name"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(storage_manager.storages[1]["name"], "New Name")

    def test_edit_storage_add_content(self):
        """Test adding content to storage"""
        self.client.post("/create", data={
            "name": "Test Storage",
            "tilavuus": "100",
            "alku_saldo": "0"
        })
        self.client.post("/edit/1", data={
            "action": "add",
            "amount": "25"
        })
        self.assertEqual(storage_manager.storages[1]["varasto"].saldo, 25)

    def test_edit_storage_remove_content(self):
        """Test removing content from storage"""
        self.client.post("/create", data={
            "name": "Test Storage",
            "tilavuus": "100",
            "alku_saldo": "50"
        })
        self.client.post("/edit/1", data={
            "action": "remove",
            "amount": "20"
        })
        self.assertEqual(storage_manager.storages[1]["varasto"].saldo, 30)

    def test_delete_storage(self):
        """Test deleting a storage"""
        self.client.post("/create", data={
            "name": "Test Storage",
            "tilavuus": "100",
            "alku_saldo": "0"
        })
        self.assertEqual(len(storage_manager.storages), 1)
        response = self.client.post("/delete/1", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(storage_manager.storages), 0)

    def test_delete_nonexistent_storage(self):
        """Test deleting non-existent storage"""
        response = self.client.post("/delete/999", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
