// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Search the bookmarks when entering the search keyword.

$(function() {
  $('#search').change(function() {
    url = 'bookworm-search.html?q='+$('#search').val();
	location.href = url;
  });
});


document.addEventListener('DOMContentLoaded', function () {
	var urlParams = new URLSearchParams(window.location.search)
	$('#search').val(urlParams.get('q'));
  makeXHR('http://localhost:5000/search?'+urlParams.toString(),reqListener);
});

function makeXHR (url, listener) {
var xhr = new XMLHttpRequest();
xhr.addEventListener("load", listener);
xhr.open("GET", url);
xhr.responseType = "json";
xhr.send();
return xhr;
}
//end ping and append


async function reqListener () {
	if (this.response.length == 0){$('#results').append('<p>No Search Results Found</p>');	}
	for (i = 0; i < this.response.length; i++){
		searchResults = $('<p>')
		searchResults.append("<h1>"+this.response[i].title+"</h1>");
		searchResults.append(this.response[i].matchedText);
		anchor = $('<a>');
		anchor.attr('href', this.response[i].link);
		url = this.response[i].link;
		anchor.html(url);		
		var highlightResponse = await makeXHR('http://localhost:5000/highlights/'+this.response[i].chromeId,reqListener2);
		const result = await resolveAfterMS(50);

		var n;
		var highlights = "";		
		for (n = 0; n < highlightResponse.response.highlights.length; n++){
		highlights += highlightResponse.response.highlights[n]+"<br />";}
		
		//console.log(highlights);
		anchor.tooltip({items: anchor, content: highlights,
		show: "slideDown", // show immediately
               open: function(event, ui) {
                  ui.tooltip.hover(
                  function () {
                     $(this).fadeTo("slow", 0.5);
                  });
               }
		})

searchResults.append('<p>');
searchResults.append(anchor);
searchResults.append('</p>');
	$('#results').append(searchResults);	
	}

	}


function reqListener2 (){
}
function resolveAfterMS(ms) {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve('resolved');
    }, ms);
  });
}
