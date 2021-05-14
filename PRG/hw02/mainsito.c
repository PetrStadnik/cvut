#include <stdio.h>
#include <stdint.h>
#include <math.h>
#include <stdlib.h>

// překlad:  gcc -Wall -pedantic -std=c99 main.c -o main

int main()
{
    int hranice = 1000000;
    int8_t pole_cisel[hranice+1];
    for(int i = 0; i < hranice+1 ; pole_cisel[i++] = 1);
    //for(int i = 0; i < hranice+1 ; i++){
      //  printf("%d -- %d\n", i, pole_cisel[i]);
    //}

    int pocet_prvocisel = 0;
    int nasobek;
    int odmocnina = sqrt(hranice);
    for (int i = 2; i < odmocnina; i++)
    {
        
        if(pole_cisel[i]==1){
            nasobek = i;
            // printf("%d", i);
            while(nasobek < hranice+2)
            {
                nasobek = nasobek + i;
                pole_cisel[nasobek] = 0;
                //printf("%d", i);
            }
        }
        //for(int i = 0; i < hranice+1 ; i++){
        //printf("%d -- %d\n", i, pole_cisel[i]);
        //}
    }

    for(int i = 1; i < hranice+1 ; i++){
        if(pole_cisel[i] == 1){
            pocet_prvocisel++;
        }
    }


    int prvocisla[pocet_prvocisel];
    int k = 0;
    for(int i = 1; i<hranice+2; i++){
        //printf("%d", pole_cisel[i]);
        if(pole_cisel[i] == 1){
            prvocisla[k] = i;
            k++;
            //printf("%d", i);
        }
    }
    



    int len = sizeof(prvocisla)/sizeof(prvocisla[0]);
    
    for(int i = 0; i < len; i++ ){
        //printf("%ld\n", prvocisla[i]);
    }
    printf("pocet %ld\n", len);

    int vstup;
    int kontrola_vstupu;
    while(kontrola_vstupu = scanf("%ld", &vstup) && vstup != 0){
        if (vstup < 0 || kontrola_vstupu != 1 ){
            fprintf(stderr, "%s", "Error: Chybny vstup!\n");
            return 100;
        }
        else{

            //printf("%ld\n", vstup);

        }
    }

    return 0;


}