import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

course = pd.read_table('courses.txt', sep=',', header=0)
i = pd.to_datetime(course['创建时间'])
course_ts = pd.DataFrame(data = course.values, columns = course.columns, index = i)
course_ts = course_ts.drop('创建时间', axis=1)
course_ts_w = course_ts.resample('W').sum()
course_ts_w['id'] = range(0, len(course_ts_w.index.values))
course_ts_A = course_ts.copy()
course_ts_A['平均学习时间'] = course_ts_A['学习时间']/course_ts_A['学习人数']
course_ts_A = course_ts_A.sort_values(by='平均学习时间', ascending=False)
time_zero = course_ts_A['平均学习时间'] == 0
course_ts_A.loc[time_zero, '平均学习时间'] = 0.01
print(course_ts_A[time_zero]['平均学习时间'])
course_ts_A['人数/平均学习时间'] = course_ts_A['学习人数']/course_ts_A['平均学习时间']
print(course_ts_A.sort_values(by='人数/平均学习时间').tail())
sns.jointplot('平均学习时间', '学习人数', kind='scatter', data=course_ts_A)
plt.xlabel('average study time')
plt.ylabel('Number of users')
plt.grid()
plt.show()