#include <stdio.h>

// 冒泡排序函数
void bubbleSort(int arr[], int n) {
    int i, j, temp;
    for (i = 0; i < n-1; i++) {
        // 每次循环将最大的元素冒泡到末尾
        for (j = 0; j < n-i-1; j++) {
            // 如果当前元素大于下一个元素，则交换它们
            if (arr[j] > arr[j+1]) {
                temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}

// 打印数组函数
void printArray(int arr[], int size) {
    int i;
    for (i = 0; i < size; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

// 主函数
int main() {
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    int n = sizeof(arr) / sizeof(arr[0]);
    
    printf("排序前的数组: \n");
    printArray(arr, n);
    
    bubbleSort(arr, n);
    
    printf("排序后的数组: \n");
    printArray(arr, n);
    
    return 0;
}