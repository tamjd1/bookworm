// Check whether new version is installed
chrome.runtime.onInstalled.addListener(function(details){
    if(details.reason == "install"){
        console.log("This is a first install!");
		console.log("Parsing all bookmarks!");
		$.when(dump()).then(setTimeout(function(){toastpopup('All bookmarks have been sent to Bookworm. Welcome!')},3000));
    }else if(details.reason == "update"){
        var thisVersion = chrome.runtime.getManifest().version;
        console.log("Updated from " + details.previousVersion + " to " + thisVersion + "!");			
	   var opt = {
	   type: "basic",
	   title:"Bookworm Version!",
	   message:"Bookworm was updated to version: "+thisVersion,
	   iconUrl:"icon.png",	   
   }
   chrome.notifications.create(opt);
    }
});

chrome.bookmarks.onCreated.addListener(function(id,bookmark){
	console.log("Listerner Fired for create!");	
	$.when(bwpost(id,bookmark.url)).then(toastpopup(bookmark.url+" has been added to bookworm"));	

});

chrome.bookmarks.onRemoved.addListener(function(id,bookmark){
	console.log("Listerner Fired for delete!");	
	$.when(bwdel(id)).then(toastpopup(bookmark.node.url+" has been deleted from bookworm"));

});

function toastpopup (message){
	var opt = {
	   type: "basic",
	   title:"Bookworm",
	   message:message,
	   iconUrl:"icon.png",	   
   }
   chrome.notifications.create(opt);
}



function bwpost(id, url)
{
  try {	  	
	const response = axios.post('http://localhost:5000/bookmark',
	                                  {"chromeId":parseInt(id),"link":url});
									  								  
return console.log(response.data);
   } catch (error) {
	   console.error("chromeId:"+id+"   URL:"+url)
    console.error(error);
  }	
}

async function bwdel(id)
{
  try {
	 url = 'http://localhost:5000/bookmark/'+id;
	const response = await axios.delete(url);	                                  
return console.log(response.data);
   } catch (error) {
    console.error(error);
  }	
}


var bookmarkJson = '{"bookmarks":['
var firstNode = true;
function dump(){

	chrome.bookmarks.getTree(function(items){		
		items.forEach(function(item){
processNode(item);
		});
	});
setTimeout(axiosinit,3000);

}

function processNode(node) {

    // recursively process child nodes
    if(node.children) {
        node.children.forEach(function(child) { processNode(child); });
    }

    // push leaf node URLs to the bookmarks array
    if(node.url) { 
	if (firstNode)
	{
		bookmarkJson += '{"chromeId":'+parseInt(node.id)+',"link":"'+node.url+'"}';;			
			firstNode = false;
	}
	else 
	{
			bookmarkJson +=  ',{"chromeId":'+parseInt(node.id)+',"link":"'+node.url+'"}';
	}
	 }
}


async function axiosinit()
{
	bookmarkJson += "]}";
	console.log(bookmarkJson);
  try {
	const response = await axios.post('http://localhost:5000/init',bookmarkJson,{headers: {'Content-Type': 'application/json'}});
return console.log(response);
   } catch (error) {
    console.error(error);
  }	
}