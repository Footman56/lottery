import os
import itertools


class Lottery:
    def __init__(self, set1=set(), set2=set(), m=None, n=None, Q=None, M=None):
        self.set1 = set1
        self.set2 = set2
        self.m = m
        self.n = n
        self.Q = Q
        self.M = M

    def find_valid_combinations(self):
        valid_combinations = []

        # Generate all possible combinations of a, b, c, d, e, f in the range [1, 33]
        numbers = [i for i in range(1, 34) if i not in self.set2]

        for combination in itertools.combinations(numbers, 6):
            a, b, c, d, e, f = combination
            M = a + b + c + d + e + f
            if self.M is not None and (M < 50 or M > 150):
                continue

            evens = len([num for num in combination if num % 2 == 0])
            odds = 6 - evens

            if self.m is not None and self.m != evens:
                continue
            if self.n is not None and self.n != odds:
                continue

            differences = [abs(combination[i] - combination[i + 1]) for i in range(5)]
            max_gap = max(differences)

            if self.Q is not None and self.Q != max_gap:
                continue

            if self.set1 and not self.set1.issubset(set(combination)):
                continue

            valid_combinations.append(combination)

        return valid_combinations


def main():
    print("请输入 Lottery 属性 (集合1, 集合2, m, n, Q, M) 或者按 Enter 跳过设置默认值：")

    set1 = input("集合1 必须存在的数字 (用逗号分隔的数字，例如：1,2,3)：")
    set2 = input("集合2 必须不存在的数字(用逗号分隔的数字，例如：1,2,3)：")
    m = input("偶数的个数 m：")
    n = input("奇数的个数 n：")
    Q = input("最大间隔 Q：")
    M = input("总和 M：")

    set1 = set(map(int, set1.split(','))) if set1 else set()
    set2 = set(map(int, set2.split(','))) if set2 else set()
    m = int(m) if m else None
    n = int(n) if n else None
    Q = int(Q) if Q else None
    M = int(M) if M else None

    # 检查文件是否存在，如果存在则删除
    output_file = 'valid_combinations.txt'
    if os.path.exists(output_file):
        os.remove(output_file)

    lottery = Lottery(set1=set1, set2=set2, m=m, n=n, Q=Q, M=M)
    combinations = lottery.find_valid_combinations()

    if combinations:
        print(f"符合条件的组合共有 {len(combinations)} 组。结果将输出到 '{output_file}' 文件中。")
        with open(output_file, 'w') as f:
            for combo in combinations:
                f.write(f"{combo}\n")
    else:
        print("没有符合条件的组合。")


if __name__ == "__main__":
    main()
