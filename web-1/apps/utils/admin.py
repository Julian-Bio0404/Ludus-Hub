"""Admin utils"""

import nested_admin
from django.contrib import admin
from django.utils.html import format_html


class ImageAdminMixin:
    """
    Image admin mixin.
    Util for Model admin with image fields.
    """

    image = None

    def render_image(self, image):
        html = '<img src={} width="80" height="80" />'
        if image:
            preview = format_html(html, image.url)
            return preview
        return '-'

    def icon_preview(self, obj):
        if hasattr(obj, 'icon'):
            self.image = obj.icon
        return self.render_image(self.image)

    def photo_preview(self, obj):
        if hasattr(obj, 'photo'):
            self.image = obj.photo
        return self.render_image(self.image)

    def cover_photo_preview(self, obj):
        if hasattr(obj, 'cover_photo'):
            self.image = obj.cover_photo
        return self.render_image(self.image)

    icon_preview.short_description = 'Icon'
    photo_preview.short_description = 'Photo'
    cover_photo_preview.short_description = 'Cover Photo'


class TabularInlineMixin:

    suit_form_inlines_hide_original = True
    extra = 0


class BaseTabularInline(admin.TabularInline, TabularInlineMixin):
    """Base Tabular Inline admin."""
    pass


class BaseNestedTabularInline(TabularInlineMixin, nested_admin.NestedTabularInline):
    """Base Nested Tabular Inline admin."""
    pass
