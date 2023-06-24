"""Admin utils"""

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
