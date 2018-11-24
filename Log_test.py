import datetime

# функция записи лога
def log_insert(log):
    with open('update.log', 'a', encoding='utf-8') as f_obj:
        string = f'{datetime.datetime.now()}: {log}\n'
        f_obj.write(string)

a = [1, 2, 3, 4]

try:
    print(a[7])
except Exception as e:
    log_insert(e)