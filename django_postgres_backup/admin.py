from django.contrib import admin
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.urls import path
from django.utils.html import format_html
from django.db import models
import os
import glob
from datetime import datetime
from django_postgres_backup.settings import POSTGRES_BACKUP_DIR, DATABASE_DEFAULT
from django_postgres_backup.common import backup_and_cleanup_database
from django.contrib import messages
from django_postgres_backup.settings import POSTGRES_BACKUP_GENERATIONS


class DummyBackupFile(models.Model):
    """Dummy model for the changelist view."""
    class Meta:
        managed = False
        verbose_name_plural = "Database Backups"
        app_label = 'django_postgres_backup'

    def __str__(self):
        return "Database Backups"


class BackupFileAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return DummyBackupFile.objects.none()

    def changelist_view(self, request, extra_context=None):
        if '_backup' in request.POST:
            try:
                backup_and_cleanup_database(
                    database_format='t',
                    database_name=DATABASE_DEFAULT['NAME'],
                    name=DATABASE_DEFAULT['NAME'],
                    generation=POSTGRES_BACKUP_GENERATIONS,
                    username=DATABASE_DEFAULT['USER'],
                    path=POSTGRES_BACKUP_DIR,
                )
                self.message_user(request, "Backup created successfully!", messages.SUCCESS)
            except Exception as e:
                self.message_user(request, f"Error creating backup: {str(e)}", messages.ERROR)
            return HttpResponseRedirect(".")

        backup_dir = POSTGRES_BACKUP_DIR
        backup_files = glob.glob(os.path.join(backup_dir, '*.sql.bz2'))
        backups = []
        for filepath in sorted(backup_files, reverse=True):
            filename = os.path.basename(filepath)
            try:
                date_str = filename.split('-', 1)[1].rsplit('.', 2)[0]
                date = datetime.strptime(date_str, '%Y-%m-%d_%H-%M')
                formatted_date = date.strftime('%Y-%m-%d %H:%M')
            except (ValueError, IndexError):
                formatted_date = "Unknown"

            size = os.path.getsize(filepath)
            size_mb = size / (1024 * 1024)

            download_url = f'download/{os.path.basename(filepath)}/'
            download_link = format_html('<a href="{}">Download</a>', download_url)
            delete_url = f'delete/{os.path.basename(filepath)}/'
            delete_link = format_html(
                '<a href="{}" onclick="return confirm(\'Are you sure you want to delete this backup?\');" style="color: #ba2121;">Delete</a>', delete_url)

            backups.append({
                'filename': filename,
                'date': formatted_date,
                'size': f'{size_mb:.2f} MB',
                'download': format_html('{} | {}', download_link, delete_link),
            })

        extra_context = extra_context or {}
        extra_context['backups'] = backups
        extra_context['title'] = 'Database Backups'

        template_response = super().changelist_view(request, extra_context)
        template_response.template_name = 'admin/backup_file_changelist.html'
        return template_response

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('download/<path:filepath>/', self.download_backup, name='download_backup'),
            path('delete/<path:filepath>/', self.delete_backup, name='delete_backup'),
        ]
        return custom_urls + urls

    def download_backup(self, request, filepath):
        backup_dir = POSTGRES_BACKUP_DIR
        file_path = os.path.join(backup_dir, filepath)

        if os.path.exists(file_path) and os.path.isfile(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Type'] = 'application/x-bzip2'
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        return HttpResponse('File not found', status=404)

    def delete_backup(self, request, filepath):
        backup_dir = POSTGRES_BACKUP_DIR
        file_path = os.path.join(backup_dir, filepath)

        try:
            if os.path.exists(file_path) and os.path.isfile(file_path):
                os.remove(file_path)
                self.message_user(request, f"Backup {filepath} deleted successfully!", messages.SUCCESS)
            else:
                self.message_user(request, f"Backup file {filepath} not found.", messages.WARNING)
        except Exception as e:
            self.message_user(request, f"Error deleting backup: {str(e)}", messages.ERROR)

        return HttpResponseRedirect("../../")


admin.site.register(DummyBackupFile, BackupFileAdmin)
