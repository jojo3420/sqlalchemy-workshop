# sqlalchemy-workshop

python sqlalchemy orm module workshop

## database test

```shell
pip intall ipython

```

```shell
from app import database
from app import models 

models.Base.metadata.create_all(bind=database.engine)

conn = next(database.get_conn())
conn.query(models.User).all()
```

```shell
# setup 
a = User(email='a@gmail.com', username='aaa', password='1234')
b = User(email='b@daum.com', username='daum', password='1234')
spring = User(email='spirng@naver.com', username='spring', password='1234')
summer = User(email='summer@naver.com', username='summer', password='1234')
fall = User(email='fall@naver.com', username='fall', password='1234')
winter = User(email='winter@naver.com', username='winter', password='1234')

```

## 조회하기

```shell
conn.query(models.User).all()  #  전체조회 
conn.query(models.User).first()  # 첫번째 
conn.query(models.User).get(1) # id 로 조회  
conn.query(models.User).filter_by(id=1).first() # id 로 조회  
conn.query(models.User).filter_by(username='park').first() # id 로 조회
conn.query(models.User).filter(User.id==1).first()
  
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

## LIMIT, OFFSET

```shell
conn.query(User).limit(3).all()
conn.query(User).offset(1).limit(2).all()

```

## count()

```shell
conn.query(User).count()
conn.query(User).filter(User.email.like('%naver%')).count()

```

## Relationship

### One to Many(1:N)

class Parent (부모테이블, 1)
id username children = relationship(
'참조할 클래스명',
'참조할 클래스명에서 참조할 테이블명', lazy='dynamic'
)
class Child (자식테이블, N)
id, name, parent_id = Column(Integer, ForeignKey('참조할 테이블명.pk')
)

```shell
Parent = models.Parent
Child = models.Child
p1 = Parent(username='p1')
p2 = Parent(username='p2')
p3 = Parent(username='p3')
conn.add_all([p1, p2, p3])
conn.commit()
c1 = Child(name='c1', age=1)
c2 = Child(name='c2', age=2)
c3 = Child(name='c3', age=3)
conn.add_all([c1, c2, c3])
conn.commit()

c1.parent_id = p1.id
c2.parent_id = p1.id
c3.parent_id = p1.id
conn.commit()

for child in p1.children.all():
  print(child.id, child.name)
```

### Many To Many (M:N) 관계

class Member projects = relationship(
'참조할 클래스명', secondary="association_table 명", backref='참조할 클래스가 참조할 테이블명(자기자신)', lazy='dynamic'
)

class Project members = relationship(
'참조할 클래스명', secondary="association_table 명", backref='참조할 클래스가 참조할 테이블명(자기자신)', lazy='dynamic'
)

association_table = sqlalchemy.Table(
"member_project", Base.metadata, Column('컬럼명(member_id)', Integer, ForeignKey('member.id')), Column('컬럼명(project_id)',
Integer, ForeignKey('project.id'))
)

```shell
from app import database, models
conn = next(database.get_conn())
Project = models.Project
Member = models.Member

m1 = Member(name='m1')
m2 = Member(name='m2')
m3 = Member(name='m3')
m4 = Member(name='m4')
conn.add_all([m1, m2, m3, m4])
conn.commit()

p1 = Project(name='p1')
p2 = Project(name='p2')
conn.add_all([p1, p2])
conn.commit()


p1.members.append(m1)
p1.members.append(m2)
p1.members.append(m3)
conn.commit()

p2.members.append(m1)
p2.members.append(m3)
p2.members.append(m4)
conn.commit()


m1.projects.all()
# [p1, p2]

m2.projects.all()
# [p1]

m3.projects.all()
# [p1, p2]



p1.members.all()
# [m1, m2, m3]

p2.members.all()
# [m4, m3, m1]  # 순서가 입력 순서와 다르다.

```

## One To One Relationship

```python 
class Human(IDMixin, Base):
    __tablename__ = 'human'
    name = Column(String(25))
    age = Column(Integer)
    human_info = relationship('HumanInfo', back_populates='human', uselist=False)


class HumanInfo(IDMixin, Base):
    __tablename__ = 'human_info'
    address = Column(String(200))
    zipcode = Column(String(5))
    human_id = Column(Integer, ForeignKey('human.id'))

    human = relationship('Human', back_populates='human_info')

```
relationship 속성에 uselist=False 추가 
