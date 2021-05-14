#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

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

     int *first_line = mem_alloc(ARRAY_SIZE* sizeof(int)); // allocate 5 integers for first time
     int actual_array_size = ARRAY_SIZE;

    
     while ((ch=getchar()) != EOF ){ // read first line
          if(ch == '\n'){
               break;
          }
          else{
               if(ch < 'A' || ch > 'z' || (ch > 'Z' && ch< 'a')){
                    fprintf(stderr, "Error: Chybny vstup!\n");
                    mem_release((void**)&first_line);
                    return 100;
               }
               if (actual_array_size == number_of_chars){
                    int * t = realloc(first_line, (actual_array_size + 5) * sizeof(int));
                    if (t){
                         first_line = t; //realloc handle possible allocation of new memory block  
                         actual_array_size = actual_array_size + 5;            
                    }else{
                         fprintf(stderr, "ERROR: realloc fail\n");
                    }
               }
               first_line[number_of_chars] = ch;
               number_of_chars++;     
          }
     }

     int *second_line = mem_alloc(number_of_chars * sizeof(int));// inicialize array for second line with same number of chars
     for(int i = 0; i<=number_of_chars; i++){
          int c = getchar();
          
          if((c < 'A' || c > 'z' || (c > 'Z' && c< 'a')) && c != '\n'){
                    fprintf(stderr, "Error: Chybny vstup!\n");
                    mem_release((void**)&first_line);
                    mem_release((void**)&second_line);
                    return 100;
               }

          if((i != number_of_chars && c == '\n')|| (i == number_of_chars && c != '\n')){ //check if both inputs have the same length
               fprintf(stderr, "Error: Chybna delka vstupu!\n");
               mem_release((void**)&first_line);
               mem_release((void**)&second_line);
               return 101;
          }else{
               if(i<number_of_chars){
                      second_line[i] = c;
               }
          }  
     }

     int *result_array = mem_alloc(number_of_chars * sizeof(int));
     int comformity = 0;
     for(int k = 0; k <= 'Z'-'A'+'z'-'a'+2; k++){
          int comp = compare(first_line, second_line, number_of_chars);
          if (comp>comformity){
               comformity = comp;
               for (int i = 0; i<number_of_chars; i++){
               result_array[i] = first_line[i];
               }
          }
          shift(first_line, number_of_chars);
     }

     for (int i = 0; i<number_of_chars; i++){ 
          printf("%c", result_array[i]);
     }
     printf("\n");
     mem_release((void**)&first_line);
     mem_release((void**)&second_line);
     mem_release((void**)&result_array);
     return 0;
}


