

$(document).ready(function(){
 
   $("#success").hide();
   $("#failed").hide();

});


function extract_file(fname) 
{

localStorage.setItem("Start", "False");

var request = $.ajax({
  type:"GET",
  url : '/extract/'+fname,
  dataType: '', 
      
  success: function(data) {
          var msg = "<strong>Success!</strong> File: "+fname;
          $("#successm").html(msg);
          $("#success").show();

          window.setInterval(function() {
               window.location.replace("/reports/"); 
          }, 2000);
          
  },

  error: function (request, status, error) {
          var msg = "<strong>Error!</strong> Better check yourself, you're not looking too good."
          $("#failedm").html(msg);
          $("#failed").show();

          window.setInterval(function() {
               window.location.replace("/reports/"); 
          }, 2000);
  }


 });

    
}



$("#unco").click(function() {
	var fname=$("#unco").data("name");
	extract_file(fname);
});



