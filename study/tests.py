from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Assignment, Material, Test as TestModel


class CrudMixin:
    """Общий прогон полного CRUD для сущности."""

    basename = None
    create_data = {}
    update_data = {}
    patch_data = {}

    def url(self, name, *args):
        return reverse(f"{self.basename}-{name}", args=args)

    def test_crud(self):
        # create
        r = self.client.post(self.url("list"), self.create_data, format="json")
        self.assertEqual(r.status_code, 201, r.data)
        pk = r.data["id"]
        # list
        r = self.client.get(self.url("list"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["count"], 1)
        # retrieve
        r = self.client.get(self.url("detail", pk))
        self.assertEqual(r.status_code, 200)
        # full update
        r = self.client.put(self.url("detail", pk), self.update_data, format="json")
        self.assertEqual(r.status_code, 200, r.data)
        for k, v in self.update_data.items():
            self.assertEqual(r.data[k], v)
        # partial update
        r = self.client.patch(self.url("detail", pk), self.patch_data, format="json")
        self.assertEqual(r.status_code, 200, r.data)
        for k, v in self.patch_data.items():
            self.assertEqual(r.data[k], v)
        # delete
        self.assertEqual(self.client.delete(self.url("detail", pk)).status_code, 204)
        self.assertEqual(self.client.get(self.url("detail", pk)).status_code, 404)

    def test_title_required(self):
        r = self.client.post(self.url("list"), {}, format="json")
        self.assertEqual(r.status_code, 400)
        self.assertIn("title", r.data)


class MaterialTests(CrudMixin, APITestCase):
    basename = "material"
    create_data = {"title": "Intro", "content": "text", "url": "https://example.com"}
    update_data = {"title": "Intro v2", "description": "d", "content": "c", "url": ""}
    patch_data = {"title": "Intro v3"}

    def test_search(self):
        Material.objects.create(title="Python basics")
        Material.objects.create(title="Django ORM")
        r = self.client.get(self.url("list"), {"search": "django"})
        self.assertEqual(r.data["count"], 1)


class AssignmentTests(CrudMixin, APITestCase):
    basename = "assignment"
    create_data = {"title": "HW1", "max_score": 50, "due_date": "2030-01-01T10:00:00Z"}
    update_data = {"title": "HW1 v2", "description": "d", "max_score": 70, "due_date": None, "material": None}
    patch_data = {"max_score": 10}

    def test_material_link_and_filter(self):
        m1 = Material.objects.create(title="m1")
        m2 = Material.objects.create(title="m2")
        r = self.client.post(self.url("list"), {"title": "a", "material": m1.id}, format="json")
        self.assertEqual(r.status_code, 201)
        Assignment.objects.create(title="b", material=m2)
        r = self.client.get(self.url("list"), {"material": m1.id})
        self.assertEqual(r.data["count"], 1)

    def test_invalid_score(self):
        r = self.client.post(self.url("list"), {"title": "a", "max_score": 0}, format="json")
        self.assertEqual(r.status_code, 400)

    def test_material_delete_keeps_assignment(self):
        m = Material.objects.create(title="m")
        a = Assignment.objects.create(title="a", material=m)
        self.client.delete(reverse("material-detail", args=[m.id]))
        a.refresh_from_db()
        self.assertIsNone(a.material)


class TestEntityTests(CrudMixin, APITestCase):
    basename = "test"
    create_data = {"title": "Quiz 1", "time_limit_minutes": 30, "passing_score": 70}
    update_data = {
        "title": "Quiz 1 v2", "description": "d", "material": None,
        "time_limit_minutes": None, "passing_score": 80, "is_published": True,
    }
    patch_data = {"is_published": False}

    def test_passing_score_max(self):
        r = self.client.post(self.url("list"), {"title": "q", "passing_score": 101}, format="json")
        self.assertEqual(r.status_code, 400)

    def test_filter_by_material(self):
        m = Material.objects.create(title="m")
        TestModel.objects.create(title="a", material=m)
        TestModel.objects.create(title="b")
        r = self.client.get(self.url("list"), {"material": m.id})
        self.assertEqual(r.data["count"], 1)


class DocsTests(APITestCase):
    def test_schema_and_ui(self):
        r = self.client.get(reverse("schema"))
        self.assertEqual(r.status_code, 200)
        for p in ("materials", "assignments", "tests"):
            self.assertIn(f"/api/study/{p}/", r.data["paths"])
            self.assertIn(f"/api/study/{p}/{{id}}/", r.data["paths"])
        self.assertEqual(self.client.get(reverse("swagger-ui")).status_code, 200)
        self.assertEqual(self.client.get(reverse("redoc")).status_code, 200)
