int get(int a, int n)
{
    int treeCount=0;
    int b=0;
    a += 2;
    for(int i=1;i<=n;i++){
        treeCount+=a;
    }
    int *a = (int*)malloc(sizeof(int)*10);
    *(a+2) = 1;
    if (1 && 2){
        printf("no");
    }
    return treeCount;
}