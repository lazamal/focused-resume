from django.core.management.base import BaseCommand, CommandError
from api.models import Skill
import pandas as pd


# the command should take a cv file and load it onto the database

#  add_arguments function
# enable argument to be provided with the cv path in the


# handle function
# load the cv into pandas DataFrame
# loops through the DF and for each row add the name, alt-name and description of the skill to the model
# 




class Command(BaseCommand):
    help = "populates the Skill model with data from a skill table"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='provide a cv file containing skill name, alt-name and description in order to populate the skill db model')
    
    def handle(self, *args, **options):
        original_skil_table = pd.read_csv(options['file_path'])
        skills_for_model = pd.DataFrame({
                'name': original_skil_table['preferredLabel'],
                'alt_name': original_skil_table['altLabels'],
                'description': original_skil_table['description'],
        })
        
        for row in skills_for_model.itertuples(index = False):
            try:
               obj, created =  Skill.objects.get_or_create(name = row.name, 
                                            defaults= { "alt_name" : row.alt_name, "description" : row.description})
            except:
                raise CommandError(f'proccess failed on line {row} {obj.name}' )
            self.stdout.write(
                
            )
        self.style.SUCCESS('Successfully populated model')
        