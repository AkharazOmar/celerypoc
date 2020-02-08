import time

from celery import chain
from celerypoc.mycelery import app


class TaskResult:
    def __init__(self, value):
        self.value = value


@app.task()
def add(x, y):
    if isinstance(x, TaskResult):
        x = x.value
    return x + y

@app.task()
def mul(x, y):
    if isinstance(x, TaskResult):
        x = x.value
    return x * y


@app.task()
def division(x, y=None):
    print("FIXME x = {}".format(x))
    print("FIXME x = {}".format(type(x)))
    print("FIXME y = {}".format(y))
    if isinstance(x, (tuple, list)):
        x, y = x
    elif isinstance(x, TaskResult):
        x, y = x.value
    else:
        x = x
    print("FIXME x = {}, y = {}".format(x, y))
    return x / y


@app.task()
def timeout(x, y):
    print("i sleep {} sec".format(x), flush=True)
    time.sleep(x)
    print("now i sleep {} sec".format(y), flush=True)
    time.sleep(y)
    return x, y


my_chain = chain(
    add.subtask((2, 2)),
    mul.subtask((1, )),
    timeout.subtask((1,)),
    division.subtask(),
    add.subtask((1,)),
    timeout.subtask((10,)),
)


if __name__ == "__main__":
    res = my_chain.delay()
    print(res.ready())
    print(res.state)
