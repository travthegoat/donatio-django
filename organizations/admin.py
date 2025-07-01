from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import transaction 

from .models import OrganizationRequest, Organization
from .constants import OrganizationRequestStatus


# Admin configuration for OrganizationRequest
@admin.register(OrganizationRequest)
class OrganizationRequestAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'submitted_by', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('organization_name', 'submitted_by__username')
    readonly_fields = ('created_at', 'approved_at')

    fieldsets = (
        (None, {
            'fields': ('organization_name', 'submitted_by',)
        }),
        ('Approval Details', {
            'fields': ('status', 'approved_by', 'approved_at'),
            'description': 'These fields are for admin approval.'
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

    def has_change_permission(self, request, obj=None):
        # Only staff and superuser can change
        return request.user.is_staff or request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        # Only staff and superuser can change
        return request.user.is_staff or request.user.is_superuser

    @admin.action(description='Mark selected requests as Approved and Create Organizations')
    def approve_requests_and_create_organizations(self, request, queryset):
        approved_and_created_count = 0
        already_processed_count = 0
        rejected_count = 0 
        error_count = 0 

        for org_request in queryset:
            try:
                with transaction.atomic():
                    if org_request.status == OrganizationRequestStatus.PENDING:
                        org_request.status = OrganizationRequestStatus.APPROVED
                        org_request.approved_by = request.user
                        org_request.approved_at = timezone.now()
                        org_request.save()

                        # Create the Organization
                        Organization.objects.create(
                            organization_request=org_request,
                            name=org_request.organization_name,
                            description=_("Default description for %s") % org_request.organization_name,
                            admin=org_request.submitted_by,
                        )
                        approved_and_created_count += 1

                    elif org_request.status == OrganizationRequestStatus.APPROVED:
                        # Check if an Organization record exists
                        if not hasattr(org_request, 'organization'): 
                            Organization.objects.create(
                                organization_request=org_request,
                                name=org_request.organization_name,
                                description=_("Default description for %s") % org_request.organization_name,
                                admin=org_request.submitted_by,
                            )
                            self.message_user(
                                request,
                                f"Organization '{org_request.organization_name}' was already approved, but its Organization record has now been created.",
                                level=messages.INFO
                            )
                            approved_and_created_count += 1
                        else:
                            already_processed_count += 1
                            self.message_user(
                                request,
                                f"Request for {org_request.organization_name} is already approved and has an associated Organization.",
                                level=messages.INFO
                            )
                    elif org_request.status == OrganizationRequestStatus.REJECTED:
                        rejected_count += 1
                        self.message_user(
                            request,
                            f"Request for {org_request.organization_name} is rejected and cannot be approved via this action.",
                            level=messages.WARNING
                        )

            except Exception as e:
                error_count += 1
                self.message_user(
                    request,
                    f"An error occurred while processing request for {org_request.organization_name}: {e}. This request was not processed.",
                    level=messages.ERROR
                )

        if approved_and_created_count > 0:
            self.message_user(
                request,
                f"Successfully processed {approved_and_created_count} organization requests (approved and/or created missing organizations).",
                level=messages.SUCCESS
            )
        if already_processed_count > 0:
            self.message_user(
                request,
                f"{already_processed_count} requests were already fully processed and required no action.",
                level=messages.INFO
            )
        if rejected_count > 0:
            self.message_user(
                request,
                f"{rejected_count} rejected requests were skipped.",
                level=messages.WARNING
            )
        if error_count > 0:
            self.message_user(
                request,
                f"{error_count} requests encountered errors during processing.",
                level=messages.ERROR
            )


        if queryset.exists() and approved_and_created_count == 0 and already_processed_count == 0 and rejected_count == 0 and error_count == 0:
            self.message_user(
                request,
                "All selected requests were already in a state that prevented this action (e.g., already approved with an organization, or rejected).",
                level=messages.INFO
            )
        elif not queryset.exists():
            self.message_user(
                request,
                "No requests were selected for processing.",
                level=messages.WARNING
            )

    actions = ['approve_requests_and_create_organizations']

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'email', 'phone_number', 'created_at')
    list_filter = ('admin', 'created_at')
    search_fields = ('name', 'admin__username', 'email')
    readonly_fields = ('organization_request', 'created_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'admin', 'description',)
        }),
        ('Contact Info', {
            'fields': ('email', 'phone_number', 'additional_info',)
        }),
        ('System Details', {
            'fields': ('organization_request', 'created_at',)
        }),
    )

    def has_add_permission(self, request):
        # Prevent adding organizations directly
        return False

