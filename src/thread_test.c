#include <stdio.h>
#include <pthread.h>

void* myThreadFunction(void* arg)
{
    printf("Hello from a separate thread!\n");
    return NULL;
}

int main()
{
    pthread_t thread;

    pthread_create(&thread, NULL, myThreadFunction, NULL);

    pthread_join(thread, NULL);

    printf("Main thread finished.\n");

    return 0;
}
