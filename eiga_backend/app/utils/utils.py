import base64

from django.db.models import Sum

from app.models import Bangumi, Score
from eiga_backend.settings import ASSETS_ROOT


def getBangumiScoreAndRank():
    raw_bangumis = []
    for bangumi in Bangumi.objects.all():
        rater_cnt = Score.objects.filter(bangumi_id=bangumi.bangumi_id).__len__()
        total_score = Score.objects.filter(bangumi_id=bangumi.bangumi_id).aggregate(total=Sum('score'))
        raw_bangumis.append({
            'bangumi_id': bangumi.bangumi_id,
            'bangumi_score': total_score['total'] / rater_cnt if total_score['total'] else 0.0,
            'rater_cnt': rater_cnt
        })
    sorted_bangumis = sorted(raw_bangumis, key=lambda x: x['bangumi_score'], reverse=True)
    bangumi_dict = {}
    for i in range(len(sorted_bangumis)):
        bangumi = sorted_bangumis[i]
        bangumi_dict[bangumi['bangumi_id']] = {
            'bangumi_score': bangumi['bangumi_score'],
            'bangumi_rank': i + 1,
            'rater_cnt': bangumi['rater_cnt']
        }
    return bangumi_dict


def urlToImgDate(img):
    with open(ASSETS_ROOT + img, 'rb') as f:
        image_data = base64.b64encode(f.read())
    return str(image_data)[2:-1]
