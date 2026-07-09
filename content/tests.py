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
    @patch("realtor_project.features.is_feature_enabled")
    def test_landing_lead_api_stores_qualified_sell_lead(self, mock_is_feature_enabled):
        mock_is_feature_enabled.side_effect = lambda flag, default=True: False if flag == "CAPTCHA_ENABLE" else True
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


class CaptchaVerificationTests(TestCase):
    def setUp(self):
        from content.models import CompanyInfo
        CompanyInfo.objects.create(company_name="Propertism Realty Advisors LLP")
        from django.core.cache import cache
        cache.clear()

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="info@propertism.in",
        ADMIN_EMAIL="info@propertism.in",
        EXTRA_NOTIFICATION_EMAIL="propertism.tamil@gmail.com",
    )
    @patch("content.views.send_whatsapp_notification")
    @patch("realtor_project.features.is_feature_enabled")
    def test_captcha_disabled_submits_normally(self, mock_is_feature_enabled, mock_send_whatsapp):
        # When CAPTCHA is disabled, form should submit without reCAPTCHA tokens
        mock_is_feature_enabled.side_effect = lambda flag, default=True: False if flag == "CAPTCHA_ENABLE" else True
        
        from properties.models import Inquiry
        self.assertEqual(Inquiry.objects.count(), 0)

        response = self.client.post(
            reverse("contact"),
            data={
                "name": "Genuine User",
                "email": "genuine@example.com",
                "phone": "+919876543210",
                "message": "Interested in properties in OMR",
                "form_source": "General Inquiry",
            }
        )

        self.assertEqual(response.status_code, 302)  # Successful submit redirects
        self.assertEqual(Inquiry.objects.count(), 1)
        inquiry = Inquiry.objects.first()
        self.assertEqual(inquiry.name, "Genuine User")

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="info@propertism.in",
        ADMIN_EMAIL="info@propertism.in",
        RECAPTCHA_SECRET_KEY="dummy-secret",
    )
    @patch("content.views.send_whatsapp_notification")
    @patch("realtor_project.features.is_feature_enabled")
    def test_captcha_enabled_missing_token_fails(self, mock_is_feature_enabled, mock_send_whatsapp):
        # When CAPTCHA is enabled, missing or invalid token should fail validation
        mock_is_feature_enabled.side_effect = lambda flag, default=True: True if flag == "CAPTCHA_ENABLE" else True
        
        from properties.models import Inquiry
        self.assertEqual(Inquiry.objects.count(), 0)

        response = self.client.post(
            reverse("contact"),
            data={
                "name": "Anonymous User",
                "email": "anon@example.com",
                "phone": "+919876543210",
                "message": "Testing reCAPTCHA validation",
                "form_source": "General Inquiry",
            }
        )

        # It should render the page with an error instead of redirecting
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home-premium.html")
        self.assertEqual(Inquiry.objects.count(), 0)

        # Check that SpamLog is created for the failure
        from content.models import SpamLog
        self.assertEqual(SpamLog.objects.count(), 1)
        spam_log = SpamLog.objects.first()
        self.assertEqual(spam_log.failure_reason, "captcha-failed")
        self.assertIn("missing-input-response", spam_log.google_error_code)

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="info@propertism.in",
        ADMIN_EMAIL="info@propertism.in",
        RECAPTCHA_SECRET_KEY="dummy-secret",
    )
    @patch("content.views.send_whatsapp_notification")
    @patch("realtor_project.features.is_feature_enabled")
    @patch("content.security.google_recaptcha.GoogleRecaptchaV2.verify")
    def test_captcha_enabled_valid_token_submits(self, mock_verify, mock_is_feature_enabled, mock_send_whatsapp):
        # Mock reCAPTCHA verification to pass
        from content.security.google_recaptcha import RecaptchaResult
        mock_verify.return_value = RecaptchaResult(success=True, hostname="localhost")
        
        mock_is_feature_enabled.side_effect = lambda flag, default=True: True if flag == "CAPTCHA_ENABLE" else True
        
        from properties.models import Inquiry
        self.assertEqual(Inquiry.objects.count(), 0)

        response = self.client.post(
            reverse("contact"),
            data={
                "name": "Genuine Human",
                "email": "human@example.com",
                "phone": "+919876543210",
                "message": "Interested in properties in OMR",
                "form_source": "General Inquiry",
                "g-recaptcha-response": "valid-token-mock",
            }
        )

        self.assertEqual(response.status_code, 302)  # Successful submit redirects
        self.assertEqual(Inquiry.objects.count(), 1)
        inquiry = Inquiry.objects.first()
        self.assertEqual(inquiry.name, "Genuine Human")

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="info@propertism.in",
        ADMIN_EMAIL="info@propertism.in",
    )
    @patch("content.views.send_whatsapp_notification")
    @patch("realtor_project.features.is_feature_enabled")
    def test_newsletter_captcha_disabled_submits_normally(self, mock_is_feature_enabled, mock_send_whatsapp):
        mock_is_feature_enabled.side_effect = lambda flag, default=True: False if flag == "CAPTCHA_ENABLE" else True
        
        from content.models import Newsletter
        Newsletter.objects.filter(email='newsletter@example.com').delete()
        
        response = self.client.post(
            reverse("newsletter_subscribe"),
            data={"email": "newsletter@example.com"}
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Newsletter.objects.filter(email='newsletter@example.com').exists())
        Newsletter.objects.filter(email='newsletter@example.com').delete()

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="info@propertism.in",
        ADMIN_EMAIL="info@propertism.in",
        RECAPTCHA_SECRET_KEY="dummy-secret",
    )
    @patch("content.views.send_whatsapp_notification")
    @patch("realtor_project.features.is_feature_enabled")
    def test_newsletter_captcha_enabled_missing_token_fails(self, mock_is_feature_enabled, mock_send_whatsapp):
        mock_is_feature_enabled.side_effect = lambda flag, default=True: True if flag == "CAPTCHA_ENABLE" else True
        
        from content.models import Newsletter
        Newsletter.objects.filter(email='newsletter@example.com').delete()
        
        response = self.client.post(
            reverse("newsletter_subscribe"),
            data={"email": "newsletter@example.com"}
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Newsletter.objects.filter(email='newsletter@example.com').exists())

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="info@propertism.in",
        ADMIN_EMAIL="info@propertism.in",
        RECAPTCHA_SECRET_KEY="dummy-secret",
    )
    @patch("content.views.send_whatsapp_notification")
    @patch("realtor_project.features.is_feature_enabled")
    @patch("content.security.google_recaptcha.GoogleRecaptchaV2.verify")
    def test_newsletter_captcha_enabled_valid_token_submits(self, mock_verify, mock_is_feature_enabled, mock_send_whatsapp):
        from content.security.google_recaptcha import RecaptchaResult
        mock_verify.return_value = RecaptchaResult(success=True, hostname="localhost")
        
        mock_is_feature_enabled.side_effect = lambda flag, default=True: True if flag == "CAPTCHA_ENABLE" else True
        
        from content.models import Newsletter
        Newsletter.objects.filter(email='newsletter@example.com').delete()
        
        response = self.client.post(
            reverse("newsletter_subscribe"),
            data={
                "email": "newsletter@example.com",
                "g-recaptcha-response": "valid-token-mock",
            }
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Newsletter.objects.filter(email='newsletter@example.com').exists())
        Newsletter.objects.filter(email='newsletter@example.com').delete()

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="info@propertism.in",
        ADMIN_EMAIL="info@propertism.in",
    )
    @patch("content.views.send_landing_lead_notification")
    @patch("realtor_project.features.is_feature_enabled")
    def test_landing_lead_captcha_disabled_submits_normally(self, mock_is_feature_enabled, mock_send_notif):
        mock_is_feature_enabled.side_effect = lambda flag, default=True: False if flag == "CAPTCHA_ENABLE" else True
        
        from content.models import LandingLead
        initial_count = LandingLead.objects.count()
        
        response = self.client.post(
            reverse("landing_lead_api"),
            data={
                "phone": "+919876543210",
                "property_city": "Chennai",
                "intent_type": "sell",
                "property_type": "villa",
                "selling_timeline": "immediate",
                "name": "Genuine Human",
                "email": "human@example.com",
            }
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(LandingLead.objects.count(), initial_count + 1)

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="info@propertism.in",
        ADMIN_EMAIL="info@propertism.in",
        RECAPTCHA_SECRET_KEY="dummy-secret",
    )
    @patch("content.views.send_landing_lead_notification")
    @patch("realtor_project.features.is_feature_enabled")
    def test_landing_lead_captcha_enabled_missing_token_fails(self, mock_is_feature_enabled, mock_send_notif):
        mock_is_feature_enabled.side_effect = lambda flag, default=True: True if flag == "CAPTCHA_ENABLE" else True
        
        from content.models import LandingLead
        initial_count = LandingLead.objects.count()
        
        response = self.client.post(
            reverse("landing_lead_api"),
            data={
                "phone": "+919876543210",
                "property_city": "Chennai",
                "intent_type": "sell",
                "property_type": "villa",
                "selling_timeline": "immediate",
                "name": "Anonymous User",
                "email": "anon@example.com",
            }
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(LandingLead.objects.count(), initial_count)

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="info@propertism.in",
        ADMIN_EMAIL="info@propertism.in",
        RECAPTCHA_SECRET_KEY="dummy-secret",
    )
    @patch("content.views.send_landing_lead_notification")
    @patch("realtor_project.features.is_feature_enabled")
    @patch("content.security.google_recaptcha.GoogleRecaptchaV2.verify")
    def test_landing_lead_captcha_enabled_valid_token_submits(self, mock_verify, mock_is_feature_enabled, mock_send_notif):
        from content.security.google_recaptcha import RecaptchaResult
        mock_verify.return_value = RecaptchaResult(success=True, hostname="localhost")
        
        mock_is_feature_enabled.side_effect = lambda flag, default=True: True if flag == "CAPTCHA_ENABLE" else True
        
        from content.models import LandingLead
        initial_count = LandingLead.objects.count()
        
        response = self.client.post(
            reverse("landing_lead_api"),
            data={
                "phone": "+919876543210",
                "property_city": "Chennai",
                "intent_type": "sell",
                "property_type": "villa",
                "selling_timeline": "immediate",
                "name": "Genuine Human",
                "email": "human@example.com",
                "g-recaptcha-response": "valid-token-mock",
            }
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(LandingLead.objects.count(), initial_count + 1)

    @patch("realtor_project.features.is_feature_enabled")
    def test_honeypot_triggers_silent_reject(self, mock_is_feature_enabled):
        mock_is_feature_enabled.side_effect = lambda flag, default=True: True if flag == "CAPTCHA_ENABLE" else True
        
        from properties.models import Inquiry
        from content.models import SpamLog
        self.assertEqual(Inquiry.objects.count(), 0)
        self.assertEqual(SpamLog.objects.count(), 0)

        response = self.client.post(
            reverse("contact"),
            data={
                "name": "Spammer",
                "email": "spam@example.com",
                "phone": "+919876543210",
                "message": "Viagra cheap pills",
                "website_url_check": "triggered-honeypot",  # Honeypot filled
                "form_source": "General Inquiry",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Inquiry.objects.count(), 0)
        self.assertEqual(SpamLog.objects.count(), 1)
        self.assertEqual(SpamLog.objects.first().failure_reason, "honeypot-triggered")


class LocalBusinessSchemaTests(TestCase):
    def test_organization_schema_includes_local_business_and_gbp_details(self):
        from content.templatetags.seo_tags import organization_schema
        import json
        
        # Test rendering the organization_schema tag
        context = {}
        result = organization_schema(context)
        schema = json.loads(result['schema'])
        
        # Assert type, coordinates, map query, and working hours
        self.assertEqual(schema["@context"], "https://schema.org")
        self.assertEqual(schema["@type"], ["LocalBusiness", "RealEstateAgent"])
        self.assertEqual(schema["geo"]["latitude"], "13.0531")
        self.assertEqual(schema["geo"]["longitude"], "80.2094")
        from django.conf import settings
        self.assertEqual(schema["hasMap"], settings.GOOGLE_BUSINESS_PROFILE_MAP_URL)
        self.assertEqual(schema["openingHours"], "Mo-Sa 09:00-18:00")
        self.assertEqual(schema["priceRange"], "$$")


class RelatedLinksTests(TestCase):
    def test_related_links_preserves_nri_origin_for_nri_targets(self):
        # Visit the geo-targeted url
        response = self.client.get('/dubai-uae/chennai-villas-for-sale/', follow=True)
        self.assertEqual(response.status_code, 200)
        
        # Check context
        related_intents = response.context['related_intents']
        
        # Find 'nri-sell-property' in related_intents
        sell_link = next((item for item in related_intents if item['slug'] == 'nri-sell-property'), None)
        self.assertIsNotNone(sell_link)
        self.assertEqual(sell_link['url'], '/dubai-uae/chennai-nri-sell-property/')
        
        # Find a domestic intent 'flats-for-sale'
        flats_link = next((item for item in related_intents if item['slug'] == 'flats-for-sale'), None)
        if flats_link:
            self.assertEqual(flats_link['url'], '/chennai/flats-for-sale/')


class WhatsAppNotificationTests(TestCase):
    @patch('requests.post')
    @patch('django.core.mail.send_mail')
    def test_send_whatsapp_notification_sends_email_on_expired_token(self, mock_send_mail, mock_post):
        from content.views import send_whatsapp_notification
        from django.conf import settings
        from django.core.cache import cache
        from unittest.mock import MagicMock
        
        # Configure settings mock
        settings.WHATSAPP_PHONE_ID = 'test-phone'
        settings.WHATSAPP_ACCESS_TOKEN = 'test-token'
        settings.WHATSAPP_ADMIN_PHONE = '1234567890'
        settings.ADMIN_EMAIL = 'admin@example.com'
        
        # Clear cache first
        cache.delete("whatsapp_access_token")
        
        # Mock requests.post to return 401 with OAuth expiry payload
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {
                "message": "Error validating access token: Session has expired",
                "type": "OAuthException",
                "code": 190,
                "error_subcode": 463
            }
        }
        mock_post.return_value = mock_response
        
        # Run notification
        send_whatsapp_notification("Test message")
        
        # Verify that send_mail was called to alert administrator
        mock_send_mail.assert_called_once()
        args, kwargs = mock_send_mail.call_args
        self.assertIn("Action Required: Propertism WhatsApp Access Token Expired", kwargs['subject'])
        self.assertIn("admin@example.com", kwargs['recipient_list'])


class AddressAutocompleteFrameworkTests(TestCase):
    def test_settings_load_google_maps_credentials(self):
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'GOOGLE_MAPS_API_KEY'))
        self.assertEqual(settings.GOOGLE_MAPS_API_KEY, 'AIzaSyBAOA3xvBpa3FQF4l27hVh7-_5mlTR3zB0')
        self.assertEqual(settings.GOOGLE_MAPS_DEFAULT_COUNTRY, 'in')
        self.assertEqual(settings.GOOGLE_MAPS_AUTOCOMPLETE_COUNTRIES, ['in'])

    def test_context_processor_exposes_autocomplete_config(self):
        from django.test import RequestFactory
        from content.context_processors import site_content
        
        request = RequestFactory().get('/')
        context = site_content(request)
        
        self.assertIn('google_maps_api_key', context)
        self.assertEqual(context['google_maps_api_key'], 'AIzaSyBAOA3xvBpa3FQF4l27hVh7-_5mlTR3zB0')
        self.assertEqual(context['google_maps_countries'], ['in'])
        self.assertEqual(context['google_maps_default_country'], 'in')





