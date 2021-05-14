#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

//78497

void eratosthenovo_sito(char *sito, int64_t n)
{
    for (int64_t i = 0; i < n; i++)
        sito[i] = 1;

    for (int64_t i = 1, j = 3; i < n; i++, j += 2)
        for (int64_t k = j * j >> 1; k < n && sito[i]; k += j)
            sito[k] = 0;
}

int main(int argc, const char **argv)
{
    const int64_t limit = 1000000;
    const int64_t n = limit >> 1;

    char *sito = (char *)malloc(sizeof(char) * n);

    eratosthenovo_sito(sito, n);

    int64_t pocet_prvocisel = 1;
    int k = 1;
    for (int64_t i = 1, j = 3; i < n; i++, j += 2)
        if (sito[i])
            pocet_prvocisel++;

    int64_t prvocisla[pocet_prvocisel];

    prvocisla[0] = 2;
    for (int64_t i = 1, j = 3; i < n; i++, j += 2)
    {
        if (sito[i])
        {
            prvocisla[k] = j;
            k++;
        }
    }
    free(sito);
    for (int64_t i = 0; i < pocet_prvocisel; i++)
    {
        //printf("%ld\n", prvocisla[i]);
    }
    //printf("pocet: %ld", pocet_prvocisel);
    //printf("velikost: %ld", sizeof(prvocisla)/sizeof(prvocisla[0]));

    int64_t vstup = 1;
    int kontrola_vstupu;
    while (vstup != 0)
    {
        kontrola_vstupu = scanf("%ld", &vstup);
        if (vstup == 0)
        {
            return 0;
        }
        if (vstup < 0 || kontrola_vstupu < 1)
        {
            fprintf(stderr, "%s", "Error: Chybny vstup!\n");
            return 100;
        }
        else
        {
            if (vstup == 1)
            {
                printf("Prvociselny rozklad cisla %ld je:\n", vstup);
                printf("1\n");
            }
            else
            {
                printf("Prvociselny rozklad cisla %ld je:\n", vstup);
                int64_t delitel = prvocisla[0];
                int64_t podil = vstup;
                int mocnina = 0;
                int i = 0;
                while (podil > 1)
                {
                    if (podil % delitel == 0)
                    {
                        //printf("%ld", delitel);
                        mocnina++;
                        podil = podil / delitel;

                        if (podil == 1)
                        {
                            if (mocnina > 1)
                            {
                                printf("%ld^%d", delitel, mocnina);
                            }
                            else
                            {
                                printf("%ld", delitel);
                            }
                        }
                    }
                    else
                    {
                        if (mocnina > 0)
                        {
                            if (mocnina > 1)
                            {
                                printf("%ld^%d x ", delitel, mocnina);
                            }
                            else
                            {
                                printf("%ld x ", delitel);
                            }
                        }
                        i++;
                        delitel = prvocisla[i];
                        mocnina = 0;
                    }
                }
                printf("\n");
            }
        }
    }
    return 0;
}
