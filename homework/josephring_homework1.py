def simulate_josephus_elimination(people, start_index, step):
    """模拟约瑟夫环淘汰过程，返回淘汰顺序（不含最后一人）。"""
    elimination_order = []                      # 存储被淘汰人员的顺序
    current_index = start_index                 # 当前报数起始位置（下标从0开始）
    while len(people) > 1:                      # 当剩余人数大于1时，继续淘汰
        current_index = current_index + step - 1# 向前移动 step - 1 步
        if current_index >= len(people):
            current_index %= len(people)        # 如果当前索引超出列表范围，则进行循环取余,注意,索引最大为 len(people)-1）
        eliminated = people.pop(current_index)
        elimination_order.append(eliminated)    # 淘汰当前位置的人，并从列表中移除
        '''
        # 调试用打印语句（当前已注释）
        print(f"淘汰位置: {current_index}, 淘汰的人: {eliminated}") 
        print("当前淘汰顺序:", elimination_order)
        print("剩余人员:", people, "\n")
        '''
    return elimination_order                    # 返回淘汰顺序（最后幸存者未包含）


def achieve_josephring(total_people, step, start_person):
    """实现约瑟夫环，返回完整的淘汰顺序（包括最后幸存者）。"""
    # 参数合法性校验
    if total_people < 1 or step < 1 or start_person < 0 or start_person > total_people-1:
        raise ValueError("参数数值不合法（总人数和报值数必须≥1，指定的人要在1~n之间）")
    people = list(range(total_people))  # 创建人员列表，编号从 0 开始：[0, 1, 2, ..., total_people-1]
    start_index = start_person          # 起始索引直接使用 start_person(下标从0开始)
    elimination_order = simulate_josephus_elimination(people, start_index, step)# 模拟淘汰过程（返回除最后幸存者外的所有人）
    elimination_order.append(people[0]) # 将最后剩下的一个人追加到淘汰顺序末尾，形成完整序列
    return elimination_order

if __name__ == "__main__":
    try:
        inputs = input("请输入参数，以逗号分隔（如 8,3 或 8,3,0）：")
        inputs = inputs.replace("，", ",").replace(" ", "").replace("　", "")#将输入中的中文逗号丶缩进和空格变成英文的
        inputs = list(map(str.strip, inputs.split(",")))#将输入字符串按逗号分割，并去除每项首尾空白，如 "8,3,1" → ["8", "3", "1"]

        if len(inputs) != 2 and len(inputs) != 3:           # 检查参数个数是否为2或3
            raise ValueError("输入的参数不对，程序无法正常运行")
        total_people = int(inputs[0])
        step = int(inputs[1])
        if len(inputs) == 3:
            start_person = int(inputs[2])
        else:
            start_person = 0

        result = achieve_josephring(total_people,step,start_person)
        print(f"淘汰顺序为: {result}")

    except ValueError as e:
        if "literal" in str(e):
            print("错误: 输入的参数必须是整数（请检查是否用了字母、小数、中文等）")
        else:
            print(f"错误: {e}")
    except Exception as e:
        print(f"程序意外终止: {e}")

'''
if __name__ == "__main__":
    import sys
    # 打印调试信息，确认 argv 是什么
    print("argv:", sys.argv)  # 👈 加这一行！用于调试

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        # 原始交互逻辑（略作修改，调用新函数）
        try:
            inputs = input("请输入参数，以逗号分隔（如 8,3 或 8,3,1）：")
            inputs = inputs.replace("，", ",").replace(" ", "").replace("　", "")
            inputs = list(map(str.strip, inputs.split(",")))

            if len(inputs) not in (2, 3):
                raise ValueError("输入的参数不对，程序无法正常运行")

            n = int(inputs[0])
            k = int(inputs[1])
            designated_person = int(inputs[2]) if len(inputs) == 3 else 1

            result = achieve_josephring(n, k, designated_person)
            print(f"淘汰顺序为: {result}")

        except ValueError as e:
            if "literal" in str(e):
                print("错误: 输入的参数必须是整数（请检查是否用了字母、小数、中文等）")
            else:
                print(f"错误: {e}")
        except Exception as e:
            print(f"程序意外终止: {e}")
'''

'''
def run_tests():
    print(">>> 测试函数已启动！<<<")  # 👈 这行必须出现！
    print("开始运行测试用例...\n")

    test_cases = [
        # (n, k, designated_person, expected_output, description)
        (1, 1, 1, [1], "只有1人，k=1"),
        (1, 5, 1, [1], "只有1人，k很大"),
        (2, 1, 1, [1, 2], "k=1，按顺序淘汰"),
        (2, 2, 1, [2, 1], "n=2, k=2，从1开始"),
        (3, 2, 1, [2, 1, 3], "经典小例子"),
        (4, 2, 1, [2, 4, 3, 1], "n=4, k=2"),
        (5, 3, 1, [3, 1, 5, 2, 4], "n=5, k=3"),
        (7, 2, 1, [2, 4, 6, 1, 5, 3, 7], "n=7, k=2（验证公式）"),
        (3, 10, 1, [1, 2, 3], "k > n，等效于 k % n（但这里 k%n=1，所以按1处理？注意！）"),
        (5, 1, 3, [3, 4, 5, 1, 2], "从第3人开始，k=1"),
        (4, 3, 2, [4, 3, 1, 2], "从第2人开始，k=3"),
    ]

    error_cases = [
        # (n, k, designated_person, expected_exception_msg_part)
        (0, 1, 1, "参数数值不合法"),
        (1, 0, 1, "参数数值不合法"),
        (5, 3, 0, "参数数值不合法"),
        (5, 3, 6, "参数数值不合法"),
        (-1, 2, 1, "参数数值不合法"),
    ]

    passed = 0
    total = len(test_cases) + len(error_cases)

    # 测试正常情况
    for i, (n, k, start, expected, desc) in enumerate(test_cases, 1):
        try:
            result = achieve_josephring(n, k, start)
            if result == expected:
                print(f"✅ 测试 {i}: {desc} → 通过")
                passed += 1
            else:
                print(f"❌ 测试 {i}: {desc} → 失败")
                print(f"   期望: {expected}")
                print(f"   实际: {result}")
        except Exception as e:
            print(f"❌ 测试 {i}: {desc} → 程序异常: {e}")

    # 测试异常情况
    for j, (n, k, start, msg_part) in enumerate(error_cases, len(test_cases)+1):
        try:
            result = achieve_josephring(n, k, start)
            print(f"❌ 测试 {j}: 应抛出异常但未抛出，返回了 {result}")
        except ValueError as e:
            if msg_part in str(e):
                print(f"✅ 测试 {j}: 参数非法 → 正确捕获异常")
                passed += 1
            else:
                print(f"❌ 测试 {j}: 异常信息不符: {e}")
        except Exception as e:
            print(f"❌ 测试 {j}: 抛出了非 ValueError 异常: {e}")

    print(f"\n🎉 总共 {total} 个测试，通过 {passed} 个")
    if passed == total:
        print("所有测试通过！✅")
    else:
        print("存在失败测试，请检查代码。⚠️")
'''


