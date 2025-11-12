#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_sentences(string text);
int count_words(string text);

int main(void)
{
    // get text from user
    string text = get_string("Enter text to evaluate: ");
    // count letters
    double letter_count = count_letters(text);
    // count sentences
    double sentence_count = count_sentences(text);
    // count words
    double word_count = count_words(text);

    // count readability
    double index = 0.0588*((letter_count/word_count)*100) - 0.296*((sentence_count/word_count)*100) - 15.8;

    // print answer
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        int int_index = round(index);
        printf("Grade %i\n", int_index);
    }
}
// count letters in the text
int count_letters(string text)
{
    int letters = 0;
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
        else
        {
        }
    }
    return letters;
}
// count sentences in the text
int count_sentences(string text)
{
    int sentences = 0;
    for (int j = 0, len = strlen(text); j < len; j++)
    {
        if (text[j] == '.' || text[j] == '!' || text[j] == '?')
        {
            sentences++;
        }
        else
        {
        }
    }
    return sentences;
}
// count words
int count_words(string text)
{
    int words = 0;
    for (int w = 0, len = strlen(text); w < len; w++)
    {
        if (isspace(text[w]))
        {
            words++;
        }
        else
        {
        }
    }
    return words + 1;
}
