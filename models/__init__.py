# import json
# import time
# from utils import log
#
#
# def save(data, path):
#     """
#     data 是 dict 或者 list
#     path 是保存文件的路径
#     """
#     s = json.dumps(data, indent=2, ensure_ascii=False)
#     with open(path, 'w+', encoding='utf-8') as f:
#         # log('save', path, s, data)
#         f.write(s)
#
#
# def load(path):
#     with open(path, 'r', encoding='utf-8') as f:
#         s = f.read()
#         # log('load', s)
#         return json.loads(s)
#
#
# # Model 是一个 ORM（object relation mapper）
# class Model(object):
#     """
#     Model 是所有 model 的基类
#     """
#     @classmethod
#     def db_path(cls):
#         classname = cls.__name__
#         path = 'data/{}.txt'.format(classname)
#         return path
#
#     @classmethod
#     def _new_from_dict(cls, d):
#         m = cls({})
#         for k, v in d.items():
#             setattr(m, k, v)
#         return m
#
#     @classmethod
#     def new(cls, form, **kwargs):
#         m = cls(form)
#         for k, v in kwargs.items():
#             setattr(m, k, v)
#         m.save()
#         return m
#
#     @classmethod
#     def all(cls):
#         """
#         all 方法使用 load 函数得到所有的 models
#         """
#         path = cls.db_path()
#         models = load(path)
#         # 这里用了列表推导生成一个包含所有 实例 的 list
#         # 因为这里是从 存储的数据文件 中加载所有的数据
#         # 所以用 _new_from_dict 这个特殊的函数来初始化一个数据
#         ms = [cls._new_from_dict(m) for m in models]
#         return ms
#
#     @classmethod
#     def find_all(cls, **kwargs):
#         ms = []
#         log('kwargs, ', kwargs, type(kwargs))
#         k, v = '', ''
#         for key, value in kwargs.items():
#             k, v = key, value
#         all = cls.all()
#         for m in all:
#             if v == m.__dict__[k]:
#                 ms.append(m)
#         return ms
#
#     @classmethod
#     def find_by(cls, **kwargs):
#         """
#         按条件查找
#         """
#         log('kwargs, ', kwargs, type(kwargs))
#         k, v = '', ''
#         for key, value in kwargs.items():
#             k, v = key, value
#         all = cls.all()
#         for m in all:
#             if v == m.__dict__[k]:
#                 return m
#         return None
#
#     @classmethod
#     def find(cls, id):
#         return cls.find_by(id=id)
#
#     @classmethod
#     def get(cls, id):
#         return cls.find_by(id=id)
#
#     @classmethod
#     def delete(cls, id):
#         models = cls.all()
#         index = -1
#         for i, e in enumerate(models):
#             if e.id == id:
#                 index = i
#                 break
#         # 判断是否找到了这个 id 的数据
#         if index == -1:
#             # 没找到
#             pass
#         else:
#             obj = models.pop(index)
#             l = [m.__dict__ for m in models]
#             path = cls.db_path()
#             save(l, path)
#             # 返回被删除的元素
#             return obj
#
#     def __repr__(self):
#         """
#         __repr__ 是一个魔法方法
#         得到类的 字符串表达 形式
#         """
#         classname = self.__class__.__name__
#         properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
#         s = '\n'.join(properties)
#         return '< {}\n{} \n>\n'.format(classname, s)
#
#     def json(self):
#         """
#         返回当前 model 的字典表示
#         """
#         d = self.__dict__.copy()
#         return d
#
#     def save(self):
#         """
#         用 all 方法读取文件中的所有 model 并生成一个 list
#         把 self 添加进去并且保存进文件
#         """
#         # log('debug save')
#         models = self.all()
#         # log('models', models)
#         # 如果没有 id，说明是新添加的元素
#         if self.id is None:
#             # 设置 self.id
#             # 先看看是否是空 list
#             if len(models) == 0:
#                 # 让第一个元素的 id 为 1（当然也可以为 0）
#                 self.id = 1
#             else:
#                 m = models[-1]
#                 # log('m', m)
#                 self.id = m.id + 1
#             models.append(self)
#         else:
#             # index = self.find(self.id)
#             index = -1
#             for i, m in enumerate(models):
#                 if m.id == self.id:
#                     index = i
#                     break
#             log('debug', index)
#             models[index] = self
#         l = [m.__dict__ for m in models]
#         path = self.db_path()
#         save(l, path)
