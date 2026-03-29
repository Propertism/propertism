from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import CompanyInfo, CustomerReview, CustomerReviewSection, HeroBackgroundImage


TEST_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
    b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00"
    b"\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)


def make_test_image(name):
    return SimpleUploadedFile(name, TEST_GIF, content_type="image/gif")


class HeroBackgroundImageTests(TestCase):
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
