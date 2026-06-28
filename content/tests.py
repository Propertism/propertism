from pathlib import Path
import shutil
from unittest.mock import patch
from uuid import uuid4

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import OperationalError
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from .models import (
    BlogPost,
    CompanyInfo,
    CustomerReview,
    CustomerReviewSection,
    HERO_IMAGE_NAME_ALIASES,
    HeroBackgroundImage,
    LandingLead,
)


TEST_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
    b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00"
    b"\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)


def make_test_image(name):
    return SimpleUploadedFile(name, TEST_GIF, content_type="image/gif")


def make_test_media_root():
    media_root_parent = Path(settings.BASE_DIR) / ".tmp-test-media"
    media_root_parent.mkdir(exist_ok=True)
    media_root = media_root_parent / f"propertism-test-media-{uuid4().hex}"
    media_root.mkdir()
    return str(media_root)


class HeroBackgroundImageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temp_media_root = make_test_media_root()
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
        cls._temp_media_root = make_test_media_root()
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

    def test_homepage_groups_reviews_into_slides_of_six(self):
        response = self.client.get(reverse("home"), follow=True)

        self.assertEqual(response.status_code, 200)
        slides = response.context["customer_review_slides"]
        self.assertEqual(len(slides), 1)
        self.assertEqual(len(slides[0]), 4)
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

    def test_homepage_skips_missing_hero_backgrounds_and_uses_company_fallback(self):
        self.company.hero_image = make_test_image("fallback-hero.gif")
        self.company.save(update_fields=["hero_image"])

        missing_hero = HeroBackgroundImage.objects.create(
            company=self.company,
            image=make_test_image("hero-missing-source.gif"),
            order=0,
        )
        HeroBackgroundImage.objects.filter(pk=missing_hero.pk).update(image="hero/does-not-exist.gif")

        response = self.client.get(reverse("home"), follow=True)

        self.assertEqual(response.context["hero_background_urls"], [self.company.hero_image.url])

    def test_homepage_repairs_known_stale_hero_aliases(self):
        stale_name, canonical_name = next(iter(HERO_IMAGE_NAME_ALIASES.items()))
        canonical_basename = canonical_name.split("/", 1)[1]

        repaired_hero = HeroBackgroundImage.objects.create(
            company=self.company,
            image=make_test_image(canonical_basename),
            order=0,
        )
        HeroBackgroundImage.objects.filter(pk=repaired_hero.pk).update(image=stale_name)

        response = self.client.get(reverse("home"), follow=True)

        self.assertEqual(response.context["hero_background_urls"], [f"/media/{canonical_name}"])

    def test_homepage_uses_companyinfo_for_section_and_chat_copy(self):
        self.company.contact_section_eyebrow = "Talk With Us"
        self.company.footer_services_heading = "Custom Service Coverage"
        self.company.footer_newsletter_button_text = "Join Updates"
        self.company.chat_window_title = "Chat From Admin"
        self.company.chat_success_message = "Admin controlled success copy."
        self.company.save()

        response = self.client.get(reverse("home"), follow=True)

        self.assertContains(response, "Talk With Us")
        self.assertContains(response, "Custom Service Coverage")
        self.assertContains(response, "Join Updates")
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

    @override_settings(CANONICAL_HOST="www.propertism.in", CANONICAL_SCHEME="https")
    def test_sitemap_uses_canonical_https_host_even_if_site_row_is_stale(self):
        Site.objects.update_or_create(
            id=settings.SITE_ID,
            defaults={"domain": "example.com", "name": "example.com"},
        )

        response = self.client.get(reverse("django.contrib.sitemaps.views.sitemap"))
        body = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("https://www.propertism.in/", body)
        self.assertNotIn("<loc>http://", body)
        self.assertNotIn("example.com", body)

    @override_settings(
        ADMIN_URL="admin",
        CANONICAL_HOST="www.propertism.in",
        CANONICAL_SCHEME="https",
    )
    def test_robots_txt_uses_canonical_https_sitemap(self):
        response = self.client.get(reverse("robots"))
        body = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Sitemap: https://www.propertism.in/sitemap.xml", body)
        self.assertIn("Disallow: /admin/", body)
        self.assertNotIn("http://", body)


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


class PropertyOwnerResourcesTests(TestCase):
    def setUp(self):
        self.company = CompanyInfo.objects.create(company_name="Propertism Realty Advisors LLP")

    def test_property_owner_resources_view_returns_200(self):
        response = self.client.get(reverse("property_owner_resources"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tamil Nadu Property Owner Resources")
        self.assertContains(response, "Official Government Services Directory")
        self.assertContains(response, "Legal Disclaimer")
        self.assertContains(response, "Propertism provides links to official Tamil Nadu Government services")
        # Check canonical URL override
        self.assertContains(response, 'rel="canonical" href="https://www.propertism.in/property-owner-resources/"')


class LinkRoutingTests(TestCase):
    def setUp(self):
        self.company = CompanyInfo.objects.create(company_name="Propertism Realty Advisors LLP")

    def test_core_pages_route_correctly(self):
        core_pages = [
            ("home", {}),
            ("services", {}),
            ("about", {}),
            ("management", {}),
            ("contact", {}),
            ("property_owner_resources", {}),
            ("blog", {}),
        ]
        for name, kwargs in core_pages:
            response = self.client.get(reverse(name, kwargs=kwargs))
            self.assertIn(response.status_code, [200, 302], f"Page {name} failed with status {response.status_code}")

    def test_city_hubs_route_correctly(self):
        for city in ["chennai", "bangalore", "hyderabad"]:
            response = self.client.get(reverse("city_hub", kwargs={"city_slug": city}))
            self.assertEqual(response.status_code, 200, f"City hub /{city}/ failed with status {response.status_code}")

    def test_seo_landing_pages_route_correctly(self):
        # Test a few main intents for Chennai
        intents = ["nri-sell-property", "nri-property-management", "nri-rental-management"]
        for intent in intents:
            response = self.client.get(reverse("landing_page", kwargs={"city_slug": "chennai", "intent_slug": intent}))
            self.assertEqual(response.status_code, 200, f"Landing page /chennai/{intent}/ failed with status {response.status_code}")

    def test_nri_landing_pages_route_correctly(self):
        # Test a few NRI location pages
        locations = ["new-york-usa", "london-uk", "dubai-uae", "toronto-canada"]
        for loc in locations:
            response = self.client.get(reverse("nri_landing_page", kwargs={"nri_location_slug": loc, "geo_slug": "chennai-nri-property-management"}))
            self.assertEqual(response.status_code, 200, f"NRI page /{loc}/chennai-nri-property-management/ failed with status {response.status_code}")


class SeoTagsFilterTests(TestCase):
    def test_name_only_and_quals_only_with_pipe(self):
        from content.templatetags.seo_tags import name_only, quals_only
        self.assertEqual(name_only("Mr. Tamilselvan | BE, MBA"), "Mr. Tamilselvan")
        self.assertEqual(quals_only("Mr. Tamilselvan | BE, MBA"), "BE, MBA")

        self.assertEqual(name_only("Mr. Tamilselvan | BE"), "Mr. Tamilselvan")
        self.assertEqual(quals_only("Mr. Tamilselvan | BE"), "BE")

        self.assertEqual(name_only("Mr. Tamilselvan"), "Mr. Tamilselvan")
        self.assertEqual(quals_only("Mr. Tamilselvan"), "")

    def test_name_only_and_quals_only_fallback(self):
        from content.templatetags.seo_tags import name_only, quals_only
        self.assertEqual(name_only("Mr. Tamilselvan B.E, M.B.A."), "Mr. Tamilselvan")
        self.assertEqual(quals_only("Mr. Tamilselvan B.E, M.B.A."), "B.E, M.B.A.")


class PseoRemediationTests(TestCase):
    def test_h1_differentiation_is_unique(self):
        from content.pseo_enrichment import build_differentiated_h1
        nri1 = {"name": "New York", "label": "New York, USA", "region": "USA"}
        nri2 = {"name": "San Jose, CA", "label": "San Jose, CA", "region": "USA"}
        
        h1_1 = build_differentiated_h1("sell", "Chennai", "chennai", nri_location=nri1, intent_slug="nri-sell-property")
        h1_2 = build_differentiated_h1("sell", "Chennai", "chennai", nri_location=nri2, intent_slug="nri-sell-property")
        
        self.assertNotEqual(h1_1, h1_2)
        self.assertIn("New York", h1_1)
        self.assertIn("San Jose", h1_2)

    def test_title_differentiation_is_unique(self):
        from content.pseo_enrichment import build_differentiated_title
        config = {"intent_slug": "nri-property-management", "property_type_label": "Property Management"}
        city = {"name": "Chennai"}
        nri1 = {"name": "New York"}
        nri2 = {"name": "London"}
        
        t1 = build_differentiated_title(config, city, nri1)
        t2 = build_differentiated_title(config, city, nri2)
        
        self.assertNotEqual(t1, t2)
        self.assertIn("New York", t1)
        self.assertIn("London", t2)

    def test_description_differentiation_fits_limit(self):
        from content.pseo_enrichment import build_differentiated_description
        config = {"intent_slug": "nri-property-management"}
        city = {"name": "Chennai"}
        nri = {"name": "New York"}
        
        desc = build_differentiated_description(config, city, nri)
        self.assertTrue(140 <= len(desc) <= 160, f"Description length is {len(desc)}")


class BlogPostEEATTests(TestCase):
    def test_blog_post_author_profile_lookup(self):
        post = BlogPost.objects.create(
            title="Test Post",
            slug="test-post-slug",
            author="Propertism Advisory Team",
            content="Hello world",
            is_published=True,
        )
        self.assertEqual(post.author_profile["name"], "Propertism Advisory Team")
        self.assertEqual(post.author_profile["role"], "Senior NRI Property Advisors")

        # Fallback profile for unknown authors
        post2 = BlogPost.objects.create(
            title="Test Post 2",
            slug="test-post-slug-2",
            author="Unknown Author",
            content="Hello world",
            is_published=True,
        )
        self.assertEqual(post2.author_profile["name"], "Propertism Advisory Team")

    def test_blog_post_faq_items_parsing(self):
        post_content = """
        This is some introduction text.
        <h2>Frequently Asked Questions</h2>
        <strong>What is the processing time?</strong>
        It usually takes 3-5 business days depending on documentation verification.
        <strong>Can I apply online?</strong>
        Yes, you can apply using the online client portal.
        """
        post = BlogPost.objects.create(
            title="Test Post 3",
            slug="test-post-slug-3",
            author="Propertism Team",
            content=post_content,
            is_published=True,
        )
        faqs = post.faq_items
        self.assertEqual(len(faqs), 2)
        self.assertEqual(faqs[0]["question"], "What is the processing time?")
        self.assertEqual(faqs[0]["answer"], "It usually takes 3-5 business days depending on documentation verification.")
        self.assertEqual(faqs[1]["question"], "Can I apply online?")
        self.assertEqual(faqs[1]["answer"], "Yes, you can apply using the online client portal.")


class TamilselvanContactDetailsTests(TestCase):
    def setUp(self):
        # Create company info which is needed for the team view
        CompanyInfo.objects.create(company_name="Propertism Realty Advisors LLP")
        
    def test_tamilselvan_contact_details_render(self):
        from content.models import TeamMember
        # Create a TeamMember for Tamilselvan
        TeamMember.objects.create(
            name="Mr. Tamilselvan",
            slug="mr-tamilselvan",
            role="Managing Partner",
            department="Property Acquisition & Management",
            bio="Test bio info",
            expertise="Land Acquisitions, Property Management",
            is_active=True
        )
        
        # Test rendering of contact info
        with self.settings(
            TAMILSELVAN_EMAIL_1="info@propertism.in",
            TAMILSELVAN_EMAIL_2="propertism.tamil@gmail.com"
        ):
            response = self.client.get(reverse("team_member_detail", kwargs={"slug": "mr-tamilselvan"}))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "info@propertism.in")
            self.assertContains(response, "propertism.tamil@gmail.com")
            self.assertContains(response, "https://www.linkedin.com/in/stamilselvan/")
            self.assertContains(response, "https://www.linkedin.com/company/propertism/?viewAsMember=true")



