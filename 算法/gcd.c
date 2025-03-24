#include <stdio.h>

// 使用递归的欧几里得算法计算GCD
int gcdRecursive(int a, int b) {
    if (b == 0)
        return a;
    return gcdRecursive(b, a % b);
}

// 使用迭代的欧几里得算法计算GCD
int gcdIterative(int a, int b) {
    int temp;
    while (b != 0) {
        temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// 主函数
int main() {
    int a = 98, b = 56;
    
    printf("%d 和 %d 的最大公约数（递归）是: %d\n", a, b, gcdRecursive(a, b));
    printf("%d 和 %d 的最大公约数（迭代）是: %d\n", a, b, gcdIterative(a, b));
    
    return 0;
}