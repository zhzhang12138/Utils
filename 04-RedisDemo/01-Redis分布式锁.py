import time
import uuid
import redis
from multiprocessing import Process

redis_client = redis.Redis(host='***.***.***.***', port=6379, db=0)


# 加锁的过程
def acquire_lock(lock_name, args, acquire_time=30, time_out=120):
    """
    获取一个分布式锁
    :param lock_name: 锁定名称
    :param args: 自定义参数
    :param acquire_time: 客户端等待获取锁的时间
    :param time_out: 锁的超时时间
    :return:
    """
    identifier = str(uuid.uuid4())
    # 客户端获取锁的结束时间
    end = time.time() + acquire_time
    lock_names = "lock_name:" + lock_name
    print(f"进程 {str(args)} end_time:{end}")
    while time.time() < end:
        # 使用 setnx(key,value) 设置锁   只有key不存在情况下，将key的值设置为value 返回True,若key存在则不做任何动作,返回False
        if redis_client.setnx(lock_names, identifier):
            # 设置键的过期时间，过期自动剔除，释放锁
            print('获得锁:进程' + str(args))
            print(f'分布式锁value:{identifier}')
            redis_client.expire(lock_name, time_out)
            return identifier
        # 当锁未被设置过期时间时，重新设置其过期时间
        elif redis_client.ttl(lock_name) == -1:
            redis_client.expire(lock_name, time_out)
        time.sleep(0.001)
    return False


# 锁的释放
def release_lock(lock_name, identifier):
    """
    通用的锁释放函数
    :param lock_name: 锁定名称identifier
    :param identifier: 标识符-分布式锁value
    :return:
    """
    lock_names = "lock_name:" + lock_name
    pipe = redis_client.pipeline(True)
    while True:
        try:
            # 通过watch命令监视某个键，当该键未被其他客户端修改值时，事务成功执行。当事务运行过程中，发现该值被其他客户端更新了值，任务失败
            pipe.watch(lock_names)
            print(pipe.get(lock_name))

            lock_value = redis_client.get(lock_names)
            if not lock_value:
                return True

            if pipe.get(lock_names).decode() == identifier:  # 检查客户端是否仍然持有该锁
                # multi命令用于开启一个事务，它总是返回ok
                # multi执行之后， 客户端可以继续向服务器发送任意多条命令， 这些命令不会立即被执行， 而是被放到一个队列中， 当 EXEC 命令被调用时， 所有队列中的命令才会被执行
                pipe.multi()
                # 删除键，释放锁
                pipe.delete(lock_names)
                # execute命令负责触发并执行事务中的所有命令
                pipe.execute()
                return True
            pipe.unwatch()
            break
        except redis.exceptions.WatchError:
            # 释放锁期间，有其他客户端改变了键值对，锁释放失败，进行循环
            pass
    return False


# 模拟加锁解锁的过程
def exec_test(lock_name, args):
    """
    模拟加锁解锁的过程
    :param lock_name: 锁定名称
    :param args: 自定义参数
    :return:
    """
    identifier = acquire_lock(lock_name, args)
    print(f'identifier :{identifier}')
    # 如果获取到锁,则进行业务逻辑处理
    if identifier:
        # sleep 3s 模拟业务逻辑处理,处理完之后进行锁释放,让其他进程获取锁
        time.sleep(3)
        res = release_lock(lock_name, identifier)
        print(f'释放状态: {res}')
    else:
        print('获取redis分布式锁失败,其他进程正在使用')


if __name__ == '__main__':
    for i in range(0, 9):
        Process(target=exec_test, args=('test', i)).start()
