# Django_serializer
## Django Serializer
- queryset, model, 객체 -> JSON, XML로 변환
- Deserialize : 받은 데이터를 validation하고(is_valid()) 파싱된 데이터를 다시 queryset, model, 객체 등의 complex type으로 변환
- DB, DB 인스턴스 예시
```
from datetime import datetime

class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

#원하는곳에서의 인스턴스생성
comment = Comment(email='leila@example.com', content='foo bar')
```

- serialize 객체 생성하여 직렬화
```
serializer = CommentSerializer(comment)
serializer.data
```

- Deserialize : is_valid() -> save()
```
import io
from rest_framework.parsers import JSONParser

stream = io.BytesIO(json) #JSON 문자열을 바이트 타입으로 바꾸고, ByteIO 객체로 바꾼다.
data = JSONParser().parse(stream) #JSONParser 의 parser() 메서드를 이용하여 딕셔너리 형태로 변환한다.
serializer = CommentSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
```

- Saving instance : create(), update(), save() 등 오버라이딩 가능
```
 def create(self, validated_data):
        return Comment(**validated_data)

def update(self, instance, validated_data):
      instance.email = validated_data.get('email', instance.email)
      instance.content = validated_data.get('content', instance.content)
      instance.created = validated_data.get('created', instance.created)
      return instance
      
def save(self):
        email = self.validated_data['email']
        message = self.validated_data['message']
        send_email(from=email, message=message)
 ```
 
 
