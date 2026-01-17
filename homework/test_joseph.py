print("🚀 开始运行 Python 脚本！")
def calculate_outperson_order(list_origin, index, k):
    list_process = []
    while len(list_origin) > 1:
        index += k - 1
        if index >= len(list_origin):
            index %= len(list_origin)
        list_process.append(list_origin.pop(index))
    return list_process

def achieve_josephring(n, k, designated_person=1):
    if not (1 <= designated_person <= n and n >= 1 and k >= 1):
        raise ValueError("参数非法")
    people = list(range(1, n+1))
    idx = designated_person - 1
    out = calculate_outperson_order(people, idx, k)
    out.append(people[0])
    return out

def run_tests():
    print("✅ 测试开始！")
    assert achieve_josephring(1,1,1) == [1]
    assert achieve_josephring(2,2,1) == [2,1]
    print("✅ 所有测试通过！")

if __name__ == "__main__":
    import sys
    print("ARGV:", sys.argv)
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        print("交互模式未启用（仅测试）")