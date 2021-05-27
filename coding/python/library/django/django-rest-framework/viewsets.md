---
title: django viewset
categories: 
	- [python, library, django, django rest framework]
tags:
	- django rest framework
	- django rest framework
date: 2020/12/25 19:00:00
---

# 自定义 Action

```python
from rest_framework.decorators import action


class SnippetViewSet(viewsets.ModelViewSet):
    ...

    @action(detail=False, methods=['GET'], name='Get Highlight')
    def highlight(self, request, *args, **kwargs):
        queryset = models.Highlight.objects.all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
```

