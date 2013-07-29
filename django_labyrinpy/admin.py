from django.contrib import admin

from models import Message, Report


class MessageAdmin(admin.ModelAdmin):
    list_display = ('destination', 'message_type')
    search_fields = ('destination',)
    fieldsets = [
        (None, {'fields': ['destination', 'message_type']}),
        ('Optional', {'fields': ['source_name',
                                 'source',
                                 'service',
                                 'header',
                                 'wap_text',
                                 '_class',
                                 'concatenate',
                                 'unicode',
                                 'validity',
                                 'delivery',
                                 'report'],
                      'classes': ['collapse']}),
    ]


class ReportAdmin(admin.ModelAdmin):
    raw_id_fields = ('message',)
    list_display = ('message', 'status', 'timestamp')
    list_filter = ('status',)

admin.site.register(Message, MessageAdmin)
admin.site.register(Report, ReportAdmin)
