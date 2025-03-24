class AlgorithmPractice:
    def __init__(self):
        print("算法练习开始！")
    
    # 冒泡排序
    def bubble_sort(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr
    
    # 选择排序
    def selection_sort(self, arr):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr
    
    # 二分查找
    def binary_search(self, arr, target):
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] > target:
                right = mid - 1
            else:
                left = mid + 1
        return -1
    
    # 斐波那契数列（递归实现）
    def fibonacci_recursive(self, n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return self.fibonacci_recursive(n-1) + self.fibonacci_recursive(n-2)
    
    # 斐波那契数列（动态规划实现）
    def fibonacci_dp(self, n):
        if n <= 0:
            return 0
        if n == 1:
            return 1
        
        fib = [0] * (n+1)
        fib[1] = 1
        
        for i in range(2, n+1):
            fib[i] = fib[i-1] + fib[i-2]
        
        return fib[n]

# 测试代码
if __name__ == "__main__":
    ap = AlgorithmPractice()
    
    # 测试排序
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("原始数组:", arr)
    print("冒泡排序:", ap.bubble_sort(arr.copy()))
    print("选择排序:", ap.selection_sort(arr.copy()))
    
    # 测试查找
    sorted_arr = [11, 12, 22, 25, 34, 64, 90]
    target = 22
    result = ap.binary_search(sorted_arr, target)
    print(f"二分查找: 元素 {target} 在索引 {result} 处")
    
    # 测试斐波那契
    n = 10
    print(f"斐波那契(递归) F({n}) =", ap.fibonacci_recursive(n))
    print(f"斐波那契(动态规划) F({n}) =", ap.fibonacci_dp(n))