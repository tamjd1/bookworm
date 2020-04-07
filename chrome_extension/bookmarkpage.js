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
  dump();

  makeXHR('http://localhost:5000/recommended');
  //makeCorsRequest();
});
//This should ping the server and then append the body of the html received to the div...but??
function reqListener () {
		console.log(this.response);
	$('#recommended').append("<h1 id='rechead'>Recommended site: </h1>");
	for (j = 0; j < this.response.length; j++){	
	curRec = this.response[j];
	recommended = curRec.title+"<br />Highlights: ";
	
	for (i = 0; i < curRec.highlights.length; i++){
		recommended += curRec.highlights[i]+"<br />";
	}
	$('#recommended').append(recommended);
	anchor = '<a href='+curRec.link+' >'+curRec.link+'</a>';			
	$('#recommended').append(anchor);
	}
	/* var metadata = "Your bookmarks at a glance: <br />Total Bookmarks: "+this.response.totalBookmarks+"<br />Most Visited: "+this.response.mostVisited+"<br /> Latest Bookmark Added: "+this.response.latest+"<br />Oldest Bookmark: "+this.response.oldest;
   $('#metadata').append(metadata); */
}
function makeXHR (url) {
var xhr = new XMLHttpRequest();
xhr.addEventListener("load", reqListener);
xhr.open("GET", url);
xhr.responseType = "json";
xhr.send();
}

//end ping and append





function dump(){
	tableHeaders = "<tr><td></td><td>Date Added</td><td>Date Visited Last</td></tr></table>"
	$('#bookmarks').append(tableHeaders);
	  	addlink = $('<span>[<a href="#" id="addlink">Add a bookmark</a>]</span>');
	$('#addbookmark').append(addlink);
	chrome.bookmarks.getTree(function(items){		
		items.forEach(function(item){
processNode(item);
		});
	});

}

function processNode(node) {
var span = $('<tr class="entryBox">');
    // recursively process child nodes
    if(node.children) {
        node.children.forEach(function(child) { processNode(child); });
    }

    // push leaf node URLs to the bookmarks array
    if(node.url) { 	
	var dateAdded = new Date(node.dateAdded);
	
	chrome.history.getVisits({url:node.url},
	function(items){
	var dateVisited = new Date(items[items.length-1].visitTime);
		var atext = "<td class='entryTitle'><a href="+node.url+" >"+node.title+"</a></td><td class='edateAdd'>"+dateAdded.toLocaleDateString()+"</td><td class='edatevis'>"+dateVisited.toLocaleDateString()+"</td><td>";
		

			 var options = $('<span>[<a id="editlink" href="#">Edit</a> <a id="deletelink" ' +
        'href="#">Delete</a>]</span>');
    var edit = node.children ? $('<table><tr><td>Name</td><td>' +
      '<input id="title"></td></tr><tr><td>URL</td><td><input id="url">' +
      '</td></tr></table>') : $('<input>');
    // Show add and edit links when hover over.
        span.hover(function() {
        span.append(options);
        $('#deletelink').click(function() {
          $('#deletedialog').empty().dialog({
			  	 dialogClass: "no-close",
                 autoOpen: false,
                 title: 'Confirm Deletion   ',
                 resizable: false,
                 height: 60,
				 width: '150',
                 modal: true,
				 position: {my:'center',at:'center',of:'#bookmarks'},
                 overlay: {
                   backgroundColor: '000000',
                   opacity: 0
                 },
                 buttons: {
                   'Delete It': function() {
                      chrome.bookmarks.remove(String(node.id));
                      span.parent().remove();
                      $(this).dialog('destroy');
                    },
                    Cancel: function() {
                      $(this).dialog('destroy');
                    }
                 }
               }).dialog('open');
         });
        $('#addlink').click(function() {
          $('#adddialog').empty().append(edit).dialog({
			  autoOpen: false,
              closeOnEscape: true, 
			  height: 75, 
			  width: '250', 
			  title: 'Add New Bookmark:   ',
			  modal: true,
			  position: {my:'center',at:'center',of:'#bookmarks'},
              show: 'slide',  buttons: {
            'Add' : function() {
               chrome.bookmarks.create({parentId: node.id,
                 title: $('#title').val(), url: $('#url').val()});
               $('#bookmarks').empty();
               $(this).dialog('destroy');
               window.dump();
             },
            'Cancel': function() {
               $(this).dialog('destroy');
            }
          }}).dialog('open');
        });
        $('#editlink').click(function() {
         edit.val(node.title);
         $('#editdialog').empty().append(edit).dialog({
			 dialogClass: "no-close",
			 autoOpen: false,
             closeOnEscape: true, 
			 height: 75, 
			 width: '250', 
			 title: 'Edit Bookmark Title:   ', 
			 modal: true, 
			 position: {my:'center',at:'center',of:'#bookmarks'},
           show: 'slide',  buttons: {
              'Save': function() {
                 chrome.bookmarks.update(String(node.id), {
                   title: edit.val()
                 }); 
				options.remove();				 
               $('#bookmarks').empty();
			   $('#editdialog').empty();
               $(this).dialog('destroy');
               window.dump();
              },
             'Cancel': function() {
                 $(this).dialog('destroy');
				 $('#editdialog').empty();
             }
         }}).dialog('open');
        });
        options.fadeIn();
      },
      // unhover
      function() {
        options.remove();
      }).append(atext);
			
			
	})
	$('#bookmarks').append(span);


	
}
}