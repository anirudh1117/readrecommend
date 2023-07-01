
'use strict';
{
    (function() {
        document.addEventListener('DOMContentLoaded', function() {
          // Get references to the first and second many-to-many fields
          var firstField = document.querySelector('#id_categories');
          var secondField = document.querySelector('#id_sub_categories');

          //firstField.addEventListener('onchange', handleFirstFieldChange);
          //firstField.setAttribute("onchange", () => handleFirstFieldChange());
          firstField.onchange = handleFirstFieldChange;
          secondField.innerHTML = '';
          // Define a function to handle the change event of the first field
          function handleFirstFieldChange() {
            secondField.innerHTML = '';
            var selectedValues = Array.from(firstField.selectedOptions, function(option) {
              return option.value;
            });

            // Send an AJAX request to fetch the filtered options for the second field
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/api/subcategories/' + selectedValues.join(','), true);
            xhr.onload = function() {
              if (xhr.status >= 200 && xhr.status < 400) {
                var response = JSON.parse(xhr.responseText);
                // Update the options of the second field with the filtered options
                response.forEach(function(option) {
                  var optionElement = document.createElement('option');
                  optionElement.value = option.id;
                  optionElement.textContent = option.name;
                  secondField.appendChild(optionElement);
                });
              }
            };
            xhr.send();
          }
      
          // Attach the change event handler to the first field
      
          // Trigger the change event to initialize the options of the second field
          firstField.dispatchEvent(new Event('onchange'));
        });
      })();
      

}


