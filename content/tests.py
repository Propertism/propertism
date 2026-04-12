import shutil
import tempfile
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import OperationalError
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from .models import BlogPost, CompanyInfo, CustomerReview, CustomerReviewSection, HeroBackgroundImage, LandingLead


TEST_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
    b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00"
    b"\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)


def make_test_image(name):
    return SimpleUploadedFile(name, TEST_GIF, content_type="image/gif")


class HeroBackgroundImageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temp_media_root = tempfile.mkdtemp(prefix="propertism-test-media-")
        cls._media_override = override_settings(MEDIA_ROOT=cls._temp_media_root)
        cls._media_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls._media_override.disable()
        shutil.rmtree(cls._temp_media_root, ignore_errors=True)

    def setUp(self):
        self.company = CompanyInfo.objects.create(company_name="Propertism Realty Advisors LLP")

    def test_company_is_limited_to_five_hero_background_images(self):
        for index in range(5):
            HeroBackgroundImage.objects.create(
                company=self.company,
                image=make_test_image(f"hero-{index}.gif"),
                order=index,
            )

        with self.assertRaises(ValidationError):
            HeroBackgroundImage.objects.create(
                company=self.company,
                image=make_test_image("hero-5.gif"),
                order=5,
            )


class HomePageContentTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temp_media_root = tempfile.mkdtemp(prefix="propertism-test-media-")
        cls._media_override = override_settings(MEDIA_ROOT=cls._temp_media_root)
        cls._media_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls._media_override.disable()
        shutil.rmtree(cls._temp_media_root, ignore_errors=True)

    def setUp(self):
        self.company = CompanyInfo.objects.create(company_name="Propertism Realty Advisors LLP")
        self.review_section = CustomerReviewSection.objects.create(
            title="What Our Customers Say",
            is_active=True,
        )
        for index in range(4):
            CustomerReview.objects.create(
                section=self.review_section,
                customer_name=f"Customer {index + 1}",
                quote=f"Review copy {index + 1}",
                order=index,
                is_active=True,
            )

    def test_homepage_groups_reviews_into_slides_of_three(self):
        response = self.client.get(reverse("home"), follow=True)

        self.assertEqual(response.status_code, 200)
        slides = response.context["customer_review_slides"]
        self.assertEqual(len(slides), 2)
        self.assertEqual(len(slides[0]), 3)
        self.assertEqual(len(slides[1]), 1)
        self.assertContains(response, 'data-review-carousel')

    def test_homepage_exposes_rotating_hero_background_urls(self):
        HeroBackgroundImage.objects.create(
            company=self.company,
            image=make_test_image("hero-a.gif"),
            order=0,
        )
        HeroBackgroundImage.objects.create(
            company=self.company,
            image=make_test_image("hero-b.gif"),
            order=1,
        )

        response = self.client.get(reverse("home"), follow=True)

        self.assertEqual(len(response.context["hero_background_urls"]), 2)

    def test_homepage_uses_companyinfo_for_section_and_chat_copy(self):
        self.company.about_section_title = "Model Driven About Title"
        self.company.services_section_title = "Model Driven Services"
        self.company.management_section_title = "Model Driven Management"
        self.company.blog_section_title = "Model Driven Blog"
        self.company.contact_section_title = "Model Driven Contact"
        self.company.footer_newsletter_heading = "Newsletter From Admin"
        self.company.chat_window_title = "Chat From Admin"
        self.company.chat_success_message = "Admin controlled success copy."
        self.company.save()

        response = self.client.get(reverse("home"), follow=True)

        self.assertContains(response, "Model Driven About Title")
        self.assertContains(response, "Model Driven Services")
        self.assertContains(response, "Model Driven Management")
        self.assertContains(response, "Model Driven Blog")
        self.assertContains(response, "Model Driven Contact")
        self.assertContains(response, "Newsletter From Admin")
        self.assertContains(response, "Chat From Admin")
        self.assertContains(response, "Admin controlled success copy.")

    @patch("content.views.Statistic.objects.filter", side_effect=OperationalError("no such table"))
    def test_homepage_gracefully_handles_missing_statistics_table(self, _mock_stats_filter):
        response = self.client.get(reverse("home"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["stats"], [])

    @patch("content.views.TeamMember.objects.filter", side_effect=OperationalError("no such table"))
    def test_team_member_detail_returns_404_when_table_is_unavailable(self, _mock_team_filter):
        response = self.client.get(reverse("team_member_detail", args=["missing-slug"]), follow=True)

        self.assertEqual(response.status_code, 404)


class SitemapTests(TestCase):
    def test_sitemap_renders_published_blog_posts_without_server_error(self):
        BlogPost.objects.create(
            title="Chennai Property Update",
            slug="chennai-property-update",
            excerpt="Short summary",
            content="Detailed content",
            is_published=True,
        )

        response = self.client.get(reverse("django.contrib.sitemaps.views.sitemap"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/blog/chennai-property-update/")


class LandingLeadApiTests(TestCase):
    def test_landing_lead_api_stores_qualified_sell_lead(self):
        response = self.client.post(
            reverse("landing_lead_api"),
            {
                "phone": "+919999999999",
                "property_city": "Chennai",
                "intent_type": "sell",
                "property_type": "villa",
                "selling_timeline": "30-days",
                "geo_origin": "dubai-uae",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(LandingLead.objects.count(), 1)

        lead = LandingLead.objects.get()
        self.assertEqual(lead.intent_type, "sell")
        self.assertEqual(lead.lead_stage, "qualified")
        self.assertEqual(lead.geo_origin, "dubai-uae")
        self.assertEqual(lead.qualification_data["selling_timeline"], "30-days")
        self.assertEqual(lead.lead_category, "hot")
