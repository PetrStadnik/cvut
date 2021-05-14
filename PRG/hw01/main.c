#include <stdio.h>

// překlad:  gcc -Wall -pedantic -std=c99 main.c -o main


int main()
{
    int a;
    int b;
    int c;
    int cs = 0;
    int ck;
    int plot = 0;
    int w = 1;
    int r = scanf("%d%d", &a, &b);
    if (r == 2){
        if (a>2 && a<70 && b>2 && b<70){
            if(a % 2 != 0){
                if(a==b){
                    int dr = scanf("%d", &c);
                    if(dr == 1){
                        if(c < b && c>0){
                            plot = 1;
                        }
                        else{
                            fprintf(stderr, "%s", "Error: Neplatna velikost plotu!\n");
                            return 103;
                        }
                    }
                    else{
                        fprintf(stderr, "%s", "Error: Chybny vstup!\n");
                        return 100;
                    }
                }

                int v = (a - 1)/2;
                int dv = (a - 1)/2;
                for(int i = 0; i < b+(a - 1)/2; i++){
                    for(int j = 0; j < a; j++){
                        if (v > 0){
                            if(j == dv){
                                printf("X");
                                break;
                            }
                            else if(j==v){
                                printf("X");
                            }
                            else{
                              printf(" ");
                            }                   
                        }
                        else{
                            if (v == 0 || i == b+(a - 1)/2-1){
                                printf("X");
                            }
                            else{
                                if(j==0 || j == a-1){
                                    printf("X");
                                }
                                else{
                                    if (plot != 1){
                                        printf(" ");
                                    }
                                    else{
                                        if(w==1){
                                            printf("o");
                                            w=0;
                                        }
                                        else{
                                            printf("*");
                                            w=1;
                                        }
                                    }
                                }
                            }
                        }      
                    }
                    if(plot == 1){
                            if (i>=b+(a - 1)/2-c){
                                if(c%2 != 0){
                                    ck = (c - 1)/2;
                                    cs = 0;
                                }
                                else{
                                    ck = c/2;
                                    cs = 1;
                                }
                                for(int p = 0; p<ck; p++){
                                    if(i==b+(a - 1)/2-c || i == b+(a - 1)/2-1){
                                        if (cs == 1){
                                            printf("-|");
                                        }
                                        else{
                                            printf("|-|");
                                            cs = 1;
                                        }
                                    }
                                    else{
                                        if (cs == 1){
                                            printf(" |");
                                        }
                                        else{
                                            printf("| |");
                                            cs = 1;
                                        }
                                    }

                                }
                            }
                            
                        }
                    v = v - 1;
                    dv = dv + 1; 
                    printf("\n");
                }
                return 0;
            }
            else{
                fprintf(stderr, "%s", "Error: Sirka neni liche cislo!\n");
                return 102;
            }
        }
        else{
            fprintf(stderr,"%s", "Error: Vstup mimo interval!\n");
            return 101;
        }
    }
    else{
        fprintf(stderr, "%s","Error: Chybny vstup!\n");
        return 100;
    }

    
}
