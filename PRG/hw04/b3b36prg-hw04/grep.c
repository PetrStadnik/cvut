#include <stdio.h>
#include <stdlib.h>

#define ARRAY_SIZE 10

int myStrCmp(const char *str1, const char *str2)
{
  int i1 = 0;
  int i2 = 0;

  while (str1[i1] != '\0' && str2[i2] != '\0' && str1[i1] == str2[i2])
  {
    i1++;
    i2++;
  }

  return str1[i1] == str2[i2];
}

char *readLine(FILE *fid)
{
  int capacity = ARRAY_SIZE;
  char *ret = malloc(capacity + 1);
  if (!ret)
  {
    fprintf(stderr, "ERROR: Cannot allocate memory");
  }

  int len = 0;
  int r;
  while ((r = getc(fid)) && r != EOF && r != '\n')
  {
    if (len == capacity)
    {
      char *t = realloc(ret, capacity + ARRAY_SIZE + 1);
      if (t == NULL)
      {
        free(ret);
        fprintf(stderr, "ERROR: Cannot realloc\n");
        exit(-1);
      }
      ret = t;
      capacity += ARRAY_SIZE;
    }
    ret[len++] = r;
  }
  if (r == EOF && len == 0)
  {
    free(ret);
    ret = NULL;
  }
  else
  {
    ret[len] = '\0';
  }

  return ret;
}

unsigned long myStrLen(const char *str)
{
  unsigned long ret = 0;

  while (str && str[ret] != '\0')
  {
    ret++;
  }
  return ret;
}

int matchInputLine(FILE *fid, const char *pattern)
{
  int ret = -1;
  int r;
  int c = 0;
  int s = -1;
  int i = 0;
  while ((r = getc(fid)) != EOF && r != '\n')
  {

    if (ret == -1 && pattern)
    {

      if (r != pattern[i])
      {
        i = 0;
        s = -1;
      }
      if (r == pattern[i])
      {
        if (i == 0)
        {
          s = c;
        }
        i++;
      }
      if (pattern[i] == '\0')
      {
        ret = s;
      }
    }
    c++;
  }
  return ret;
}

int strMatchRE(const char *pattern, const char *str, unsigned long start)
{
  //int pattern_len = myStrLen(pattern);
  unsigned long i1 = start;
  unsigned long i2 = 0;
  int ret = -1;
  while (pattern[i2] != '\0' && str[i1] != '\0')
  {
    if (pattern[i2] == str[i1])
    {
      i2++;
    }
    else
    {
      i2 = 0;
    }
    i1++;

    if (pattern[i2 + 1] == '?')
    {
      if (pattern[i2] == str[i1])
      {
        i1 += 1;
      }
      i2 += 2;
    }
    if (pattern[i2 + 1] == '+')
    {
      if (pattern[i2] != str[i1])
      {
        i2 = 0;
      }
      while (pattern[i2] == str[i1])
      {
        i1 += 1;
      }
      i2 += 2;
    }
    if (pattern[i2 + 1] == '*')
    {
      while (pattern[i2] == str[i1])
      {
        i1 += 1;
      }
      i2 += 2;
    }
  }

  if (pattern[i2] == '\0')
  {
    ret = 1;
  }
  return ret;
}

int strMatch(const char *pattern, const char *str, unsigned long start)
{
  int ret = -1;
  unsigned long patternLen = myStrLen(pattern); // length of searchnig sring
  unsigned long strLen = myStrLen(str);         // length of strg where I am looking
  if (patternLen > strLen)
  {
    return -1;
  }
  unsigned long end = start + patternLen;
  while (end <= strLen)
  {
    int i1 = start;
    int i2 = 0;
    while (i1 < end && pattern[i2] == str[i1])
    {
      i1++;
      i2++;
      //printf("\ni1 = %d | i2 = %d", i1, i2);
    }
    if (pattern[i2] == '\0')
    {
      ret = start;
      break;
    }
    start++;
    end++;
  }
  return ret;
}

/* The main program */
int main(int argc, char *argv[])
{
  int returned_value = 0;
  int color = 0;
  int regular_expression = 0;

  const char *pattern;
  const char *file_name;
  if (myStrCmp(argv[1], "--color=always"))
  {
    color = 1;
    pattern = argc > 1 ? argv[2] : NULL;
    file_name = argc > 2 ? argv[3] : NULL;
  }
  else if (myStrCmp(argv[1], "-E"))
  {
    regular_expression = 1;
    pattern = argc > 1 ? argv[2] : NULL;
    file_name = argc > 2 ? argv[3] : NULL;
  }
  else
  {
    pattern = argc > 1 ? argv[1] : NULL;
    file_name = argc > 2 ? argv[2] : NULL;
  }

  if (!pattern)
  {
    fprintf(stderr, "Add pattern as program argument!\n");
    return 101;
  }
  FILE *fid;
  char *line;
  if (!file_name)
  {
    line = readLine(stdin);
  }
  else
  {
    fid = fopen(file_name, "r");
    if (fid == NULL)
    {
      fprintf(stderr, "Error: cannot open file %s\n", file_name);
      return 102;
    }
    line = readLine(fid);
  }

  int ln = 1;
  int count_lines = 0;
  int pattern_len = myStrLen(pattern);
  int m;
  while (line != NULL)
  {
    if (regular_expression)
    {
      m = strMatchRE(pattern, line, 0);
    }
    else
    {
      m = strMatch(pattern, line, 0);
    }

    if (m >= 0)
    {
      count_lines++;
      //printf("Line %03d - pattern match starts at %d in --%s\n", ln, m, line);
      if (color == 1)
      {
        int k = 0;
        while (k < myStrLen(line) - pattern_len && m >= 0)
        {
          while (k < m)
          {
            printf("%c", line[k]);
            k++;
          }
          printf("\033[01;31m\033[K");
          for (int i = 0; i < pattern_len; i++)
          {
            printf("%c", pattern[i]);
            k++;
          }
          printf("\033[m\033[K");
          m = strMatch(pattern, line, k);
        }
        while (k < myStrLen(line))
        {
          printf("%c", line[k]);
          k++;
        }
        printf("\n");
      }
      else
      {
        printf("%s\n", line);
      }
    }
    ln++;
    free(line);
    if (!file_name)
    {
      line = readLine(stdin);
    }
    else
    {
      line = readLine(fid);
    }
  }
  if (count_lines == 0)
  {
    returned_value = 1;
  }
  if (file_name)
  {
    fclose(fid);
    //free(fid);
  }

  return returned_value;
}
