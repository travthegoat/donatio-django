import random
from uuid import uuid4
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.files import File
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from accounts.models import User
from organizations.models import OrganizationRequest, Organization
from attachments.models import Attachment
from activities.models import Activity, ActivityTransaction
from transactions.models import Transaction
from transactions.constants import TransactionType, TransactionStatus


class Command(BaseCommand):
    help = "Seed dummy org requests, orgs, transactions, activities, and attachments."

    def handle(self, *args, **kwargs):
        # === STEP 1: Load org admins (bot1 and bot2) ===
        admins = list(User.objects.filter(username__in=["bot1", "bot2"]))
        if not admins:
            self.stdout.write(self.style.ERROR("❌ 'bot1' and 'bot2' users not found. Run your user setup command first."))
            return

        # === STEP 2: Load dummy file ===
        dummy_file_path = Path("media/seeds/default_img.jpg")
        if not dummy_file_path.exists():
            self.stdout.write(self.style.ERROR("❌ Dummy image not found at media/seeds/default_img.jpg"))
            return

        self.stdout.write(self.style.NOTICE("✅ Starting dummy data seeding..."))

        for idx, admin in enumerate(admins, start=1):
            # === STEP 3: Create OrganizationRequest ===
            org_request = OrganizationRequest.objects.create(
                submitted_by=admin,
                organization_name=f"seed_org_{idx}",
                type="education",
                status="approved",
                approved_by=admin,
                approved_at=timezone.now()
            )
            self.create_attachments(org_request, dummy_file_path, count=2)

            # === STEP 4: Create Organization ===
            org = Organization.objects.create(
                admin=admin,
                name=f"seed_org_{idx}",
                type="education",
                organization_request=org_request,
                description="This is a dummy seeded organization."
            )
            self.create_attachments(org, dummy_file_path, count=2, max_allowed=2)

            # === STEP 5: Create Donation Transactions ===
            for i in range(2):
                donation = Transaction.objects.create(
                    organization=org,
                    actor=random.choice(admins),
                    title=f"Donation {i+1} for {org.name}",
                    amount=random.uniform(10, 100),
                    type=TransactionType.DONATION,
                    status=TransactionStatus.APPROVED,
                    review_required=False
                )
                self.create_attachments(donation, dummy_file_path, count=1, max_allowed=1)

            # === STEP 6: Create Disbursement Transactions ===
            disbursements = []
            for i in range(2):
                disbursement = Transaction.objects.create(
                    organization=org,
                    actor=admin,
                    title=f"Disbursement {i+1} for {org.name}",
                    amount=random.uniform(20, 150),
                    type=TransactionType.DISBURSEMENT,
                    status=TransactionStatus.PENDING,
                    review_required=False
                )
                self.create_attachments(disbursement, dummy_file_path, count=2)
                disbursements.append(disbursement)

            # === STEP 7: Create Activity ===
            activity = Activity.objects.create(
                organization=org,
                title=f"Activity for {org.name}",
                description="This activity explains how the funds were used.",
                location="Yangon",
            )
            self.create_attachments(activity, dummy_file_path, count=2)

            # === STEP 8: Link Disbursement Transactions to Activity ===
            for tx in disbursements:
                ActivityTransaction.objects.create(
                    activity=activity,
                    transaction=tx
                )

            self.stdout.write(self.style.SUCCESS(f"✅ Seeded data for org admin '{admin.username}'"))

        self.stdout.write(self.style.SUCCESS("🎉 All dummy data successfully seeded!"))

    def create_attachments(self, instance, file_path, count=1, max_allowed=None):
        for _ in range(min(count, max_allowed or count)):
            with open(file_path, "rb") as f:
                Attachment.objects.create(
                    content_object=instance,
                    file=File(f, name=f"default_{uuid4()}.jpg")
                )

