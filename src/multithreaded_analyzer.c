
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>

#define MAX_FILES 10
#define MAX_THREADS 8

typedef struct
{
    char filename[256];
    int count;
    int error;
} FileData;

typedef struct
{
    FileData* files;
    int start;
    int end;
    char target[100];
} ThreadData;

void* analyzeFiles(void* arg)
{
    ThreadData* data = (ThreadData*)arg;

    for (int i = data->start; i < data->end; i++)
    {
        FILE* file;
        char line[1024];

        data->files[i].count = 0;
        data->files[i].error = 0;

        file = fopen(data->files[i].filename, "r");

        if (file == NULL)
        {
            data->files[i].error = 1;
            continue;
        }

        while (fgets(line, sizeof(line), file) != NULL)
        {
            char* position = line;

            while ((position = strstr(position, data->target)) != NULL)
            {
                data->files[i].count++;
                position += strlen(data->target);
            }
        }

        fclose(file);
    }

    return NULL;
}

int main(int argc, char* argv[])
{
    pthread_t threads[MAX_THREADS];
    ThreadData threadData[MAX_THREADS];
    FileData files[MAX_FILES];

    if (argc < 4)
    {
        printf("Usage: ./multithreaded_analyzer TARGET THREAD_COUNT FILE1 FILE2 ...\n");
        return 1;
    }

    char* target = argv[1];
    int numberOfThreads = atoi(argv[2]);
    int numberOfFiles = argc - 3;

    if (numberOfThreads < 1 || numberOfThreads > MAX_THREADS)
    {
        printf("Error: Thread count must be between 1 and %d.\n",
               MAX_THREADS);
        return 1;
    }

    if (numberOfFiles > MAX_FILES)
    {
        printf("Error: Maximum %d files allowed.\n", MAX_FILES);
        return 1;
    }

    if (strlen(target) == 0 ||
        strlen(target) >= sizeof(threadData[0].target))
    {
        printf("Error: Invalid target word.\n");
        return 1;
    }

    if (numberOfThreads > numberOfFiles)
    {
        numberOfThreads = numberOfFiles;
    }

    for (int i = 0; i < numberOfFiles; i++)
    {
        int length = snprintf(
            files[i].filename,
            sizeof(files[i].filename),
            "%s",
            argv[i + 3]
        );

        if (length < 0 ||
            (size_t)length >= sizeof(files[i].filename))
        {
            printf("Error: Filename is too long.\n");
            return 1;
        }

        files[i].count = 0;
        files[i].error = 0;
    }

    int baseFiles = numberOfFiles / numberOfThreads;
    int extraFiles = numberOfFiles % numberOfThreads;
    int currentFile = 0;
    int createdThreads = 0;

    for (int i = 0; i < numberOfThreads; i++)
    {
        int filesForThisThread = baseFiles;

        if (i < extraFiles)
        {
            filesForThisThread++;
        }

        threadData[i].files = files;
        threadData[i].start = currentFile;
        threadData[i].end = currentFile + filesForThisThread;

        strcpy(threadData[i].target, target);

        int result = pthread_create(
            &threads[i],
            NULL,
            analyzeFiles,
            &threadData[i]
        );

        if (result != 0)
        {
            printf("Error: Could not create thread %d.\n", i + 1);
            break;
        }

        createdThreads++;
        currentFile += filesForThisThread;
    }

    for (int i = 0; i < createdThreads; i++)
    {
        pthread_join(threads[i], NULL);
    }

    int totalCount = 0;
    int hasError = 0;

    for (int i = 0; i < numberOfFiles; i++)
    {
        if (files[i].error)
        {
            printf("Error: Could not open %s\n", files[i].filename);
            hasError = 1;
        }
        else
        {
            printf("%s: %d occurrences\n",
                   files[i].filename,
                   files[i].count);

            totalCount += files[i].count;
        }
    }

    printf("Total occurrences: %d\n", totalCount);

    if (createdThreads != numberOfThreads)
    {
        return 1;
    }

    return hasError ? 1 : 0;
}
