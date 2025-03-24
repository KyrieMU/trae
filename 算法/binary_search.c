#include <stdio.h>

// 二分查找函数（递归版本）
int binarySearchRecursive(int arr[], int l, int r, int x) {
    if (r >= l) {
        int mid = l + (r - l) / 2;
        
        // 如果元素在中间位置
        if (arr[mid] == x)
            return mid;
        
        // 如果元素小于中间值，则在左半部分查找
        if (arr[mid] > x)
            return binarySearchRecursive(arr, l, mid - 1, x);
        
        // 否则在右半部分查找
        return binarySearchRecursive(arr, mid + 1, r, x);
    }
    
    // 元素不存在
    return -1;
}

// 二分查找函数（迭代版本）
int binarySearchIterative(int arr[], int l, int r, int x) {
    while (l <= r) {
        int mid = l + (r - l) / 2;
        
        // 检查中间位置
        if (arr[mid] == x)
            return mid;
        
        // 如果x大于中间值，忽略左半部分
        if (arr[mid] < x)
            l = mid + 1;
        
        // 如果x小于中间值，忽略右半部分
        else
            r = mid - 1;
    }
    
    // 元素不存在
    return -1;
}

// 主函数
int main() {
    int arr[] = {2, 3, 4, 10, 40};
    int n = sizeof(arr) / sizeof(arr[0]);
    int x = 10;
    
    int result = binarySearchIterative(arr, 0, n - 1, x);
    
    if (result == -1)
        printf("元素不在数组中\n");
    else
        printf("元素在索引 %d 处找到\n", result);
    
    return 0;
}