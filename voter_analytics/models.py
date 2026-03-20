from django.db import models

# Create your models here.

class Voter(models.Model):
    '''
   store voter data
    '''
    last_name = models.TextField()
    first_name = models.TextField()

    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField(blank=True)
    zip_code = models.TextField()

    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.TextField()
 
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
 
    voter_score = models.IntegerField()
 
    def __str__(self):
        ''' a string representation of a voter.'''
        return f'{self.first_name} {self.last_name} ({self.street_number} {self.street_name}, {self.zip_code})'


def load_data():
    '''method to load data records into the model'''
 
    Voter.objects.all().delete()
 
    filename = '/Users/alexchappuis/Desktop/django/newton_voters.csv'
    f = open(filename)
    f.readline()
 
    for line in f:
        fields = line.strip().split(',')
 
        try:
            result = Voter(
                last_name=fields[1],
                first_name=fields[2],
                street_number=fields[3],
                street_name=fields[4],
                apartment_number=fields[5],
                zip_code=fields[6],
                date_of_birth=fields[7],
                date_of_registration=fields[8],
                party_affiliation=fields[9].strip(),
                precinct_number=fields[10],
                v20state=(fields[11].strip() == 'TRUE'),
                v21town=(fields[12].strip() == 'TRUE'),
                v21primary=(fields[13].strip() == 'TRUE'),
                v22general=(fields[14].strip() == 'TRUE'),
                v23town=(fields[15].strip() == 'TRUE'),
                voter_score=int(fields[16]),
            )
            result.save()
            print(f'Created voter: {result}')
 
        except:
            print(f"Skipped: {fields}")
 
    print(f'Done. Created {len(Voter.objects.all())} Voters.')