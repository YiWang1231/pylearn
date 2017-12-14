import pandas as pd


class apple(object):

    def __init__(self, file):
        self.file = file

    def read_file(self):
        try:
            return pd.read_csv(self.file, header=0)
        except ValueError:
            print('parameter error')

    def ana_apple(self):
        df = self.read_file()
        df['Date'] = pd.to_datetime(df['Date'])
        df_volume = pd.Series(list(df['Volume']), index=df['Date'])
        df_volume = df_volume.resample('Q').sum()
        df_volume = df_volume.sort_values(ascending=False)
        return df_volume[1]


if __name__ == "__main__":

    app = apple('apple.csv')
    second_volume = app.ana_apple()
    print(second_volume)


# def data_plot():
#     """绘制用户学习数据图形
#     """
#
#     df = pd.read_json('user_study.json')
#
#     data = df.groupby('user_id').sum().head(5)
#     print(data.index)
#
#     fig = plt.figure()
#
#     ax = fig.add_subplot(1, 1, 1)
#     ax.set_xlabel('User ID')
#     ax.set_ylabel('Study Time')
#     ax.set_title('StudyData')
#     ax.plot(data.index, data.minutes)
#     # plt.show()
#
# if __name__ == '__main__':
#     data_plot()







# import json
# import pandas as pd
#
# class GetJson(object):
#     def __init__(self, file_name, user_id):
#         self.file_name = file_name
#         self.user_id = user_id
#
#     def read_file(self):
#         #file_path = os.path.join(os.path.dirname(__file__), self.file_name)
#         #with open(file_path) as f:
#             #json_str = json.load(f)
#         return pd.read_json(self.file_name)
#
#     def analysis(self):
#         df_user = self.read_file()
#         df_this_id = df_user[df_user['user_id'] == self.user_id]
#         times = len(df_this_id['user_id'])
#         minutes = df_this_id['minutes'].sum()
#         return times, minutes
#
#     def data_plot(self):
#         df_user = self.read_file()
#         df_minute = df_user[['user_id', 'minutes']].groupby ('user_id').sum()
#         return df_minute
#
#
# if __name__ == '__main__':
#     df_user = GetJson('user_study.json', 199071)
#     A = df_user.analysis()
#     print(len(A))
#     B = df_user.data_plot()
#     print(len(B.index))
#     print(B.head())
#     print(type(B))
#     #print('times is : %s \n minutes is : %s' % (A[0], A[1]))


