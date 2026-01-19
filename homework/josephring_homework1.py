def simulate_josephus_elimination_list(people, start_index, step):
    """使用 list 实现约瑟夫环淘汰过程，返回淘汰顺序（不含最后一人）。"""
    elimination_order = []                      # 存储被淘汰人员的顺序
    current_index = start_index                 # 当前报数起始位置（下标从0开始）
    while len(people) > 1:                      # 当剩余人数大于1时，继续淘汰
        current_index = current_index + step - 1# 向前移动 step - 1 步
        if current_index >= len(people):
            current_index %= len(people)        # 如果当前索引超出列表范围，则进行循环取余,注意,索引最大为 len(people)-1）
        eliminated = people.pop(current_index)
        elimination_order.append(eliminated)    # 淘汰当前位置的人，并从列表中移除
        '''
        # 列表实现的调试用打印语句
        print(f"淘汰位置: {current_index }, 淘汰的人: {eliminated}")
        print("当前淘汰顺序:", elimination_order)
        print("剩余人员:", people, "\n")
        '''
    return elimination_order                    # 返回淘汰顺序（最后幸存者未包含）
#test1
def achieve_josephring_list(total_people, step, start_person):
    """实现约瑟夫环，返回完整的淘汰顺序（包括最后幸存者）。"""
    # 参数合法性校验
    if total_people < 1 or step < 1 or start_person < 0 or start_person > total_people-1:
        raise ValueError("参数数值不合法（总人数和报值数必须≥1，指定的人要在1~n之间）")
    people = list(range(total_people))  # 创建人员列表，编号从 0 开始：[0, 1, 2, ..., total_people-1]
    start_index = start_person          # 起始索引直接使用 start_person(下标从0开始)
    elimination_order = simulate_josephus_elimination_list(people, start_index, step)# 模拟淘汰过程
    elimination_order.append(people[0]) # 将最后剩下的一个人追加到淘汰顺序末尾，形成完整序列
    return elimination_order



from collections import deque                   #双端队列，支持两端插入/删除，非常适合模拟循环队列

def simulate_josephus_elimination_deque(total_people, step, start_person):
    """使用 deque 模拟约瑟夫环，返回完整淘汰顺序（含最后幸存者）。"""
    people_deque = deque(range(total_people))   # 初始化人员编号 [0, 1, ..., n-1]
    people_deque.rotate(-start_person)          # 从左向右的start_person个数，与其右边的所有数逆时针旋转，让 start_person 成为队列的第一个元素

    elimination_order = []
    while len(people_deque) > 1:
        people_deque.rotate(-(step - 1))        # 将前 (step - 1) 人移到队尾
        eliminated_person = people_deque.popleft()  # 队首为第 step 人，淘汰
        elimination_order.append(eliminated_person)
        '''
        # 队列实现的调试用打印语句
        print(f"淘汰的人: {eliminated_person}")
        print("当前淘汰顺序:", elimination_order)
        print("剩余人员（从当前队首开始）:", list(people_deque), "\n")
        '''
    elimination_order.append(people_deque[0])   # 添加最后幸存者
    return elimination_order

def achieve_josephring_deque(total_people, step, start_person):
    if total_people < 1 or step < 1 or not (0 <= start_person < total_people):
        raise ValueError("参数数值不合法（总人数和报值数必须≥1，指定的人要在0~n-1之间）")
    return simulate_josephus_elimination_deque(total_people, step, start_person)



class ListNode:
    """单向链表节点"""
    __slots__ = ('val', 'next')             #限制这个类只能有 val 和 next 两个属性，val：存储人的编号，next：指向下一个节点
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def simulate_josephus_elimination_linked_list(total_people, step, start_person):
    """使用循环单链表实现约瑟夫环，返回完整淘汰顺序（含最后幸存者）。"""
    if total_people == 1:   
        return [0]                          #特殊情况：只有 1 个人，直接返回 [0]

    '''构建循环链表: 0 -> 1 -> ... -> n-1 -> 0'''
    head = ListNode(0)                      #创建一个 ListNode节点，它的val是 0
    current_node = head                     #current_node初始指向 head
    for i in range(1, total_people):
        current_node.next = ListNode(i)     #给当前节点的 next 指向一个新节点
        current_node = current_node.next    #移动指针到新节点
    current_node.next = head                #最后一个值的next指向0，形成环

    '''定位到起始节点start_person'''
    previous_node = None                    #current_node的前一个节点
    current_node = head
    for _ in range(start_person):           #使用_作占位符，循环start_person次
        previous_node = current_node
        current_node = current_node.next

    '''如果从索引 0 开始，需手动找到尾节点作为 previous_node'''
    if start_person == 0:
        previous_node = current_node
        while previous_node.next != current_node:   #current_node为0时，previous_node为n-1，循环找得尾结点
            previous_node = previous_node.next

    elimination_order = []
    remaining_count = total_people


    while remaining_count > 1:                  # 开始淘汰过程
        for _ in range(step - 1):
            previous_node = current_node
            current_node = current_node.next    # 移动 (step - 1) 步

        eliminated_person = current_node.val    #取出当前被淘汰的人的编号
        elimination_order.append(eliminated_person) #把被淘汰者的编号记录到结果列表中

        previous_node.next = current_node.next  # 跳过当前节点,即删除
        current_node = current_node.next        # 移动 current_node 到下一个人
        remaining_count -= 1                    # 剩余人数减 1
        '''
        # 链表实现的调试用打印语句
        print(f"淘汰: {eliminated_person}, 当前下一人: {current_node.val}")
        print("顺序:", elimination_order, "\n")
        '''

    elimination_order.append(current_node.val)  # 添加最后幸存者
    return elimination_order


def achieve_josephring_linked_list(total_people, step, start_person):
    if total_people < 1 or step < 1 or not (0 <= start_person < total_people):
        raise ValueError("参数数值不合法（总人数和报值数必须≥1，指定的人要在0~n-1之间）")
    return simulate_josephus_elimination_linked_list(total_people, step, start_person)


import time
import matplotlib.pyplot as plt

def performance_test():
    """性能测试函数"""
    n = 2000
    k = 100
    start_person = 0  # 固定起始位置 

    # 测试列表实现
    start_time = time.time()                #记录当前的开始时间
    achieve_josephring_list(n, k, start_person)
    list_time = time.time() - start_time    #消耗时间等于结束时间与开始时间之差
    print(f"列表实现耗时: {list_time:.4f}秒")

    # 测试队列实现
    start_time = time.time()
    achieve_josephring_deque(n, k, start_person)
    queue_time = time.time() - start_time
    print(f"队列实现耗时: {queue_time:.4f}秒")

    # 测试链表实现
    start_time = time.time()
    achieve_josephring_linked_list(n, k, start_person)
    linked_list_time = time.time() - start_time
    print(f"链表实现耗时: {linked_list_time:.4f}秒")

    # 性能比较分析
    print(f"性能比 (列表/队列): {list_time/queue_time:.2f}")
    print(f"性能比 (链表/队列): {linked_list_time/queue_time:.2f}")


def scalability_test():
    """可扩展性测试"""
    test_sizes = [1000 , 5000 , 10000 , 20000] 
    k = 100
    start_person = 0
    list_times = []
    queue_times = []
    linked_list_times = []

    for n in test_sizes:
        # 测试列表实现
        start_time = time.time()
        achieve_josephring_list(n, k, start_person)
        list_time = time.time() - start_time
        list_times.append(list_time)

        # 测试队列实现
        start_time = time.time()
        achieve_josephring_deque(n, k, start_person)
        queue_time = time.time() - start_time
        queue_times.append(queue_time)

        # 测试链表实现
        start_time = time.time()
        achieve_josephring_linked_list(n, k, start_person)
        linked_list_time = time.time() - start_time
        linked_list_times.append(linked_list_time)

        print(f"n={n}: 列表={list_time:.4f}s, 队列={queue_time:.4f}s, 链表={linked_list_time:.4f}s")

if __name__ == "__main__":
    try:
        print("=== 性能测试 ===")
        performance_test()
        print("\n=== 可扩展性测试 ===")
        scalability_test()
        print("test1")
    except ValueError as e:
        if "literal" in str(e):
            print("错误: 输入的参数必须是整数（请检查是否用了字母、小数、中文等）")
        else:
            print(f"错误: {e}")
    except Exception as e:
        print(f"程序意外终止: {e}")