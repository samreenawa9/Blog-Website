from django.contrib import admin
from django.utils.html import format_html
from .models import Post, ContactMessage

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "published_at", "created_at", "image_thumb")
    list_filter = ("status", "author", "published_at", "created_at")
    search_fields = ("title", "content", "slug")
    prepopulated_fields = {"slug": ("title",)}  #  hum waise bhi save() me set kar rahe
    readonly_fields = ("published_at", "created_at", "updated_at", "image_preview")
    date_hierarchy = "published_at"
    list_per_page = 20
    ordering = ("-published_at", "-created_at")

    fieldsets = (
        ("Content", {"fields": ("title", "slug", "content", "image", "image_preview")}),
        ("Meta", {"fields": ("author", "status", "published_at", "created_at", "updated_at")}),
    )

    actions = ["make_published", "make_draft"]

    def make_published(self, request, queryset):
        updated = 0
        for post in queryset:
            if post.status != 'published':
                post.status = 'published'
                if post.published_at is None:
                    from django.utils import timezone
                    post.published_at = timezone.now()
                post.save()
                updated += 1
        self.message_user(request, f"{updated} post(s) published.")

    make_published.short_description = "Mark selected posts as Published"

    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f"{updated} post(s) moved to Draft.")

    make_draft.short_description = "Mark selected posts as Draft"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:240px;border-radius:8px;" />', obj.image.url)
        return "—"

    def image_thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;width:60px;object-fit:cover;border-radius:4px;" />', obj.image.url)
        return "—"
    image_thumb.short_description = "Image"
    
    
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "short_message", "created_at")
    search_fields = ("name", "email", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    def short_message(self, obj):
        return obj.message[:50] + ("..." if len(obj.message) > 50 else "")
    short_message.short_description = "Message"

