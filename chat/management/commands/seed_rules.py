"""
chat/management/commands/seed_rules.py — M2.4
Idempotent management command that loads all 29 intent rules from rules_config.py
into the BusinessRule table.

Usage:
    .\\scripts\\django.cmd seed_rules
    .\\scripts\\django.cmd seed_rules --reset    # wipe and re-seed all rules
"""
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Seed the BusinessRule table with all 29 realBOT intent rules (M2.4)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete all existing BusinessRule records before seeding.',
        )

    def handle(self, *args, **options):
        from chat.models import BusinessRule
        from chat.rules_config import SEED_RULES

        if options['reset']:
            count = BusinessRule.objects.count()
            BusinessRule.objects.all().delete()
            self.stdout.write(self.style.WARNING(
                f"[seed_rules] Reset: deleted {count} existing rules."
            ))

        created = updated = skipped = 0

        with transaction.atomic():
            for rule_data in SEED_RULES:
                intent = rule_data['intent']
                defaults = {
                    'name':                  rule_data['name'],
                    'category':              rule_data['category'],
                    'priority':              rule_data['priority'],
                    'positive_keywords':     rule_data.get('positive_keywords', ''),
                    'negative_keywords':     rule_data.get('negative_keywords', ''),
                    'phrase_patterns':       rule_data.get('phrase_patterns', ''),
                    'keyword_weight':        rule_data.get('keyword_weight', 1.0),
                    'min_confidence':        rule_data.get('min_confidence', 0.4),
                    'action_type':           rule_data['action_type'],
                    'action_config':         rule_data.get('action_config', {}),
                    'clarification_question': rule_data.get('clarification_question', ''),
                    'is_enabled':            True,
                }

                existing = BusinessRule.objects.filter(intent=intent).first()

                if existing is None:
                    # Create new rule (rule_id auto-generated on save)
                    BusinessRule.objects.create(intent=intent, **defaults)
                    self.stdout.write(
                        self.style.SUCCESS(f"  [CREATED] {intent}")
                    )
                    created += 1
                else:
                    # Check if any meaningful field changed
                    changed = any(
                        getattr(existing, field) != value
                        for field, value in defaults.items()
                        if field not in ('is_enabled',)  # don't override manual disable
                    )
                    if changed:
                        for field, value in defaults.items():
                            setattr(existing, field, value)
                        existing.version += 1
                        existing.save()
                        self.stdout.write(
                            self.style.WARNING(f"  [UPDATED] {intent} → v{existing.version}")
                        )
                        updated += 1
                    else:
                        self.stdout.write(f"  [SKIP]    {intent}")
                        skipped += 1

        total = created + updated + skipped
        self.stdout.write(self.style.SUCCESS(
            f"\n[seed_rules] Done. {total} rules processed: "
            f"{created} created, {updated} updated, {skipped} unchanged."
        ))

        # Print summary table
        from chat.models import BusinessRule as BR
        enabled = BR.objects.filter(is_enabled=True).count()
        disabled = BR.objects.filter(is_enabled=False).count()
        self.stdout.write(
            f"[seed_rules] Registry: {enabled} enabled, {disabled} disabled "
            f"({BR.objects.count()} total)."
        )
