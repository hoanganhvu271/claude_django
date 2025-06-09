from django.core.management.base import BaseCommand
from chatbot_service_app.symptom_extractor import SymptomExtractor
import os

class Command(BaseCommand):
    help = 'Manage symptom patterns - load, validate, update'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            choices=['validate', 'stats', 'reload', 'create-default'],
            default='stats',
            help='Action to perform'
        )
        parser.add_argument(
            '--patterns-file',
            type=str,
            help='Path to patterns JSON file'
        )
    
    def handle(self, *args, **options):
        action = options['action']
        patterns_file = options.get('patterns_file')
        
        # Initialize extractor
        extractor = SymptomExtractor(patterns_file)
        
        if action == 'validate':
            self.stdout.write("Validating symptom patterns...")
            issues = extractor.validate_patterns()
            
            if issues:
                self.stdout.write(
                    self.style.ERROR(f"Found {len(issues)} issues:")
                )
                for issue in issues:
                    self.stdout.write(f"  - {issue}")
            else:
                self.stdout.write(
                    self.style.SUCCESS("All patterns are valid!")
                )
        
        elif action == 'stats':
            self.stdout.write("Pattern statistics:")
            stats = extractor.get_pattern_statistics()
            
            self.stdout.write(f"Total symptoms: {stats['total_symptoms']}")
            self.stdout.write(f"Total patterns: {stats['total_patterns']}")
            self.stdout.write(f"Critical symptoms: {stats['critical_symptoms']}")
            
            self.stdout.write("\nCategories:")
            for category, count in stats['categories'].items():
                self.stdout.write(f"  {category}: {count}")
        
        elif action == 'reload':
            self.stdout.write("Reloading patterns...")
            success = extractor.reload_patterns()
            
            if success:
                self.stdout.write(self.style.SUCCESS("Patterns reloaded successfully!"))
            else:
                self.stdout.write(self.style.ERROR("Failed to reload patterns"))
        
        elif action == 'create-default':
            self.stdout.write("Creating default patterns file...")
            
            # Create data directory
            data_dir = os.path.join('chatbot_service_app', 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            patterns_file = os.path.join(data_dir, 'symptom_patterns.json')
            success = extractor.save_patterns(patterns_file)
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS(f"Default patterns created at: {patterns_file}")
                )
            else:
                self.stdout.write(self.style.ERROR("Failed to create default patterns"))