$(document).ready(function () {
  var totalcount=0;
  $('.js-example-basic-single').select2();
  $('.js-example-basic-multiple').select2({
    width:'300px'
  });
  $('.datepicker').datepicker();
  jQuery('.select2').select2({
    width:'150px'
  });
  $("#btnSave").click(function () {
    alert("Hi Lekshmi hello");
    $("#test").html("<h1>Hi Lekshmi</h1>");
  });
  jQuery("input.duplicatecheck:text").change(function(){
		var valinput=jQuery(this).val()
	  var objname=	$(this).attr("data-modelname")
    var objcolumnname=$(this).attr("data-fieldname")
    jQuery.ajax({
      type:"GET",
      url:'commonfunc',
      data:{
        objectname:objname,
        columnname:objcolumnname,
        columnvalue:valinput
      },
      success:function(response){
        alert(response)
      }
    })
		
	})
  function createpaginationcontrols(count){
    totalcount=jQuery('#hdTotalCount').val()
    jQuery('#first-get').empty()
    $('#page-links').empty();
    for (var i = 0; i < totalcount/2; i++) {
      
    var anchortag = document.createElement('a')
        anchortag.className = "pagination"
        anchortag.textContent = i+1
        anchortag.value = i+1      
        anchortag.style.display="inline-block"
        
        jQuery('#page-links').append(anchortag)
        
  }
  
}
  $('#page-links').on('click', 'a', function(event) {
    var term = jQuery('#searchterm').val()
    pagenum=jQuery(this).val()
    
    console.log('Anchor clicked!');
    jQuery.ajax({

      type: "GET",
      url: "/search2",
      data: {

        myterm: term,
        pagenum:pagenum,
      },
      success: function (data) {
        console.log(data)
        
        // $('#page-links').empty();
        $('#emplist tbody').empty();
        $("#cmbname").empty()
        jQuery('.js-example-basic-single').empty()
       var counter=0
        $.each(data, function (i, item) {
          counter=counter+1
          var name = item.employee_fname
          var lname = item.employee_lname
          var id = item.pk
          

          var markup = "<tr><td><input type='checkbox' name='record'></td><td>" + name + "</td><td>" + lname + "</td></tr>";

          var combostring = "<option value='" + id + "'>" + name + "</option>"
          $("#emplist tbody").append(markup);
          jQuery('#cmbname').append(combostring);
          jQuery('.js-example-basic-single').append(combostring)

        });

      }
    })
    
    jQuery('#first-get').empty()
    createpaginationcontrols(0)
    event.preventDefault();
    return false;
});
  jQuery('#btnSearch').click(function () {

    var term = jQuery('#searchterm').val()
    /*totalcount= jQuery('#hdTotalCount').val()*/
    jQuery.ajax({

      type: "GET",
      url: "/search",
      data: {

        myterm: term
      },
      success: function (data) {
        console.log(data)
        $('#emplist tbody').empty();
        $("#cmbname").empty()
        jQuery('.js-example-basic-single').empty()
        
        var counter=0;
        
        jQuery('#first-get').empty()
        $.each(data, function (i, item) {
          counter=counter+1
          console.log(i)
          if(i=='totalcount'){
            
            jQuery('#hdTotalCount').val(item.querysetcount)
          }
          var name = item.employee_fname
          var lname = item.employee_lname
          var id = item.pk
          

          var markup = "<tr><td><input type='checkbox' name='record'></td><td>" + name + "</td><td>" + lname + "</td></tr>";

          var combostring = "<option value='" + id + "'>" + name + "</option>"
          $("#emplist tbody").append(markup);
          jQuery('#cmbname').append(combostring);
          jQuery('.js-example-basic-single').append(combostring)

        });
        
        
        createpaginationcontrols(counter)
      }
    })
  });
});
