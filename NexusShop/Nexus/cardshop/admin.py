from django.contrib import admin
from .models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'series', 'price', 'rarity', 'clan', 'stock', 'image_preview')
    list_filter = ('rarity', 'clan', 'series')
    search_fields = ('name', 'series', 'clan')
    ordering = ('-id',)
    
    fieldsets = (
        ('ข้อมูลพื้นฐาน', {
            'fields': ('name', 'series', 'clan')
        }),
        ('ค่ากำหนด', {
            'fields': ('price', 'rarity', 'stock')
        }),
        ('รูปภาพ', {
            'fields': ('image',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return '✓ มีรูป'
        return '✗ ไม่มีรูป'
    image_preview.short_description = 'รูปภาพ'


admin.site.register(Card, CardAdmin)