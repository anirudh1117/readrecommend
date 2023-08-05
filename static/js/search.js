
let suggestions = [
  "Channel",
  "CodingLab",
  "CodingNepal",
  "YouTube",
  "YouTuber",
  "YouTube Channel",
  "Blogger",
  "Bollywood",
  "Vlogger",
  "Vechiles",
  "Facebook",
  "Freelancer",
  "Facebook Page",
  "Designer",
  "Developer",
  "Web Designer",
];

'use strict';
{
  (function () {
    document.addEventListener("DOMContentLoaded", function () {
      const searchInput = document.querySelector(".searchInput");
      const input = searchInput.querySelector("input");
      const resultBox = searchInput.querySelector(".resultBox");
      const icon = searchInput.querySelector(".icon");
      let linkTag = searchInput.querySelector("a");
      let webLink;

      // if user press any key and release
      input.onkeyup = (e) => {
        let userData = e.target.value; //user enetered data
        console.log(userData);
        let emptyArray = [];
        if (userData) {
          var xhr = new XMLHttpRequest();
          xhr.open('GET', '/people/search-celebrity/' + userData, true);
          xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 400) {
              var response = JSON.parse(xhr.responseText);
              // Update the options of the second field with the filtered options
              response.forEach(function (option) {
                let url = "/people/" + option.name_slug + "-books";
                let data = '<a href=' + url +  '> <li>' + option.name + '</li></a>'
                emptyArray.push(data);
              });

              searchInput.classList.add("active"); //show autocomplete box
              showSuggestions(emptyArray, e.target);
              let allList = resultBox.querySelectorAll("li");
              for (let i = 0; i < allList.length; i++) {
                //adding onclick attribute in all li tag
                allList[i].setAttribute("onclick", "select(this)");
              }
            }
          };
          xhr.send();
        } else {
          searchInput.classList.remove("active"); //hide autocomplete box
        }
      }

      function showSuggestions(list, inputBox) {
        let listData;
        if (!list.length) {
          userValue = inputBox.value;
          listData = '<li>' + userValue + '</li>';
        } else {
          listData = list.join('');
        }
        resultBox.innerHTML = listData;
      }
    })
  })();
}
