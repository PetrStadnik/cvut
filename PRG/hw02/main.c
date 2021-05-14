#include <stdio.h>
#include <stdint.h>
#include <math.h>
#include <stdlib.h>

// překlad:  gcc -Wall -pedantic -std=c99 main.c -o main
//	clang -pedantic -Wall -Werror -std=c99 -O3 -lm

int main()
{
    int64_t vstup = 1;
    int kontrola_vstupu;
    while(vstup != 0){
        kontrola_vstupu = scanf("%ld", &vstup);
        if(vstup == 0){
            return 0;
        }
        if (vstup < 0 || kontrola_vstupu < 1){
            fprintf(stderr, "%s", "Error: Chybny vstup!\n");
            return 100;
        }
        else{
            if(vstup == 1){
                 printf("Prvociselny rozklad cisla %ld je:\n", vstup);
                printf("1\n");
            }
            else{
                printf("Prvociselny rozklad cisla %ld je:\n", vstup);
                int64_t delitel = 2;
                int64_t podil = vstup;
                int mocnina = 0;
                while (podil>1)
                {
                    if(podil%delitel == 0){
                        //printf("%ld", delitel);
                        mocnina++;
                        podil= podil/delitel;

                        if(podil==1){
                            if(mocnina>1){
                                printf("%ld^%d", delitel, mocnina);
                            }
                            else{
                                printf("%ld", delitel);
                            }
                        }
                    }
                    else{
                        if(mocnina>0){
                            if(mocnina>1){
                                printf("%ld^%d x ", delitel, mocnina);
                            }
                            else{
                                printf("%ld x ", delitel);
                            }
                        }    
                        delitel++;
                        mocnina = 0;
                    }
                }
                printf("\n");
            }
        }
    }
    return 0;
}
