#include <cs50.h>
#include <stdio.h>

void print_right_side(int bricks);
void print_left_side(int bricks, int spaces);

int main(void)
{
    int height;

    do
    {
        height = get_int("Enter the height of the pyramid: ");
    }
    while (height <= 0 || height > 8);

    for (int i = 0; i < height; i++)
    {
        int bricks_l = i + 1;
        int bricks_r = i + 1;
        int spaces = height - i - 1;
        print_left_side(bricks_l, spaces);
        print_right_side(bricks_r);
        printf("\n");
    }
}

void print_right_side(int bricks_r)
{
    for (int b = 0; b < bricks_r; b++)
    {
        printf("#");
    }
}

void print_left_side(int bricks_l, int spaces)
{
    for (int s = 0; s < spaces; s++)
    {
        printf(" ");
    }
    for (int b = 0; b < bricks_l; b++)
    {
        printf("#");
    }
    printf("  ");
}
