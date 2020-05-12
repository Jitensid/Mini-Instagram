//when the page is loaded execute the following function
$(function(){
	$('#search').keyup(function(){

		$.ajax({
			type: "POST"
			url: "social/search"  //url of the page where the ajax result needs to be dislplayed!!!
			data: {
				'search_text': $('#search').val() //get value from the search box !!
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success : searchSuccess,  //if successfull call searchSuccess function
			dataType : 'html'   	  //datatype of the result given back to us!!!!
		});


	});



});

function searchSuccess(data, textStatus, jqXHR)
{
	$('#search_results').html(data)  //append the result into the ul search_results
}