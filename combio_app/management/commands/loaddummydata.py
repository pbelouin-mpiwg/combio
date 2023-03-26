from django.core.management.base import BaseCommand, CommandError
from combio_app.models import Record, Collection
import random


def load_collections():
    i = 0
    while i < 4:
        c = Collection(name=(random.sample(["SHI", "Wellcome Trust", "Queen Mary", "NIH"], 1))[0])
        c.save()
        i = i + 1


def create_record(data, collection):
    r = Record(transcript=data["transcript"], metadata=data["metadata"])
    col = collection
    r.collection = col
    r.save()


def purge_collections():
    Collection.objects.all().delete()


def purge_records():
    Record.objects.all().delete()


def load_records():
    data1 = {
        "transcript": "Cruisin' down the street in my '64 Jockin' the freaks, clockin' the dough Went to the park to get the scoop Knuckleheads out there cold-shootin' some hoops A car pulls up, who can it be?A fresh El Camino rollin', Kilo GHe rolls down his window and he started to say 'It's all about makin' that GTA'",
        "metadata": {
            "combio": {
                "title": "Boyz-n-the-Hood",
                "permalink": "https://www.youtube.com/watch?v=DsZOnZWpgNY",
                "participants": [
                    {"name": "Pascal Belouin", "role": "interviewer"},
                    {"name": "Kim Pham", "role": "interviewee"},
                    {"name": "Michael Winter", "role": "interviewee"},
                    {"name": "Calvin Yeh", "role": "participant"},
                    {"name": "Hassan El Hajj", "role": "participant"},
                ],
            },
            "dc": {
                "subject": "Biomedicine",
                "description": "This is a description",
                "publisher": "This is the publisher",
                "date": "2019-04-12",
            },
            "other": {"a_field": "some stuff", "another_field": "some other stuff"},
        },
    }

    data2 = {
        "transcript": "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?",
        "metadata": {
            "combio": {
                "title": "Medical ethics education in Britain, 1963-1993 : the transcript of a Witness Seminar held by the Wellcome Trust Centre for the History of Medicine at UCL, London.",
                "permalink": "https://www.youtube.com/watch?v=DsZOnZWpgNY",
                "participants": [
                    {"name": "Patrick Bateman", "role": "interviewer"},
                    {"name": "Bob Loblow", "role": "interviewee"},
                    {"name": "Linda Brites", "role": "interviewee"},
                    {"name": "Robert Casties", "role": "participant"},
                    {"name": "Catherine Bloos", "role": "interviewer"},
                ],
            },
            "dc": {
                "subject": "Psychology",
                "description": "This is a long description",
                "publisher": "This is the publisher of this thing",
                "date": "2017-02-12",
            },
            "other": {"a_nother_field": "some more stuff", "another_metadata_field": "some more other stuff"},
        },
    }

    i = 0
    while i < 150:
        create_record(random.sample([data1, data2], 1)[0], random.sample(list(Collection.objects.all()), 1)[0])
        i = i + 1


class Command(BaseCommand):
    help = "Loads dummy data"

    def handle(self, **options):
        purge_records()
        purge_collections()
        load_collections()
        load_records()
        self.stdout.write(self.style.SUCCESS("Successfully loaded dummy data"))
