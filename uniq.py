
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
    crossage = False
    age = (int)((date.today() - baby.birthday).days)

    if age > 3*365:
      if age % 365 == 0:
        crossage = True
    else:
      if age % 30 == 0:
        crossage = True
    #knowls = Knowledge.objects.filter(max__gte = age, min__lte = age)
    if crossage:
      newknowls = Knowledge.objects.filter(max__gte = age, min__lte = age)
      try:
        info = PushInfo.objects.get(user_id=key)
        info.knowledge_info = [knowl.id for knowl in newknowls]
        info.save
      except PushInfo.DoesNotExist:
        pass
      continue 
    knowls = knowlqueryset.filter(max__gte = age, min__lte = age)
    userknowls = user_pushinfo_dict.setdefault(parentid,set())
    
    knowl_ids = [userknowls.add(knowl.id) for knowl in knowls]
    #PushInfo.objects.create(user_id=parentid, knowledge_info=knowl_ids)

  for key, value in user_pushinfo_dict.iteritems():
    try:
      info = PushInfo.objects.get(user_id=key)
      newvalue = info.knowledge_info + list(value)
      info.save(newvalue)
    except PushInfo.DoesNotExist:
      PushInfo.objects.create(user_id=key, knowledge_info=list(value))
    except PushInfo.MultipleObjectsReturned:
      print "multiple object"
      PushInfo.objects.filter(user_id=key).delete()
      PushInfo.objects.create(user_id=key, knowledge_info=list(value))


  for i in PushInfo.objects.all():
    print i.knowledge_info

  #PushInfo.objects.create(user_id=2,knowledge_info=[1,2])
  

   
