import pandas as pd
import spacy
from django.core.management.base import BaseCommand
from tqdm import tqdm

from belege.models import Annotation, Citation


class Command(BaseCommand):
    help = "import coordinates for places"

    def handle(self, *args, **options):
        tool = "de_core_news_sm"
        nlp = spacy.load(tool)

        items = (
            Citation.objects.filter(definition__isnull=False)
            .exclude(definition="--")
            .exclude(definition="")
        )
        columns = ["dboe_id", "beleg__dboe_id", "quote_text", "definition"]

        values = items.values_list(*columns)
        df = pd.DataFrame(values, columns=columns)
        source_field = "definition"
        for i, row in tqdm(df.iterrows(), total=len(df)):
            text = row[source_field]
            kontext = Citation.objects.get(dboe_id=row["dboe_id"])
            annotation, _ = Annotation.objects.get_or_create(
                kontext=kontext, tool=tool, source_field=source_field
            )
            if annotation.payload:
                pass
            else:
                payload = []
                doc = nlp(text)
                for token in doc:
                    payload.append(
                        {
                            "text": token.text,
                            "lemma": token.lemma_,
                            "pos": token.pos_,
                            "tag": token.tag_,
                            "dep": token.dep_,
                            "shape": token.shape_,
                            "is_alpha": token.is_alpha,
                            "is_stop": token.is_stop,
                        }
                    )
                annotation.payload = payload
                annotation.save()
