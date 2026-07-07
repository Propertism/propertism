"""
chat/management/commands/seed_suggestions.py — M2.7
Idempotent Django management command that loads all default Suggestion Definitions into the DB.

Usage:
    .\\scripts\\django.cmd seed_suggestions
    .\\scripts\\django.cmd seed_suggestions --reset
"""
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Seed the SuggestionDefinition table with standard suggestions (M2.7)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete all existing SuggestionDefinition records before seeding.',
        )

    def handle(self, *args, **options):
        from chat.models import SuggestionDefinition
        from chat.suggestions_config import SEED_SUGGESTIONS

        if options['reset']:
            count = SuggestionDefinition.objects.count()
            SuggestionDefinition.objects.all().delete()
            self.stdout.write(self.style.WARNING(
                f"[seed_suggestions] Reset: deleted {count} existing suggestion definitions."
            ))

        created = updated = skipped = 0

        with transaction.atomic():
            for index, sug_data in enumerate(SEED_SUGGESTIONS, start=1):
                display_text = sug_data['display_text']
                category = sug_data['category']
                
                # Pre-defined target Suggestion ID based on loop index to keep them stable e.g. SUG000001
                target_id = f"SUG{index:06d}"

                defaults = {
                    'display_text':       display_text,
                    'category':           category,
                    'parent_context':     sug_data.get('parent_context', ''),
                    'trigger_condition':  sug_data.get('trigger_condition', {}),
                    'business_intent':    sug_data.get('business_intent', ''),
                    'target_action':      sug_data.get('target_action', ''),
                    'display_priority':   sug_data.get('display_priority', 50),
                    'icon':               sug_data.get('icon', ''),
                    'display_order':      sug_data.get('display_order', 0),
                    'visibility_rules':   sug_data.get('visibility_rules', {}),
                    'status':             'active',
                }

                # Try to get by suggestion_id or by unique combo of display_text + category + business_intent
                existing = (
                    SuggestionDefinition.objects.filter(suggestion_id=target_id).first()
                    or SuggestionDefinition.objects.filter(
                        display_text=display_text,
                        category=category,
                        business_intent=defaults['business_intent'],
                    ).first()
                )

                if existing is None:
                    # Create new suggestion
                    SuggestionDefinition.objects.create(suggestion_id=target_id, **defaults)
                    self.stdout.write(
                        self.style.SUCCESS(f"  [CREATED] {target_id}: {display_text} ({category})")
                    )
                    created += 1
                else:
                    # Check for changes
                    changed = any(
                        getattr(existing, field) != value
                        for field, value in defaults.items()
                        if field not in ('status',)
                    )
                    if changed:
                        for field, value in defaults.items():
                            setattr(existing, field, value)
                        existing.version += 1
                        existing.save()
                        self.stdout.write(
                            self.style.WARNING(f"  [UPDATED] {existing.suggestion_id}: {display_text} → v{existing.version}")
                        )
                        updated += 1
                    else:
                        skipped += 1

        total = created + updated + skipped
        self.stdout.write(self.style.SUCCESS(
            f"\n[seed_suggestions] Done. {total} suggestions processed: "
            f"{created} created, {updated} updated, {skipped} unchanged."
        ))
        self.stdout.write(
            f"[seed_suggestions] Registry: {SuggestionDefinition.objects.filter(status='active').count()} active "
            f"({SuggestionDefinition.objects.count()} total)."
        )
