#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

#define MAX_ERATOSTHEN_NUMBER 1000000

#define ERROR_MALLOC 101
#define INPUT_ERROR 100

#define RETURN_SUCCESS 0

void eratosthenes(char *sieve, int max)
{
    for (int i = 0; i < max; i++)
    {
        sieve[i] = 1;
    }

    for (int i = 2; i < sqrt(max); i++)
        if (sieve[i])
        {
            for (int j = i * i; j < max; j += i)
            {
                sieve[j] = 0;
                //printf("%d\n",j);
            }
        }
}

int get_nubmber_of_PN(char *sieve)
{
    int number = 1;
    for (int i = 3; i < MAX_ERATOSTHEN_NUMBER; i++)
        if (sieve[i])
            number++;
    return number;
}

void get_prime_numbers(char *sieve, int64_t *prime_numbers)
{
    int k = 0;
    for (int i = 2; i < MAX_ERATOSTHEN_NUMBER; i++)
    {
        if (sieve[i])
        {
            prime_numbers[k] = i;
            k++;
        }
    }
}

void mem_release(void **ptr)
{
    // 1st test ptr is valid pointer, and also *ptr is a valid
    if (ptr != NULL && *ptr != NULL)
    {
        free(*ptr);
        *ptr = NULL;
    }
}

int main(int argc, const char **argv)
{
    int returned_value = RETURN_SUCCESS;

    char *sieve = (char *)malloc(sizeof(char) * MAX_ERATOSTHEN_NUMBER);
    if (sieve)
    {
        eratosthenes(sieve, MAX_ERATOSTHEN_NUMBER);
    }
    else
    {
        fprintf(stderr, "Error: allocation fail"); //report error
        returned_value = ERROR_MALLOC;
    }

    int64_t *prime_numbers;
    if (returned_value == RETURN_SUCCESS)
    {

        prime_numbers = malloc(sizeof(int64_t) * get_nubmber_of_PN(sieve));
        if (prime_numbers)
        {
            get_prime_numbers(sieve, prime_numbers);
            mem_release((void **)&sieve);
        }
        else
        {
            fprintf(stderr, "Error: allocation fail"); //report error
            returned_value = ERROR_MALLOC;
        }
    }

    int64_t input = 1;
    while (input != 0 && returned_value == RETURN_SUCCESS)
    {
        if (scanf("%ld", &input))
        {
            if (input == 0)
            {
                break;
            }
            if (input < 0)
            {
                fprintf(stderr, "%s", "Error: Chybny vstup!\n");
                returned_value = INPUT_ERROR;
            }
        }
        else
        {
            fprintf(stderr, "%s", "Error: Chybny vstup!\n");
            returned_value = INPUT_ERROR;
        }

        if (returned_value == RETURN_SUCCESS)
        {

            if (input == 1)
            {
                printf("Prvociselny rozklad cisla %ld je:\n", input);
                printf("1\n");
            }
            else
            {
                printf("Prvociselny rozklad cisla %ld je:\n", input);
                int64_t factor = prime_numbers[0];
                int64_t fraction = input;
                int exponent = 0;
                int i = 0;
                while (fraction > 1)
                {
                    if (fraction % factor == 0)
                    {
                        exponent++;
                        fraction = fraction / factor;

                        if (fraction == 1)
                        {
                            if (exponent > 1)
                            {
                                printf("%ld^%d", factor, exponent);
                            }
                            else
                            {
                                printf("%ld", factor);
                            }
                        }
                    }
                    else
                    {
                        if (exponent > 0)
                        {
                            if (exponent > 1)
                            {
                                printf("%ld^%d x ", factor, exponent);
                            }
                            else
                            {
                                printf("%ld x ", factor);
                            }
                        }
                        i++;
                        factor = prime_numbers[i];
                        exponent = 0;
                    }
                }
                printf("\n");
            }
        }
    }

    mem_release((void **)&prime_numbers);
    return returned_value;
}
