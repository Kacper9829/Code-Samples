// Implements a dictionary's functionality
#include <cs50.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 100003;

// Set word counter
int word_count = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // hash word to find
    int hashed_word = hash(word);
    // set curosr at the right index
    node *cursor = table[hashed_word];
    // check if word is in dictioanry
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        // set cursor to the next position
        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // set hashed value to 0
    int hashed = 0;
    // hash the word using prime number, ASCII and modulo
    for (int i = 0, len = strlen(word); i < len; i++)
    {
        // set to uppercase
        char character = toupper(word[i]);
        hashed = (hashed * 33 + character) % N;
    }
    return hashed;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // open the dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    // set word count
    word_count = 0;
    char word[100];
    while (fscanf(file, "%99s", word) != EOF)
    {
        // create a node
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        // copy word into node
        strcpy(n->word, word);
        n->next = NULL;
        // hash word
        int index = hash(n->word);
        // insert hashed word into the table
        n->next = table[index];
        // update head of the table
        table[index] = n;
        word_count++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    if (word_count == 0)
    {
        printf("No dictionary loaded");
    }
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // loop through every bucket in the table
    for (int i = 0; i < N; i++)
    {
        // set the curosr at the beginig of the linked list
        node *cursor = table[i];
        // loop through linked list
        while (cursor != NULL)
        {
            // set temp curosr
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
