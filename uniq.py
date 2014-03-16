
import os
import sys
import wjbbserver.settings 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wjbbserver.settings")

from baby.models import Baby
from knowledge.models import *
from datetime import date
import os

if __name__ == "__main__":
  queryid = -1
  if os.path.isfile("/tmp/uid"):
    with open("/tmp/uid") as fo:
      queryid = int(fo.read())
  print queryid
  user_pushinfo_dict = {}
  knowlqueryset = Knowledge.objects.filter(id__gt = queryid)
  print knowlqueryset.all().count()
  print knowlqueryset.count()
  if knowlqueryset.count() > 0:
    lastqueryknowl = knowlqueryset.all().order_by("-id")[0]
    print "lastid:", lastqueryknowl
    with open("/tmp/uid", 'w') as fo:
      fo.write(str(lastqueryknowl.id))
  
  for baby in Baby.objects.all():
    print baby
    print baby.name
    parentid = baby.parent_id
    age = (int)((date.today() - baby.birthday).days)
    #knowls = Knowledge.objects.filter(max__gte = age, min__lte = age)
    knowls = knowlqueryset.filter(max__gte = age, min__lte = age)
    userknowls = user_pushinfo_dict.setdefault(parentid,set())
    
    knowl_ids = [userknowls.add(knowl.id) for knowl in knowls]
    #PushInfo.objects.create(user_id=parentid, knowledge_info=knowl_ids)

  for key, value in user_pushinfo_dict.iteritems():
    PushInfo.objects.create(user_id=key, knowledge_info=list(value))


  for i in PushInfo.objects.all():
    print i.knowledge_info

  #PushInfo.objects.create(user_id=2,knowledge_info=[1,2])
  

   
