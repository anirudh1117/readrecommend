'use strict';
{
    (function () {
        document.addEventListener("DOMContentLoaded", function () {
            console.log("enterrr..")
            const readMoreLink = document.querySelector("#read-more");
            const hiddenText = document.querySelector(".hidden-text");
            const description = document.getElementById('#book-description');

            const maxTextLength = 100; // Maximum characters to show before truncating

            // Get the full text and truncated text
            //const fullText = description.textContent;
            console.log(description)
            const truncatedText = fullText.slice(0, maxTextLength) + "...";

            // Set the truncated text as the initial content
            description.textContent = truncatedText;
            readMoreLink.click = ReadMoreFunction;
            function ReadMoreFunction(event) {
                event.preventDefault();
                console.log("here--")
                if (description.textContent === truncatedText) {
                    // Switch to full text
                    description.textContent = fullText;
                    readMoreLink.textContent = "Read Less";
                } else {
                    // Switch back to truncated text
                    description.textContent = truncatedText;
                    readMoreLink.textContent = "Read More";
                }
            };
        });
    })();
}
