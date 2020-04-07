// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
// Search the bookmarks when entering the search keyword.

// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Search the bookmarks when entering the search keyword.

$(function() {
	$('#search').change(function() {
    url = 'bookworm-search.html?q='+$('#search').val();
	chrome.tabs.create({url});
	})
});


document.addEventListener('DOMContentLoaded', function () {
  makeXHR('http://localhost:5000/metadata',reqListener);
  makeXHR('http://localhost:5000/recommended',reqListener2); 
});
//This should ping the server and then append the body of the html received to the div...but??
function reqListener () {
	var metadata = "Your bookmarks at a glance: <br />Total Bookmarks: "+this.response.totalBookmarks+"<br />Most Visited: "+this.response.mostVisited+"<br /> Latest Bookmark Added: "+this.response.latest+"<br />Oldest Bookmark: "+this.response.oldest;
   $('#metadata').append(metadata);
}
function makeXHR (url, listener) {
var xhr = new XMLHttpRequest();
xhr.addEventListener("load", listener);
xhr.open("GET", url);
xhr.responseType = "json";
xhr.send();
}
//end ping and append



function reqListener2 () {
	console.log(this.response);
	$('#recommended').append("Recommended site: ");
	for (j = 0; j < this.response.length; j++){	
	curRec = this.response[j];
	recommended = "<br />"+curRec.title+"<br />Highlights:";
	
	for (i = 0; i < curRec.highlights.length; i++){
		recommended += curRec.highlights[i]+"<br />";
	}
	$('#recommended').append(recommended);
	anchor = '<a href='+curRec.link+' >'+curRec.link+'</a>';			
	$('#recommended').append(anchor);
	}
}


