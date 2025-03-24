#include <stdio.h>

// 递归方式计算斐波那契数列
int fibRecursive(int n) {
    if (n <= 1)
        return n;
    return fibRecursive(n - 1) + fibRecursive(n - 2);
}

// 迭代方式计算斐波那契数列（更高效）
int fibIterative(int n) {
    int a = 0, b = 1, c, i;
    if (n == 0)
        return a;
    
    for (i = 2; i <= n; i++) {
        c = a + b;
        a = b;
        b = c;
    }
    return b;
}

// 主函数
int main() {
    int n = 10;
    
    printf("使用递归方法计算的第 %d 个斐波那契数是: %d\n", n, fibRecursive(n));
    printf("使用迭代方法计算的第 %d 个斐波那契数是: %d\n", n, fibIterative(n));
    
    printf("\n斐波那契数列的前 %d 个数字:\n", n+1);
    for (int i = 0; i <= n; i++) {
        printf("%d ", fibIterative(i));
    }
    printf("\n");
    
    return 0;
}