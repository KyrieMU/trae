#include <stdio.h>

// 线性搜索函数
int linearSearch(int arr[], int n, int x) {
    int i;
    for (i = 0; i < n; i++) {
        if (arr[i] == x)
            return i;
    }
    return -1; // 如果元素不存在
}

// 主函数
int main() {
    int arr[] = {2, 3, 4, 10, 40};
    int n = sizeof(arr) / sizeof(arr[0]);
    int x = 10;
    
    int result = linearSearch(arr, n, x);
    
    if (result == -1)
        printf("元素不在数组中\n");
    else
        printf("元素在索引 %d 处找到\n", result);
    
    return 0;
}