from api.models import Session
from api.utils import getVirtualRanks
session = Session.objects.get(id=15)
getVirtualRanks(session)