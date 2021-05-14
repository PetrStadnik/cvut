#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "math.h"

typedef struct
{
  unsigned char red, green, blue;
} Pixel;

int main(int argc, char **argv)
{
  FILE *in = fopen(argv[1], "rb");
  FILE *outText = fopen("output.txt", "w");
  FILE *outImage = fopen("output.ppm", "wb");
  int height, width, ccv;
  char header[100];
  if (fscanf(in, "%s %d %d %d", header, &width, &height, &ccv) != 4)
  {
    fprintf(stderr, "Error image format\n");
    exit(1);
  }

  fprintf(outImage, "P6\n%d\n%d\n%d\n", width, height, ccv);

  Pixel *pixels = malloc(width * height * sizeof(Pixel));
  Pixel *new_pixels = malloc(width * height * sizeof(Pixel));

  while (fgetc(in) != '\n')
    ;

  if (fread(pixels, 3 * width, height, in) != height)
  {
    fprintf(stderr, "Error loading image\n");
    exit(1);
  }

  int histogram[] = {0, 0, 0, 0, 0};

  for (int i = 0; i < height * width; i++)
  {
    if ((i) % width != 0 && (i + 1) % width != 0 && i > width && i < width * (height - 1))
    {
      int r = 5 * pixels[i].red - pixels[i + 1].red - pixels[i - 1].red - pixels[i + width].red - pixels[i - width].red;
      int g = 5 * pixels[i].green - pixels[i + 1].green - pixels[i - 1].green - pixels[i + width].green - pixels[i - width].green;
      int b = 5 * pixels[i].blue - pixels[i + 1].blue - pixels[i - 1].blue - pixels[i + width].blue - pixels[i - width].blue;
      if (r > 255)
      {
        r = 255;
      }
      if (r < 0)
      {
        r = 0;
      }

      if (g > 255)
      {
        g = 255;
      }
      if (g < 0)
      {
        g = 0;
      }

      if (b > 255)
      {
        b = 255;
      }
      if (b < 0)
      {
        b = 0;
      }
      new_pixels[i].red = r;
      new_pixels[i].green = g;
      new_pixels[i].blue = b;
    }
    else
    {
      new_pixels[i].red = pixels[i].red;
      new_pixels[i].green = pixels[i].green;
      new_pixels[i].blue = pixels[i].blue;
    }

    int y = round(0.2126 * new_pixels[i].red + 0.7152 * new_pixels[i].green + 0.0722 * new_pixels[i].blue);

    if (y <= 50)
    {
      histogram[0]++;
    }
    else if (y <= 101)
    {
      histogram[1]++;
    }
    else if (y <= 152)
    {
      histogram[2]++;
    }
    else if (y <= 203)
    {
      histogram[3]++;
    }
    else if (y <= 255)
    {
      histogram[4]++;
    }
  }

  fwrite(new_pixels, 3 * width, height, outImage);

  fprintf(outText, "%d %d %d %d %d", histogram[0], histogram[1], histogram[2], histogram[3], histogram[4]);

  fclose(in);
  fclose(outImage);
  fclose(outText);
  free(pixels);
  free(new_pixels);
  return(0);
}
