
window.django = {jQuery: jQuery.noConflict(true)};


$(document).ready(function() {
    var searchInput = $('#search-navbar');
    var resultsDropdown = $('#search-results');

    console.log(searchInput)
    searchInput.on('input', function() {
        print('enter--')
      var query = searchInput.val();
      print(query)
      if (query.length >= 3) {
        // Make an AJAX request to the search view
        $.get('/search/', { q: query }, function(data) {
          // Clear previous results
          resultsDropdown.empty();
  
          // Populate the dropdown with the search results
          data.forEach(function(result) {
            resultsDropdown.append('<a href="/details/' + result.id + '">' + result.name + '</a>');
          });
  
          // Show the dropdown
          resultsDropdown.show();
        });
      } else {
        // Hide the dropdown if the query length is less than 3
        resultsDropdown.hide();
      }
    });
  });