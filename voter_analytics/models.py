# file: models.py
# name: Shanika Paul
# email: shanikap@bu.edu
# date: October 31, 2025
# description: Data models for voter_analytics application including Voter model and load_data function.

from django.db import models

class Voter(models.Model):
    '''Represent a registered voter in Newton, MA.'''
    
    # Personal information
    first_name = models.TextField()
    last_name = models.TextField()
    
    # Address
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField(blank=True, null=True)  # Optional field
    zip_code = models.CharField(max_length=10)
    
    # Demographics and registration
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=10)
    
    # Election participation (boolean fields)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    
    # Voter score
    voter_score = models.IntegerField()
    
    def __str__(self):
        '''Return a string representation of this voter.'''
        return f'{self.first_name} {self.last_name} - {self.street_number} {self.street_name}, Precinct {self.precinct_number}'
    
    
    
    
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    
    # Delete existing records to prevent duplicates
    Voter.objects.all().delete()
    
    filename = 'data/newton_voters.csv'
    f = open(filename)
    f.readline()  # Discard headers
    
    for line in f:
        line = line.strip()
        fields = line.split(',')
        
        try:
            # Create a new instance of Voter object with this record from CSV
            voter = Voter(
                # fields[0] is Voter ID Number - we skip it
                last_name = fields[1],
                first_name = fields[2],
                street_number = fields[3],
                street_name = fields[4],
                apartment_number = fields[5] if fields[5] else None,  # Handle empty apartment numbers
                zip_code = fields[6],
                date_of_birth = fields[7],
                date_of_registration = fields[8],
                party_affiliation = fields[9],  
                precinct_number = fields[10],
                
                # Convert TRUE/FALSE strings to boolean
                v20state = fields[11].upper() == 'TRUE',
                v21town = fields[12].upper() == 'TRUE',
                v21primary = fields[13].upper() == 'TRUE',
                v22general = fields[14].upper() == 'TRUE',
                v23town = fields[15].upper() == 'TRUE',
                
                voter_score = fields[16],
            )
            
            voter.save()  # Commit to database
            print(f'Created voter: {voter}')
            
        except Exception as e:
            print(f"Skipped: {fields}")
            print(f"Error: {e}")
    
    print(f'Done. Created {len(Voter.objects.all())} Voters.')