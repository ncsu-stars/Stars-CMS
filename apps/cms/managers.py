from django.db import models

import datetime

from cms import academic_year

class BlogPostManager(models.Manager):
    def by_academic_year(self, year):
        if isinstance(year, list):
            return reduce(lambda a,b: a|b, [ self.by_academic_year(x) for x in year ])
        else:
            if isinstance(year, str) or isinstance(year, unicode):
                year = int(year)

            lower_limit = datetime.datetime(year, 7, 1)
            upper_limit = datetime.datetime(year+1, 6, 30)

            return self.get_query_set().filter(date__gte=lower_limit, date__lte=upper_limit)
