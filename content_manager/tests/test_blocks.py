from django.contrib.auth.models import User
from wagtail.models import Page
from wagtail.rich_text import RichText
from wagtail.test.utils import WagtailPageTestCase

from content_manager.models import ContentPage


class HorizontalCardBlockCase(WagtailPageTestCase):
    # Logic *should* be the same for a vertical card, but inside of a multiple columns block.
    def setUp(self):
        home = Page.objects.get(slug="home")
        self.admin = User.objects.create_superuser("test", "test@test.test", "pass")
        self.admin.save()

        body = [
            (
                "card",
                {
                    "title": "Sample card",
                    "description": RichText('<p data-block-key="test">This is a sample card.</p>'),
                },
            )
        ]
        self.content_page = home.add_child(
            instance=ContentPage(title="Sample cards page", slug="content-page", owner=self.admin, body=body)
        )
        self.content_page.save()

    def test_basic_card_is_renderable(self):
        self.assertPageIsRenderable(self.content_page)

    def test_basic_card_has_structure_and_content(self):
        url = self.content_page.url
        response = self.client.get(url)

        self.assertContains(
            response,
            "fr-card fr-card--horizontal",
        )
        self.assertInHTML("""<h3 class="fr-card__title">Sample card</h3>""", response.content.decode())
        self.assertInHTML(
            """<p class="fr-card__desc" data-block-key="test">This is a sample card.</p>""", response.content.decode()
        )

    def test_card_with_no_link_does_not_have_enlarge_class(self):
        url = self.content_page.url
        response = self.client.get(url)

        # The page header and footer have the class on the bloc-marque,
        # The card with no link should not, so count should be 2
        self.assertContains(response, "fr-enlarge-link", count=2)

    def test_card_with_main_link(self):
        body = [
            (
                "card",
                {"title": "Sample card", "description": "This is a sample card.", "url": "https://www.info.gouv.fr"},
            )
        ]
        self.content_page.body = body
        self.content_page.save()

        url = self.content_page.url
        response = self.client.get(url)

        # Count = 3 (page header and footer, card)
        self.assertContains(response, "fr-enlarge-link", count=3)

        self.assertInHTML("""<a href="https://www.info.gouv.fr">Sample card</a>""", response.content.decode())

    def test_card_with_cta_links(self):
        body = [
            (
                "card",
                {
                    "title": "Sample card",
                    "description": "This is a sample card.",
                    "url": "https://www.info.gouv.fr",
                    "call_to_action": [
                        {
                            "type": "links",
                            "value": [
                                {
                                    "type": "link",
                                    "value": {
                                        "page": None,
                                        "text": "Lien externe",
                                        "external_url": "https://numerique.gouv.fr",
                                    },
                                }
                            ],
                        }
                    ],
                },
            )
        ]
        self.content_page.body = body
        self.content_page.save()

        url = self.content_page.url
        response = self.client.get(url)

        # Count = 3 (page header and footer, but not the card as it has several links)
        self.assertContains(response, "fr-enlarge-link", count=2)

        self.assertInHTML("""<a href="https://www.info.gouv.fr">Sample card</a>""", response.content.decode())

        self.assertInHTML(
            """<ul class="fr-links-group">
                <li>
                    <a href="https://numerique.gouv.fr" target="_blank" rel="noopener external">Lien externe</a>
                </li>
            </ul>""",
            response.content.decode(),
        )

    def test_card_with_cta_buttons(self):
        body = [
            (
                "card",
                {
                    "title": "Sample card",
                    "description": "This is a sample card.",
                    "url": "https://www.info.gouv.fr",
                    "call_to_action": [
                        {
                            "type": "buttons",
                            "value": [
                                {
                                    "type": "button",
                                    "value": {
                                        "page": None,
                                        "text": "Label",
                                        "button_type": "fr-btn fr-btn--secondary",
                                        "external_url": "https://numerique.gouv.fr",
                                    },
                                },
                            ],
                        }
                    ],
                },
            )
        ]
        self.content_page.body = body
        self.content_page.save()

        url = self.content_page.url
        response = self.client.get(url)

        # Count = 3 (page header and footer, but not the card as it has several links)
        self.assertContains(response, "fr-enlarge-link", count=2)

        self.assertInHTML("""<a href="https://www.info.gouv.fr">Sample card</a>""", response.content.decode())

        self.assertInHTML(
            """<ul class="fr-btns-group fr-btns-group--inline-reverse fr-btns-group--inline-lg">
                <li>
                    <a class="fr-btn fr-btn--secondary"
                    href="https://numerique.gouv.fr"
                    target="_blank"
                    rel="noopener external">Label</a>
                </li>
            </ul>""",
            response.content.decode(),
        )

    def test_card_with_basic_top_tag(self):
        body = [
            (
                "card",
                {
                    "title": "Sample card",
                    "description": "This is a sample card.",
                    "url": "https://www.info.gouv.fr",
                    "top_detail_badges_tags": [
                        {
                            "type": "tags",
                            "value": [
                                {
                                    "type": "tag",
                                    "value": {
                                        "link": {"page": None, "external_url": ""},
                                        "color": "purple-glycine",
                                        "label": "Tag 1",
                                        "is_small": False,
                                        "icon_class": "fr-icon-community-fill",
                                    },
                                },
                            ],
                        }
                    ],
                },
            )
        ]
        self.content_page.body = body
        self.content_page.save()

        url = self.content_page.url
        response = self.client.get(url)

        # Count = 3 (page header and footer, card)
        self.assertContains(response, "fr-enlarge-link", count=3)

        self.assertInHTML("""<a href="https://www.info.gouv.fr">Sample card</a>""", response.content.decode())

        self.assertInHTML(
            """<ul class="fr-tags-group">
                <li>
                    <p class="fr-tag fr-tag--purple-glycine fr-icon-community-fill fr-tag--icon-left">Tag 1</p>
                </li>
            </ul>""",
            response.content.decode(),
        )

    def test_card_with_linked_top_tag(self):
        body = [
            (
                "card",
                {
                    "title": "Sample card",
                    "description": "This is a sample card.",
                    "url": "https://www.info.gouv.fr",
                    "top_detail_badges_tags": [
                        {
                            "type": "tags",
                            "value": [
                                {
                                    "type": "tag",
                                    "value": {
                                        "link": {"page": None, "external_url": "https://numerique.gouv.fr"},
                                        "color": "purple-glycine",
                                        "label": "Tag 1",
                                        "is_small": False,
                                        "icon_class": "fr-icon-community-fill",
                                    },
                                },
                            ],
                        }
                    ],
                },
            )
        ]
        self.content_page.body = body
        self.content_page.save()

        url = self.content_page.url
        response = self.client.get(url)

        # Count = 3 (page header and footer, but not the card as it has several links)
        self.assertContains(response, "fr-enlarge-link", count=2)

        self.assertInHTML("""<a href="https://www.info.gouv.fr">Sample card</a>""", response.content.decode())

        self.assertInHTML(
            """<ul class="fr-tags-group">
                <li>
                    <a href="https://numerique.gouv.fr"
                    class="fr-tag fr-tag--purple-glycine fr-icon-community-fill fr-tag--icon-left">Tag 1</a>
                </li>
            </ul>""",
            response.content.decode(),
        )
