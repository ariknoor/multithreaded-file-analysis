#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
    char line[1024];
    char *target;
    int total_count = 0;

    if (argc < 3)
    {
        printf("Usage: ./analyzer TARGET FILE1 FILE2 ...\n");
        return 1;
    }

    target = argv[1];

    for (int i = 2; i < argc; i++)
    {
        FILE *file;
        int count = 0;

        file = fopen(argv[i], "r");

        if (file == NULL)
        {
            printf("Error: Could not open %s\n", argv[i]);
            continue;
        }

        while (fgets(line, sizeof(line), file) != NULL)
        {
            char *position = line;

            while ((position = strstr(position, target)) != NULL)
            {
                count++;
                position += strlen(target);
            }
        }

        fclose(file);

        printf("%s: %d occurrences\n", argv[i], count);

        total_count += count;
    }

    printf("Total occurrences: %d\n", total_count);

    return 0;
}

