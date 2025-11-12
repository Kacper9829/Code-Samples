//word of the day
document.addEventListener("DOMContentLoaded", () => {
    function wordOfTheDay(){
        // find today's date
        const today = new Date();
        // map date to the array
        const number = today.getDate() % words.length
        const todaysWord = words[number]
        document.getElementById("dayilyWord").innerHTML = `EN: ${todaysWord.word} PL: ${todaysWord.pl}, CN: ${todaysWord.zh}`;
    }
    wordOfTheDay();
});

let index = 0;
document.addEventListener("DOMContentLoaded", () => {
    //listen for the click of the "New Word" button
    document.getElementById("newWord").addEventListener("click", () => {
        // Get the word from words based on index
        document.getElementById("word").innerText = words[index].word;
        // return worda and it's equivalents
        document.getElementById("equivalent").innerText = `PL: ${words[index].pl} CN: ${words[index].zh}`;
        // next index for the next word
        index = (index + 1) % words.length;
})
});
