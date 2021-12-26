# sqlalchemy-workshop

python sqlalchemy orm module workshop

## database test

```shell
ipython
  $ from app import database
  $ from app import models 
  $ 
  $ models.Base.metadata.create_all(bind=database.engine)
  $ 
  $ conn = next(database.get_conn())
  $ conn.query(models.User).all()
```

## 조회하기

```shell
conn.query(models.User).all()  #  전체조회 
conn.query(models.User).first()  # 첫번째 
conn.query(models.User).get(1) # id 로 조회  
conn.query(models.User).filter_by(id=1).first() # id 로 조회  
conn.query(models.User).filter_by(username='park').first() # id 로 조회  
```

## 삭제

```shell

park = conn.query(models.User).filter_by(username=park)  #  전체조
if park:
  conn.delete(park)
  conn.commit()
```

## 추가(생성)

```shell
new_user = models.User(username='aaa', email='a@a.com', password='1234')
conn.add(new_user)
conn.commit()

spring = models.User(email='spirng@a.com', password='1234', username='spring')
summer = models.User(email='summer@a.com', password='1234', username='summer')
fall = models.User(email='fall@a.com', password='1234', username='fall')
winter = models.User(email='winter@a.com', password='1234', username='winter')

conn.add_all([spring, summer, fall, winter])
conn.commit()
```

## 변경(modify)

```shell
user = conn.query(models.User).filter_by(username='park')
user.password = '1111'
conn.commit()

```

## Query 란?

SQL 문에서 질의할 때 여러가지 연산자를 구현한다. ex) equal, not equal, like, in, not in, null, not null, and, or, order by, limit, offset,
count

### Equal, Not Equal

```shell
# equal
first = conn.query(models.User).filter(User.id == 1).first()

# not equal
rest_members = conn.query(models.User).filter(User.id !=1).all()

querySet = conn.query(models.User).filter(User.id !=1)
type(querySet)
# sqlalchemy.orm.query.Query
querySet[0]
querySet[-1]
querySet[2]
querySet[0] == querySet.first()  # True
```

### LIKE '%%' 연산자

```shell
User = models.User
conn.query(User).filter(User.username.like('%pa%')).first()
# Out[143]: <User> park
```

### IN, NOT IN 연산자

```shell
# in:  .in_ 사용
conn.query(User).filter(User.username.in_(['summer', 'winter'])).all()
Out[144]: [<User> summer, <User> winter]

# not in : 앞에 ~ 표시 
conn.query(User).filter(~User.username.in_(['summer', 'winter'])).all()
Out[145]: [<User> park, <User> bbb, <User> u2, <User> aaa, <User> spring, <User> fall]

```

# IS NULL, IS NOT NULL

```shell
# nickname 프로퍼티 추가 
conn.query(User).filter(User.nickname == None).all()
# Out[11]: [<User> park, <User> bbb, <User> u2, <User> aaa, <User> spring]

conn.query(User).filter(User.nickname != None).all()
Out[12]: [<User> summer, <User> fall, <User> winter]

```

# AND 연산자

```shell
# 이중 필터함수 사용 
conn.query(User).filter(User.username.like('%s%')).filter(User.id==5).first()
Out[33]: <User> spring


conn.query(User).filter_by(gender='m').filter(User.username.like('%pa%')).all()
Out[17]: [<User> park]



```

두번째 방법

```shell
from sqlalchemy import and_
conn = ...
models = ...
User = models.User

conn.query(User).filter(User.gender == 'm').filter(
  and_(
  User.username.like('%pa%'),
  User.nickname=='p'
  )
).first()
Out[34]: <User> park

``` 

## OR 연산자

```shell
from sqlalchemy import or_, and_
conn.query(User).filter(User.gender == 'm').filter(
  or_(
    User.username.like('%a%')
  ),
    User.email.like('%a%')
).all()

# Out[39]: [<User> park, <User> aaa]

```

## ORDER BY

```shell
conn.query(User).order_by(User.username).all()
# [<User> aaa, <User> bbb, <User> fall, <User> park,
# <User> spring, <User> summer, <User> u2, <User> winter ]

conn.query(User).order_by(User.username.desc()).all()
# [
 # <<User> winter, User> u2, <User> summer, <User> spring, 
 # <User> park, <User> fall, <User> bbb, <User> aaa
# ]

conn.query(User).order_by(User.username.desc()).filter(User.gender=='m').all()
# Out[69]: [<User> winter, <User> u2, <User> park, <User> bbb, <User> aaa]


```