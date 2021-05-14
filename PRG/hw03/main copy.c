#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

#define ARRAY_SIZE 5

void shift(int* arr, int arr_len){
     for(int i = 0; i<arr_len; i++){
          if(arr[i] == 'Z'){
               arr[i] = arr[i] + ('a' - 'Z');
          }else if(arr[i] == 'z'){
               arr[i] = arr[i] - ('z' - 'A');
          }else{
               arr[i]++;
          }
     }
}

int compare(int* first_arr, int* second_arr, int arr_len){
     int comformity = 0;
     for(int i = 0; i < arr_len; i++){
          if(first_arr[i] == second_arr[i]){
               comformity++;
          }
     }
     return comformity;
}

void* mem_alloc(unsigned int size){
     void *ptr = malloc(size); //call malloc to allocate memory

     if (ptr == NULL){
          fprintf(stderr, "Error: allocation fail"); //report error
          exit(-1);
     }
     return ptr;
}

void mem_release(void **ptr){
     // 1st test ptr is valid pointer, and also *ptr is a valid
     if (ptr != NULL && *ptr != NULL){
          free(*ptr);
          *ptr = NULL;
     }
}

int main(void){
     int number_of_chars = 0;
     int ch;

     int *first_line = mem_alloc(ARRAY_SIZE* sizeof(int)); // allocate 10 integers for first time
     int actual_array_size = 5;

    

     while ((ch=getchar()) != EOF ){
          if(ch == '\n'){
               printf("STOP\n");
               break;
          }
          else{
               if(ch < 'A' || ch > 'z' || (ch > 'Z' && ch< 'a')){
                    fprintf(stderr, "Error: Chybny vstup!\n");
                    return 100;
               }
               if (actual_array_size == number_of_chars){
                    printf("rozsiruji pamet");

                    int * t = realloc(first_line, (actual_array_size + 5        ) * sizeof(int));
                    if (t){
                         first_line = t; //realloc handle possible allocation of new memory block  
                         actual_array_size = actual_array_size + 5;            
                    }else{
                         fprintf(stderr, "ERROR: realloc fail\n");
                    }

               }
               printf("Znak %c: ", ch);
               first_line[number_of_chars] = ch;
               number_of_chars++;     
          }
     }

     int second_line[number_of_chars]; // inicialize array for second line with same number of chars
     for(int i = 0; i<=number_of_chars; i++){
          int c = getchar();
          
          if((c < 'A' || c > 'z' || (c > 'Z' && c< 'a')) && c != '\n'){
                    fprintf(stderr, "Error: Chybny vstup!\n");
                    return 100;
               }

          if((i != number_of_chars && c == '\n')|| (i == number_of_chars && c != '\n')){ //check if both inputs have the same length
               fprintf(stderr, "Error: Chybna delka vstupu!\n");
               return 101;
          }else{
               second_line[i] = c;
          }
          
     }

     for (int i = 0; i<number_of_chars; i++){
          printf("%c\n", first_line[i]);
     }
     printf("Druhy:");
     for (int i = 0; i<number_of_chars; i++){
          printf("%c\n", second_line[i]);
     }


     int result_array[number_of_chars];
     int comformity = 0;
     for(int k = 0; k <= 'Z'-'A'+'z'-'a'+2; k++){
          int comp =compare(first_line, second_line, number_of_chars);
          if (comp>comformity){
               comformity = comp;
               for (int i = 0; i<number_of_chars; i++){
               result_array[i] = first_line[i];
               }
          }
          
          printf("\nk %d: - %d --", k, comp);
          for (int i = 0; i<number_of_chars; i++){
               
               printf("%c", first_line[i]);
          }
          shift(first_line, number_of_chars);
     }


     for (int i = 0; i<number_of_chars; i++){
          printf("%c", result_array[i]);
     }
     

     mem_release((void**)&first_line);
     //mem_release((void**)&second_line);
     return 0;
}


