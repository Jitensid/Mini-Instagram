function fetch_results(){

	var searchField = $('#search').val()    //fetching the text from the search box

	if(searchField==""){					//if text is empty
    
    $('#search_results').html("");   //to empty the result list
    return;                  //return to stop the execution of tehe function
	}
		$.ajax({
			type: "POST",
			url: "search/",  //url of the page from where the ajax result needs to be dislplayed!!!
			data: {
				'search_text': $('#search').val(), //get value from the search box !!
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success : searchSuccess,  //if successfull call searchSuccess function
			dataType : 'html'   	  //datatype of the result given back to us!!!!
		});

}


function searchSuccess(data, textStatus, jqXHR)
{
	$('#search_results').html(data)  //append the result into the ul search_results
}

function followFunction(csrf_token){

   $.ajax({

      type: "POST",
      url: "follow/",
      dataType: "application/json",

      data: {
                'csrfmiddlewaretoken' : csrf_token,
      },
      success: followSuccess(),

      complete : function(data){
        res = JSON.parse(data.responseText);
        document.getElementById("change_no_of_followers").innerHTML = res["no_of_followers_after_ajax"];
      }

    });

  }

  function followSuccess(){
    document.getElementById("follow_button").style.display = "none";
    document.getElementById("unfollow_button").style.display = "block";
    document.getElementById("message_button").style.display = "block";
  }

  function unfollowFunction(csrf_token){
    

    $.ajax({

      type : "POST",
      url : "unfollow/",
      dataType: "application/json",

      data: {
                'csrfmiddlewaretoken' : csrf_token,

      },
      success: unfollowSuccess(),
    
      complete : function(data){
        res = JSON.parse(data.responseText);
        document.getElementById("change_no_of_followers").innerHTML = res["no_of_followers_after_ajax"];
         }

    });

  }

  function unfollowSuccess(){
    document.getElementById("follow_button").style.display = "block";
    document.getElementById("unfollow_button").style.display = "none";
    document.getElementById("message_button").style.display = "none";
  }  




function like_an_image(imageid,csrf_token){

    $.ajax({

      type : "POST",
       
      url : "like/",

      dataType: "application/json",
      
      data: {
        'imageid' : imageid,
        'csrfmiddlewaretoken' : csrf_token,
      },

      success: after_liking(imageid),

      complete : function(data){
        res = JSON.parse(data.responseText);
        document.getElementById("like_counter_" + imageid).innerHTML = res["no_of_likes"];

      }

    });

  }

  function after_liking(imageid){
      document.getElementById("liked_icon_" + imageid).style.display = "block";
      document.getElementById("not_liked_icon_" + imageid).style.display = "none";
  }


  function unlike_an_image(imageid, csrf_token){

    $.ajax({

      type : "POST",

      url : "unlike/",

      dataType: "application/json",
      
      data: {
        'imageid' : imageid,
        'csrfmiddlewaretoken' : csrf_token,
      },

      success: after_unliking(imageid),

      complete : function(data){
            res = JSON.parse(data.responseText);
            document.getElementById("like_counter_"+imageid).innerHTML = res["no_of_likes"];
      }

    });

  }

  function after_unliking(imageid){
      document.getElementById("liked_icon_" + imageid).style.display = "none";
      document.getElementById("not_liked_icon_" + imageid).style.display = "block";
  }
